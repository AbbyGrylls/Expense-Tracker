from fastapi import APIRouter, Request, Depends
from app.database import insights_collection
from app.middleware import authenticate_user

router = APIRouter(prefix="/insights", tags=["Insights"])

@router.get("/summary")
async def get_summary(request: Request, userId=Depends(authenticate_user)):
    summary = await insights_collection.find_one({"userId": userId})
    return summary if summary else {"categories": []}

@router.get("/alerts")
async def get_budget_alerts(request: Request, userId=Depends(authenticate_user)):
    summary = await insights_collection.find_one({"userId": userId})
    alerts = []
    if summary:
        for category in summary["categories"]:
            if category["totalSpent"] >= 0.8 * category["limit"]:
                alerts.append({
                    "category": category["name"],
                    "message": f"You have spent {category['totalSpent']} out of {category['limit']}!"
                })
    return {"alerts": alerts}
