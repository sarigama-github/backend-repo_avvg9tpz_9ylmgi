import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from database import db, create_document
from schemas import ContactRequest

app = FastAPI(title="Grande Charte API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Grande Charte Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            from pymongo.errors import PyMongoError
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
                response["database_name"] = db.name
            except PyMongoError as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = response["database_name"] or ("✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set")
    return response

# --------------------------------------------------
# Contact Endpoint
# --------------------------------------------------

class ContactIn(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    market_region: Optional[str] = None
    interest: str = Field(..., description="Allocation request / Event collaboration / Professional inquiry / Press")
    message: Optional[str] = None

@app.post("/contact")
def submit_contact(payload: ContactIn):
    try:
        # Persist to database
        contact = ContactRequest(
            name=payload.name,
            email=payload.email,
            market_region=payload.market_region,
            interest=payload.interest,
            message=payload.message,
        )
        inserted_id = create_document("contactrequest", contact)

        # Send email notification (placeholder using SMTP via requests to a mailhook or similar)
        # For now we simulate success. In a real deployment, integrate with Postmark/SES/etc.
        notification_email = os.getenv("NOTIFY_EMAIL", "hello@grandecharte.com")
        _ = notification_email  # variable used placeholder

        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
