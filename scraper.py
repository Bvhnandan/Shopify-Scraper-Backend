import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re

def fetch_products_json(base_url: str) -> List[Dict]:
    url = base_url.rstrip("/") + "/products.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("products", [])
        return []
    except Exception:
        return []

def scrape_hero_products(base_url: str) -> List[Dict]:
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        hero_products = []
        # Adapt selectors to your target site
        for card in soup.find_all("div", class_="grid-product__content"):
            title_tag = card.find("div", class_="grid-product__title")
            price_tag = card.find("div", class_="grid-product__price")
            img_tag = card.find("img")
            title = title_tag.get_text(strip=True) if title_tag else None
            price = price_tag.get_text(strip=True) if price_tag else None
            image = img_tag.get("src") if img_tag else None
            hero_products.append({
                "title": title,
                "price": price,
                "image": image
            })
        return hero_products
    except Exception:
        return []

def scrape_policies(base_url: str, policy: str) -> str:
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            if policy in link.get_text(strip=True).lower():
                policy_url = link.get("href")
                if not policy_url.startswith("http"):
                    policy_url = base_url.rstrip("/") + "/" + policy_url.lstrip("/")
                policy_resp = requests.get(policy_url, timeout=10)
                policy_soup = BeautifulSoup(policy_resp.text, "html.parser")
                paragraphs = policy_soup.find_all("p")
                return "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        return ""
    except Exception:
        return ""

def scrape_faqs(base_url: str) -> List[Dict]:
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        faqs = []
        faq_section = soup.find("section", class_="faq") or soup.find(id="faq")
        if faq_section:
            for item in faq_section.find_all(["div", "li"], class_="faq-item"):
                q = item.find(class_="question")
                a = item.find(class_="answer")
                if q and a:
                    faqs.append({"question": q.get_text(strip=True), "answer": a.get_text(strip=True)})
        return faqs
    except Exception:
        return []

def scrape_social_handles(base_url: str) -> List[str]:
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        social = []
        for link in soup.find_all("a", href=True):
            if any(h in link["href"] for h in ["instagram.com", "facebook.com", "tiktok.com", "twitter.com"]):
                social.append(link["href"])
        return social
    except Exception:
        return []

def scrape_contact_details(base_url: str) -> List[str]:
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        contacts = []
        emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", soup.text))
        contacts.extend(emails)
        phones = set(re.findall(r"\+?\d[\d -]{7,}\d", soup.text))
        contacts.extend(phones)
        return contacts
    except Exception:
        return []

def scrape_about_brand(base_url: str) -> str:
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            if "about" in link.get_text(strip=True).lower():
                about_url = link.get("href")
                if not about_url.startswith("http"):
                    about_url = base_url.rstrip("/") + "/" + about_url.lstrip("/")
                about_resp = requests.get(about_url, timeout=10)
                about_soup = BeautifulSoup(about_resp.text, "html.parser")
                paragraphs = about_soup.find_all("p")
                return "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        return ""
    except Exception:
        return ""

def scrape_important_links(base_url: str) -> List[str]:
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        important = []
        keywords = ["order", "track", "contact", "blog"]
        for link in soup.find_all("a", href=True):
            text = link.get_text(strip=True).lower()
            if any(k in text for k in keywords):
                important.append(link["href"])
        return important
    except Exception:
        return []

def fetch_all_insights(base_url: str) -> dict:
    catalog = fetch_products_json(base_url)
    hero = scrape_hero_products(base_url)
    privacy = scrape_policies(base_url, "privacy")
    refund = scrape_policies(base_url, "refund")
    return_policy = scrape_policies(base_url, "return")
    faqs = scrape_faqs(base_url)
    social = scrape_social_handles(base_url)
    contacts = scrape_contact_details(base_url)
    about = scrape_about_brand(base_url)
    important = scrape_important_links(base_url)
    return {
        "products_catalog": catalog,
        "hero_products": hero,
        "privacy_policy": privacy,
        "refund_policy": refund,
        "return_policy": return_policy,
        "faqs": faqs,
        "social_handles": social,
        "contact_details": contacts,
        "brand_about": about,
        "important_links": important
    }
