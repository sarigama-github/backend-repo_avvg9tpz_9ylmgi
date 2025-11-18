"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# --------------------------------------------------
# Grande Charte Schemas
# --------------------------------------------------

class Cuvee(BaseModel):
    """
    Cuvée collection schema
    Collection name: "cuvee"
    """
    name: str = Field(..., description="Cuvée name")
    collection: str = Field(..., description="Collection name, e.g., GC-5, GC-4, Iroise 769, Alba")
    vintage: Optional[str] = Field(None, description="Vintage year or NV")
    tasting_notes: Optional[str] = Field(None, description="Tasting notes")
    technical_notes: Optional[str] = Field(None, description="Technical notes")
    imagery: Optional[List[str]] = Field(default=None, description="List of image URLs")
    key_story: Optional[str] = Field(None, description="Key story about the cuvée")

class ContactRequest(BaseModel):
    """
    Contact requests from the website
    Collection name: "contactrequest"
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Valid email address")
    market_region: Optional[str] = Field(None, description="Market / Region")
    interest: str = Field(..., description="What brings you: Allocation / Event / Professional / Press")
    message: Optional[str] = Field(None, description="Free message")

# --------------------------------------------------
# Example schemas (kept for reference)
# --------------------------------------------------

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Note: The Flames database viewer can read these schemas from GET /schema endpoint if implemented.
