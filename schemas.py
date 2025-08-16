from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ProductBase(BaseModel):
    title: str
    price: Optional[str] = None
    image: Optional[str] = None

class ProductOut(ProductBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class FAQBase(BaseModel):
    question: str
    answer: str

class FAQOut(FAQBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class SocialHandleBase(BaseModel):
    url: str

class SocialHandleOut(SocialHandleBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class ContactDetailBase(BaseModel):
    contact: str

class ContactDetailOut(ContactDetailBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class ImportantLinkBase(BaseModel):
    url: str

class ImportantLinkOut(ImportantLinkBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class BrandBase(BaseModel):
    name: str
    site_url: HttpUrl
    privacy_policy: Optional[str] = None
    refund_policy: Optional[str] = None
    return_policy: Optional[str] = None
    brand_about: Optional[str] = None

class BrandCreate(BrandBase):
    products: List[ProductBase] = []
    faqs: List[FAQBase] = []
    social_handles: List[SocialHandleBase] = []
    contact_details: List[ContactDetailBase] = []
    important_links: List[ImportantLinkBase] = []

class BrandOut(BrandBase):
    id: int
    products: List[ProductOut] = []
    faqs: List[FAQOut] = []
    social_handles: List[SocialHandleOut] = []
    contact_details: List[ContactDetailOut] = []
    important_links: List[ImportantLinkOut] = []
    model_config = {
        "from_attributes": True
    }
