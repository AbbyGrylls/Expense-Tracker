from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, expenses, insights, speech 
import uvicorn

app = FastAPI(title="Expense Manager API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(expenses.router)
app.include_router(insights.router)
app.include_router(users.router)


app.include_router(speech.router) 

@app.get("/")
def home():
    return {"message": "Expense Manager API is running!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
