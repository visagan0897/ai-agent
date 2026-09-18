import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

const API = "http://127.0.0.1:8000";

type Alert = {
  alert_id: string;
  service: string;
  original_message: string;
  normalized_message: string;
  alert_type: string;
  severity: string;
  source: string;
};

type Incident = {
  incident_id: string;
  created_at: string;
  service: string;
  description: string;
  alerts: Alert[];
  logs: string[];
  metrics: {
    error_rate?: number;
    latency?: number;
  };
  recent_changes: string[];
  dependencies: string[];
  system_state: Record<string, unknown>;
};

type CorrelationResponse = {
  incidents: Incident[];
};

type InvestigationResult = {
  incident: Incident;
  ai_decision: {
    root_cause?: {
      description?: string;
      confidence?: number;
    };
    evidence?: string[];
    severity?: string;
    business_impact?: string;
    possible_actions?: {
      action_id: string;
      action: string;
      reason: string;
    }[];
    selected_action?: {
      action_id: string;
      action: string;
      reason: string;
    };
    execution_mode?: string;
    explanation?: string;
  };
  execution?: {
    status?: string;
    action?: string;
    result?: {
      service?: string;
      status?: string;
    };
  };
  verification?: {
    status?: string;
    recovered?: boolean;
    service?: string;
    reason?: string;
  };
};

type InvestigationResponse = {
  service: string;
  incident_count: number;
  results: InvestigationResult[];
};

