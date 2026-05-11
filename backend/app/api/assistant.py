"""Assistant API Endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.assistant.nlp_assistant import AnalyticsAssistant
from app.utils.database import get_db

router = APIRouter(prefix="/api/assistant", tags=["AI Assistant"])


@router.post("/query")
async def process_query(
    request: dict,
    db: Session = Depends(get_db)
):
    """Process natural language query"""
    query = request.get('query', '')
    
    if not query:
        return {
            "status": "error",
            "message": "Query text required"
        }
    
    assistant = AnalyticsAssistant(db)
    response = assistant.process_query(query)
    
    return {
        "status": "success",
        "query": query,
        "response": response
    }


@router.get("/suggestions")
async def get_query_suggestions():
    """Get example queries"""
    suggestions = [
        "Which products may stock out next week?",
        "Show top declining products",
        "Forecast next month demand",
        "What are the top selling products?",
        "Show me products with low inventory",
        "Which products have highest revenue?",
        "Show sales trends for the last 30 days",
        "What inventory level should we maintain?"
    ]
    
    return {
        "status": "success",
        "suggestions": suggestions
    }
