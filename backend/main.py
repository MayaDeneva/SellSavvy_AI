from fastapi import FastAPI
from backend.agents.keyword_generator import router as keyword_router
from backend.agents.categorization_agent import router as categorization_router
from backend.agents.description_generator import router as description_router
from backend.agents.background_removal import router as background_router

app = FastAPI(title="E-Commerce AI Agents API")

#  Register each agent
app.include_router(keyword_router, prefix="/keywords", tags=["Keyword Generation"])
app.include_router(categorization_router, prefix="/categorization", tags=["Categorization"])
app.include_router(description_router, prefix="/description", tags=["Description Generation"])
app.include_router(background_router, prefix="/background", tags=["Background Removal"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