function IncidentDetails() {
  const { incidentId } = useParams();

  const [incident, setIncident] =
    useState<Incident | null>(null);

  const [resolution, setResolution] =
    useState<InvestigationResult | null>(null);

  const [loading, setLoading] = useState(true);
  const [resolving, setResolving] = useState(false);
  const [error, setError] = useState("");

  // Load the incident without executing remediation
  const loadIncident = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API}/correlate/payment-service`
      );

      if (!response.ok) {
        throw new Error("Failed to load incident");
      }

      const data: CorrelationResponse =
        await response.json();

      const foundIncident =
        data.incidents.find(
          (item) =>
            item.incident_id === incidentId
        );

      if (!foundIncident) {
        setIncident(null);
        return;
      }

      setIncident(foundIncident);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to load incident details."
      );
    } finally {
      setLoading(false);
    }
  };

  // Run the complete AI resolution pipeline
  const runResolution = async () => {
    try {
      setResolving(true);
      setError("");

      const response = await fetch(
        `${API}/investigate/payment-service`
      );

      if (!response.ok) {
        throw new Error(
          "AI resolution failed"
        );
      }

      const data: InvestigationResponse =
        await response.json();

      const result =
        data.results.find(
          (item) =>
            item.incident.incident_id ===
            incidentId
        );

      if (result) {
        setResolution(result);
      }

      await loadIncident();
    } catch (err) {
      console.error(err);
      setError(
        "AI resolution could not be completed."
      );
    } finally {
      setResolving(false);
    }
  };

  useEffect(() => {
    loadIncident();
  }, [incidentId]);

  if (loading) {
    return (
      <div className="empty-state">
        Loading incident details...
      </div>
    );
  }

  if (!incident) {
    return (
      <div>
        <div className="empty-state">
          Incident not found or already resolved.
        </div>

        <div style={{ marginTop: "20px" }}>
          <Link
            className="primary-button"
            to="/"
          >
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const aiDecision =
    resolution?.ai_decision;

  const confidence =
    aiDecision?.root_cause?.confidence;

  return (
    <section className="incident-details-page">

      {/* ERROR */}

      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}

      {/* HEADER */}

      <section className="incident-section">

        <div className="section-header">
          <div>
            <p className="eyebrow">
              INCIDENT DETAILS
            </p>

            <h3>
              {incident.incident_id}
            </h3>
          </div>

          <span className="severity-badge">
            {aiDecision?.severity ||
              "HIGH"}
          </span>
        </div>

        <div className="incident-card">

          <div className="incident-header">

            <div>
              <span className="incident-id">
                {incident.service}
              </span>

              <h3>
                Payment Service Incident
              </h3>

              <p>
                {incident.description}
              </p>
            </div>

            <span className="incident-state">
              {resolution
                ? "ANALYZED"
                : "DETECTED"}
            </span>

          </div>

          <div className="incident-grid">

            <div>
              <span className="label">
                ALERTS
              </span>

              <strong>
                {incident.alerts.length}
              </strong>
            </div>

            <div>
              <span className="label">
                SERVICE
              </span>

              <strong>
                {incident.service}
              </strong>
            </div>

            <div>
              <span className="label">
                ERROR RATE
              </span>

              <strong>
                {incident.metrics
                  ?.error_rate ?? 0}
              </strong>
            </div>

            <div>
              <span className="label">
                LATENCY
              </span>

              <strong>
                {incident.metrics
                  ?.latency ?? 0}s
              </strong>
            </div>

          </div>

          <div className="incident-actions">

            <button
              className="primary-button"
              onClick={runResolution}
              disabled={resolving}
            >
              {resolving
                ? "AI Resolving..."
                : "Run AI Resolution"}
            </button>

          </div>

        </div>
      </section>

      {/* ALERTS */}

      <section className="resolution-section">

        <div className="section-header">
          <div>
            <p className="eyebrow">
              CORRELATED SIGNALS
            </p>

            <h3>
              Alerts
            </h3>
          </div>
        </div>

        <div className="resolution-grid">

          {incident.alerts.map(
            (alert) => (
              <div
                className="result-card"
                key={alert.alert_id}
              >
                <span className="label">
                  {alert.alert_type}
                </span>

                <p>
                  {alert.original_message}
                </p>

                <small>
                  Source: {alert.source}
                </small>
              </div>
            )
          )}

        </div>
      </section>

      {/* LOGS + METRICS */}

      <section className="resolution-section">

        <div className="section-header">
          <div>
            <p className="eyebrow">
              INVESTIGATION EVIDENCE
            </p>

            <h3>
              System Evidence
            </h3>
          </div>
        </div>

        <div className="resolution-grid">

          <div className="result-card">

            <span className="label">
              LOGS
            </span>

            {incident.logs.length === 0 ? (
              <p>No logs available.</p>
            ) : (
              incident.logs.map(
                (log, index) => (
                  <p key={index}>
                    {log}
                  </p>
                )
              )
            )}

          </div>

          <div className="result-card">

            <span className="label">
              METRICS
            </span>

            <p>
              Error Rate:{" "}
              {incident.metrics
                ?.error_rate ?? 0}
            </p>

            <p>
              Latency:{" "}
              {incident.metrics
                ?.latency ?? 0}s
            </p>

          </div>

        </div>
      </section>

      {/* AI RESULT */}

      {resolution && (
        <>
          <section className="resolution-section">

            <div className="section-header">
              <div>
                <p className="eyebrow">
                  AI INVESTIGATION
                </p>

                <h3>
                  Root Cause Analysis
                </h3>
              </div>
            </div>

            <div className="resolution-grid">

              <div className="result-card">

                <span className="label">
                  PROBABLE ROOT CAUSE
                </span>

                <p>
                  {aiDecision?.root_cause
                    ?.description ||
                    "No root cause identified."}
                </p>

              </div>

              <div className="result-card">

                <span className="label">
                  CONFIDENCE
                </span>

                <strong>
                  {confidence !==
                  undefined
                    ? `${Math.round(
                        confidence * 100
                      )}%`
                    : "N/A"}
                </strong>

              </div>

              <div className="result-card">

                <span className="label">
                  BUSINESS IMPACT
                </span>

                <p>
                  {aiDecision
                    ?.business_impact ||
                    "No impact assessment available."}
                </p>

              </div>

              <div className="result-card">

                <span className="label">
                  EXECUTION MODE
                </span>

                <strong>
                  {aiDecision
                    ?.execution_mode
                    ?.toUpperCase() ||
                    "UNKNOWN"}
                </strong>

              </div>

            </div>

          </section>

          {/* AI EVIDENCE */}

          <section className="resolution-section">

            <div className="section-header">
              <div>
                <p className="eyebrow">
                  AI REASONING
                </p>

                <h3>
                  Evidence
                </h3>
              </div>
            </div>

            <div className="incident-card">

              {aiDecision?.evidence?.map(
                (item, index) => (
                  <p
                    key={index}
                    style={{
                      margin:
                        "0 0 12px",
                      lineHeight: 1.6,
                    }}
                  >
                    {index + 1}. {item}
                  </p>
                )
              )}

              {aiDecision?.explanation && (
                <p
                  style={{
                    margin:
                      "20px 0 0",
                    paddingTop:
                      "20px",
                    borderTop:
                      "1px solid #e5e5e5",
                    lineHeight: 1.6,
                  }}
                >
                  <strong>
                    Decision:
                  </strong>{" "}
                  {
                    aiDecision.explanation
                  }
                </p>
              )}

            </div>

          </section>

          {/* ACTION DECISION */}

          <section className="resolution-section">

            <div className="section-header">
              <div>
                <p className="eyebrow">
                  REMEDIATION DECISION
                </p>

                <h3>
                  Selected Action
                </h3>
              </div>
            </div>

            <div className="incident-card">

              <div className="incident-grid">

                <div>
                  <span className="label">
                    ACTION
                  </span>

                  <strong>
                    {aiDecision
                      ?.selected_action
                      ?.action ||
                      "No action selected"}
                  </strong>
                </div>

                <div>
                  <span className="label">
                    ACTION ID
                  </span>

                  <strong>
                    {aiDecision
                      ?.selected_action
                      ?.action_id ||
                      "N/A"}
                  </strong>
                </div>

                <div>
                  <span className="label">
                    EXECUTION
                  </span>

                  <strong>
                    {resolution.execution
                      ?.status
                      ?.toUpperCase() ||
                      "UNKNOWN"}
                  </strong>
                </div>

                <div>
                  <span className="label">
                    VERIFICATION
                  </span>

                  <strong>
                    {resolution.verification
                      ?.recovered
                      ? "RECOVERED"
                      : "NOT RECOVERED"}
                  </strong>
                </div>

              </div>

              <p
                style={{
                  margin: "0",
                  lineHeight: 1.6,
                }}
              >
                <strong>
                  Reason:
                </strong>{" "}
                {aiDecision
                  ?.selected_action
                  ?.reason ||
                  "No reason provided."}
              </p>

            </div>

          </section>

          {/* FINAL STATUS */}

          <section className="resolution-section">

            <div className="section-header">
              <div>
                <p className="eyebrow">
                  VERIFICATION
                </p>

                <h3>
                  Resolution Status
                </h3>
              </div>
            </div>

            <div className="incident-card">

              <div className="incident-grid">

                <div>
                  <span className="label">
                    STATUS
                  </span>

                  <strong>
                    {resolution.verification
                      ?.status
                      ?.toUpperCase() ||
                      "UNKNOWN"}
                  </strong>
                </div>

                <div>
                  <span className="label">
                    SERVICE
                  </span>

                  <strong>
                    {resolution.verification
                      ?.service ||
                      incident.service}
                  </strong>
                </div>

                <div>
                  <span className="label">
                    RECOVERED
                  </span>

                  <strong>
                    {resolution.verification
                      ?.recovered
                      ? "YES"
                      : "NO"}
                  </strong>
                </div>

                <div>
                  <span className="label">
                    RESULT
                  </span>

                  <strong>
                    {resolution.execution
                      ?.result
                      ?.status
                      ?.toUpperCase() ||
                      "N/A"}
                  </strong>
                </div>

              </div>

              <p
                style={{
                  margin: "0",
                  lineHeight: 1.6,
                }}
              >
                {
                  resolution.verification
                    ?.reason
                }
              </p>

            </div>

          </section>
        </>
      )}

      {/* BACK */}

      <div style={{ marginTop: "10px" }}>
        <Link
          className="primary-button"
          to="/"
        >
          ← Back to Dashboard
        </Link>
      </div>

    </section>
  );
}

export default IncidentDetails;