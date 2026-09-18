from prioritization.business_impact import BusinessImpactAnalyzer
from prioritization.onnx_inference import ONNXSeverityInference
from prioritization.features import IncidentFeatureExtractor
from models.incidents import Incident


class IncidentPrioritizer:

    def __init__(self, model_path: str):
        self.feature_extractor = IncidentFeatureExtractor()
        self.impact_analyzer = BusinessImpactAnalyzer()
        self.severity_model = ONNXSeverityInference(model_path)

    def prioritize(self, incident: Incident) -> dict:
        features = self.feature_extractor.extract(incident)

        severity_result = self.severity_model.predict(features)

        impact_result = self.impact_analyzer.analyze(incident)

        return {
            "incident_id": incident.incident_id,
            "severity": severity_result["severity"],
            "severity_confidence": severity_result["confidence"],
            "business_impact": impact_result,
        }