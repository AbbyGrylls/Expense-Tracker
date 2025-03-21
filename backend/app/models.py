from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
class User(BaseModel):
    name: str
    email: EmailStr
    password: str 
class Expense(BaseModel):
    userId: str
    amount: float
    category: str
    date: datetime
    notes: Optional[str] = None
class BudgetCategory(BaseModel):
    name: str
    totalSpent: float

class BudgetSummary(BaseModel):
    userId: str
    categories: List[BudgetCategory]
    lastUpdated: datetime
