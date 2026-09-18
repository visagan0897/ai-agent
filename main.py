from fastapi import FastAPI
from models import IncidentRequest
from agent import IncidentAgent


app = FastAPI(
    title="AI Incident Resolution Agent",
    description="AI Agent for enterprise incident analysis",
    version="1.0.0"
)


agent = IncidentAgent()


@app.get("/")
def root():
    return {
        "agent": "AI Incident Resolution Agent",
        "status": "online"
    }


@app.post("/analyze")
def analyze_incident(incident: IncidentRequest):
    return agent.analyze(incident)