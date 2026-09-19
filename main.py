from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.requests import IncidentRequest
from agent import IncidentAgent

from monitoring.enterprise_monitor import EnterpriseMonitor
from monitoring.detector import IncidentDetector
from monitoring.pipeline import MonitoringPipeline

from clustering.pipeline import CorrelationPipeline

from ai_brain.decision_engine import AIDecisionEngine

from remediation.registry_setup import create_action_registry
from remediation.action_planner import ActionPlanner
from remediation.executor import RemediationExecutor

from verification.verifier import IncidentVerifier

from database import save_incident, save_resolution


app = FastAPI(
    title="AI Incident Resolution Agent",
    description="AI Agent for enterprise incident analysis",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


agent = IncidentAgent()

enterprise_monitor = EnterpriseMonitor(
    "http://127.0.0.1:8002"
)

incident_detector = IncidentDetector()

monitoring_pipeline = MonitoringPipeline()

correlation_pipeline = CorrelationPipeline()


action_registry = create_action_registry()

action_planner = ActionPlanner()

remediation_executor = RemediationExecutor(
    action_registry
)

incident_verifier = IncidentVerifier()


ai_capabilities = [
    {
        "action_id": "recover_payment_service",
        "description": "Recover the payment service to its healthy state.",
        "autonomous": True,
    }
]


ai_decision_engine = AIDecisionEngine(
    capabilities=ai_capabilities
)


@app.get("/")
def root():
    return {
        "agent": "AI Incident Resolution Agent",
        "status": "online"
    }


@app.post("/analyze")
async def analyze_incident(incident: IncidentRequest):
    return await agent.analyze(incident)


@app.get("/observe/{service}")
async def observe_service(service: str):

    evidence = await enterprise_monitor.collect(service)

    return evidence


@app.get("/detect/{service}")
async def detect_incident(service: str):

    evidence = await enterprise_monitor.collect(service)

    alerts = incident_detector.detect(
        health=evidence["health"],
        logs=evidence["logs"],
        metrics=evidence["metrics"],
    )

    return {
        "service": service,
        "alerts": [
            alert.model_dump(mode="json")
            for alert in alerts
        ],
    }


@app.get("/correlate/{service}")
async def correlate_incident(service: str):

    evidence = await enterprise_monitor.collect(service)

    alerts = incident_detector.detect(
        health=evidence["health"],
        logs=evidence["logs"],
        metrics=evidence["metrics"],
    )

    normalized_alerts = monitoring_pipeline.process(alerts)

    correlation_result = correlation_pipeline.process(
        normalized_alerts,
        evidence=evidence,
    )

    for incident in correlation_result["incidents"]:
        save_incident(incident)

    return {
        "service": service,
        "alert_count": len(alerts),
        "normalized_alert_count": len(normalized_alerts),
        "incidents": [
            incident.model_dump(mode="json")
            for incident in correlation_result["incidents"]
        ],
        "outliers": [
            alert.model_dump(mode="json")
            if hasattr(alert, "model_dump")
            else alert
            for alert in correlation_result["outliers"]
        ],
    }


@app.get("/investigate/{service}")
async def investigate_incident(service: str):

    evidence = await enterprise_monitor.collect(service)

    alerts = incident_detector.detect(
        health=evidence["health"],
        logs=evidence["logs"],
        metrics=evidence["metrics"],
    )

    normalized_alerts = monitoring_pipeline.process(alerts)

    correlation_result = correlation_pipeline.process(
        normalized_alerts,
        evidence=evidence,
    )

    results = []

    for incident in correlation_result["incidents"]:

        save_incident(incident)

        ai_decision = await ai_decision_engine.decide(
            incident
        )

        action_request = action_planner.plan(
            ai_decision
        )

        execution_result = await remediation_executor.execute(
            action_request
        )

        verification_result = await incident_verifier.verify(
            service,
            "http://127.0.0.1:8002/health",
        )

        save_resolution(
            incident_id=incident.incident_id,
            ai_decision=ai_decision,
            execution_result=execution_result,
            verification_result=verification_result,
        )

        results.append({
            "incident": incident.model_dump(mode="json"),
            "ai_decision": ai_decision,
            "action_request": action_request,
            "execution": execution_result,
            "verification": verification_result,
        })

    return {
        "service": service,
        "incident_count": len(results),
        "results": results,
    }