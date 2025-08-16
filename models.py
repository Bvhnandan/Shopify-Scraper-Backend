from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db import Base

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    site_url = Column(String(512))
    privacy_policy = Column(Text)
    refund_policy = Column(Text)
    return_policy = Column(Text)
    brand_about = Column(Text)

    products = relationship("Product", back_populates="brand")
    faqs = relationship("FAQ", back_populates="brand")
    social_handles = relationship("SocialHandle", back_populates="brand")
    contact_details = relationship("ContactDetail", back_populates="brand")
    important_links = relationship("ImportantLink", back_populates="brand")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512))
    price = Column(String(128))
    image = Column(String(512))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", back_populates="products")

class FAQ(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(1024))
    answer = Column(Text)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", back_populates="faqs")

class SocialHandle(Base):
    __tablename__ = "social_handles"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(512))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", back_populates="social_handles")

class ContactDetail(Base):
    __tablename__ = "contact_details"
    id = Column(Integer, primary_key=True, index=True)
    contact = Column(String(512))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", back_populates="contact_details")

class ImportantLink(Base):
    __tablename__ = "important_links"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(512))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", back_populates="important_links")
