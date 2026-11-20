from enum import Enum
from pydantic import BaseModel, Field

class Category(str, Enum):
    """Category of the product."""
    BILLING = "Billing"
    TECHNICAL = "Technical"
    ACCOUNT = "Account"

class CustomerTicket(BaseModel):
    """Customer ticket model."""
    customer_name: str = Field(description="Name of the customer")
    issue_category: Category = Field(description="Category of the issue")
    urgency: int = Field(ge=1, le=5, description="Urgency from 1 (low) to 5 (high)")
    summary: str = Field(max_length=100, description="Brief summary of the issue")