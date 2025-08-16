Shopify Insights Fetcher with LLM-enabled Structuring and Competitor Analysis
Overview:
1. Built a FastAPI backend that scrapes Shopify stores for detailed product, policy, FAQ, and brand data, then uses Groq’s GPT-OSS-120B LLM to intelligently structure this raw data and identify relevant competitor stores.
2. Persisted the structured insights in a SQLite database with SQLAlchemy, enabling recursive competitor analysis and providing robust API endpoints for data retrieval and market research.

Features Implemented:
1. Comprehensive Web Scraping
2. Scrapes Shopify storefronts for both JSON product feeds and homepage content.
3. Extracts core data elements such as product catalog, hero products, store policies (privacy, refund, return), FAQs, social handles, contact details, About page content, and important store links.
4. Integration with Groq LLM API
5. Sends raw scraped data to Groq's GPT-OSS-120B model API for:
  1. Structuring the unorganized raw data into well-defined JSON format.
  2. Extracting and suggesting up to five relevant competitor Shopify stores automatically.
  3. Parses and validates the LLM response before persisting.
  4. Automated Competitor Analysis
  5. For each competitor URL suggested by the LLM, the system scrapes and structures their data similarly.
6. Stores competitor insights alongside the main brand in the database.
7.Data Persistence:
  1. Uses SQLite as the database backend for ease of deployment and portability.
  2. Defines a comprehensive SQLAlchemy ORM model schema including Brands, Products, FAQs, Social Handles, Contact Details, and Important Links.
8. Robust API Endpoints
  1. /fetch-insights/ (POST): Accepts a Shopify store URL, scrapes the site, sends data to the LLM API for structuring and competitor extraction, persists all data, and returns structured brand insights and competitor data.
  2. /brands/ (GET): Retrieves all stored brands and their associated insights from the database.
  3. Error Handling and Request Validation
9. Future-ready Pydantic Schemas
10. Uses Pydantic V2-compatible model_config = {"from_attributes": True} for ORM model serialization.

Technologies and Tools Used
1. FastAPI: for building RESTful HTTP API endpoints.

2. SQLAlchemy: for ORM database modeling and interaction with SQLite.

3. SQLite: lightweight local relational database.

4. Requests: for HTTP client requests.

5. BeautifulSoup4: for HTML parsing and scraping.

6. Groq API: Large Language Model API for semantic data structuring and competitor extraction.

Python 3.12+

Project Structure:
1. db.py - Defines database connection and session management.

2. models.py - SQLAlchemy ORM models for brands, products, FAQs, social links, contacts, and important store links.

3. schemas.py - Pydantic models for request validation and response serialization.

4. scraper.py - Functions to scrape Shopify JSON feeds and parse store pages for detailed info.

5. main.py - FastAPI app configuring endpoints and orchestrating scraping, LLM calls, data saving, and response logic.

How It Works
1. User sends a POST request to /fetch-insights/ with a Shopify store URL.
2. The backend scrapes the store’s public content and product JSON feed, collecting raw data.
3. Raw data plus instructions are sent as a prompt to the Groq API's GPT-OSS-120B model.
4. The LLM returns structured JSON including cleaned products, policies, FAQs, contacts, and competitor URLs.
5. The backend persists this structured data into the SQLite database.
6. For each competitor found, the process repeats recursively.
7. The endpoint responds with the structured data of the main brand plus all competitors.

Limitations & Notes:
1. The Groq API has payload size limits; therefore, large datasets are truncated or preprocessed before sending.
2. Competitor detection depends on the LLM's ability to suggest valid Shopify stores and is heuristic in nature.
3. Scraping logic may need adjustments based on variations in Shopify themes or custom storefronts.
4. This backend does not include frontend UI but exposes clean JSON APIs consumable by any client.

Setup Instructions
1. Install dependencies from requirements.txt: fastapi uvicorn sqlalchemy pydantic requests beautifulsoup4
2. Set your Groq API key or any other llm in main.py or preferably as an environment variable and read it securely.
3. Run the API server: uvicorn main:app --reload
4. Testing with Postman
  1. Open Postman and create a new POST request.
  2. http://127.0.0.1:8000/fetch-insights/?site_url=https://example-shopify-store.com
  3. Make sure the method is POST.
  4. You should receive a JSON response with structured brand insights and competitors.


