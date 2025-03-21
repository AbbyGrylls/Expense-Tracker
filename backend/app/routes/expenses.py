from fastapi import APIRouter, Request, Depends
from app.database import expenses_collection
from app.models import Expense
from app.middleware import authenticate_user
from bson import ObjectId

router = APIRouter(prefix="/expenses", tags=["Expenses"])
@router.post("/")
async def add_expense(expense: Expense, request: Request, userId=Depends(authenticate_user)):
    expense_data = expense.dict()
    expense_data["userId"] = userId
    result = await expenses_collection.insert_one(expense_data)
    expense_data["_id"] = str(result.inserted_id)

    return expense_data



@router.get("/")
async def get_expenses(request: Request, userId=Depends(authenticate_user)):
    expenses = await expenses_collection.find({"userId": userId}).to_list(100)
    for expense in expenses:
        expense["_id"] = str(expense["_id"])
    return expenses