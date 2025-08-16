from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models
import schemas
from db import SessionLocal, engine
from scraper import fetch_all_insights
import requests
import json

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import json
import requests
from fastapi import HTTPException

def call_groq_llm_for_structuring(raw_data: dict, brand_url: str) -> dict:
    prompt = f"""
    Here is raw data scraped from {brand_url}:\n{json.dumps(raw_data)}
    Please:
    1. Structure the products (with title, price, image, etc.), policies, faqs, contacts, social handles, about.
    2. Extract and suggest up to 5 web competitors (ecommerce brands or similar shops).
    Return organized JSON as:
    {{
        "products_catalog": [...],
        "policies": {{"privacy": "...", "refund": "...", "return": "..."}},
        "faqs": [...],
        "contacts": [...],
        "social_handles": [...],
        "brand_about": "...",
        "competitors": ["https://brand1.com", "https://brand2.com"]
    }}
    """

    api_endpoint = "https://api.groq.com/openai/v1/chat/completions"
    api_key = " API KEY "  # Replace with your Groq API key

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-oss-120b",  # Or your chosen Groq model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for ecommerce insights."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4096
    }

    try:
        response = requests.post(api_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        resp_json = response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Groq API request failed: {str(e)}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Groq API response is not valid JSON")

    if "choices" not in resp_json or not resp_json["choices"]:
        raise HTTPException(status_code=502, detail=f"Groq API error or empty response: {resp_json}")

    try:
        content = resp_json["choices"][0]["message"]["content"]
        structured_data = json.loads(content)
    except (KeyError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=502, detail=f"Failed to parse Groq content JSON: {str(e)}")

    return structured_data


def save_brand_data(db: Session, insights: dict, site_url: str):
    name = site_url.replace("https://", "").replace("http://", "").split(".").capitalize()
    db_brand = db.query(models.Brand).filter(models.Brand.site_url == site_url).first()
    if not db_brand:
        db_brand = models.Brand(name=name, site_url=site_url)
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
    else:
        db.query(models.Product).filter(models.Product.brand_id == db_brand.id).delete()
        db.query(models.FAQ).filter(models.FAQ.brand_id == db_brand.id).delete()
        db.query(models.SocialHandle).filter(models.SocialHandle.brand_id == db_brand.id).delete()
        db.query(models.ContactDetail).filter(models.ContactDetail.brand_id == db_brand.id).delete()
        db.query(models.ImportantLink).filter(models.ImportantLink.brand_id == db_brand.id).delete()
        db.commit()

    db_brand.privacy_policy = insights.get("policies", {}).get("privacy")
    db_brand.refund_policy = insights.get("policies", {}).get("refund")
    db_brand.return_policy = insights.get("policies", {}).get("return")
    db_brand.brand_about = insights.get("brand_about")

    for prod in insights.get("products_catalog", []) + insights.get("hero_products", []):
        if prod.get("title"):
            db_product = models.Product(
                title=prod.get("title"),
                price=prod.get("price"),
                image=prod.get("image"),
                brand_id=db_brand.id
            )
            db.add(db_product)

    for faq in insights.get("faqs", []):
        db_faq = models.FAQ(
            question=faq.get("question"),
            answer=faq.get("answer"),
            brand_id=db_brand.id
        )
        db.add(db_faq)

    for social in insights.get("social_handles", []):
        db_social = models.SocialHandle(
            url=social,
            brand_id=db_brand.id
        )
        db.add(db_social)

    for contact in insights.get("contact_details", []):
        db_contact = models.ContactDetail(
            contact=contact,
            brand_id=db_brand.id
        )
        db.add(db_contact)

    for link in insights.get("important_links", []):
        db_link = models.ImportantLink(
            url=link,
            brand_id=db_brand.id
        )
        db.add(db_link)

    db.commit()
    db.refresh(db_brand)
    return db_brand

@app.post("/fetch-insights/")
def fetch_brand_insights(site_url: str = Query(..., description="URL of Shopify store"), db: Session = Depends(get_db)):
    raw_data = fetch_all_insights(site_url)
    structured = call_groq_llm_for_structuring(raw_data, site_url)
    brand = save_brand_data(db, structured, site_url)

    competitors = structured.get("competitors", [])
    competitor_brands = []
    for competitor_url in competitors:
        comp_raw = fetch_all_insights(competitor_url)
        comp_structured = call_groq_llm_for_structuring(comp_raw, competitor_url)
        save_brand_data(db, comp_structured, competitor_url)
        competitor_brands.append(comp_structured)

    return {"main_brand": structured, "competitors": competitor_brands}

@app.get("/brands/", response_model=list[schemas.BrandOut])
def read_brands(db: Session = Depends(get_db)):
    brands = db.query(models.Brand).all()
    return brands
