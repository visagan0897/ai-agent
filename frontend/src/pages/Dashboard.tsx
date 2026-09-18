import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

/* =========================================================
   TYPES
========================================================= */

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
  recent_changes?: string[];
  dependencies?: string[];
  system_state?: Record<string, unknown>;
  cluster_id?: string | null;
};

type CorrelationResponse = {
  service: string;
  alert_count: number;
  normalized_alert_count: number;
  incidents: Incident[];
};

type AIDecision = {
  incident_id?: string;

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

type ResolutionResult = {
  incident: Incident;
  ai_decision: AIDecision;

  action_request?: {
    incident_id?: string;
    action_id?: string;
    requested_action?: string;
    action?: string;
    reason?: string;
    execution_mode?: string;
  };

  execution?: {
    status?: string;
    action?: string;
    message?: string;
    result?: {
      service?: string;
      status?: string;
      [key: string]: unknown;
    };
  };

  verification?: {
    status?: string;
    recovered?: boolean;
    service?: string;
    reason?: string;
    health?: {
      service?: string;
      status?: string;
      status_code?: number;
      [key: string]: unknown;
    };
  };
};

type InvestigationResponse = {
  service: string;
  incident_count: number;
  results: ResolutionResult[];
};


/* =========================================================
   COMPONENT
========================================================= */

function Dashboard() {

  const [incident, setIncident] =
    useState<Incident | null>(null);

  const [resolution, setResolution] =
    useState<ResolutionResult | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [resolving, setResolving] =
    useState(false);

  const [error, setError] =
    useState("");

  const [resolutionStarted, setResolutionStarted] =
    useState(false);

  const [resolutionComplete, setResolutionComplete] =
    useState(false);


  /* =======================================================
     LOAD INCIDENT
  ======================================================= */

  const loadIncident = async () => {

    try {

      const response = await fetch(
        `${API}/correlate/payment-service`
      );

      if (!response.ok) {
        throw new Error(
          "Backend unavailable"
        );
      }

      const data: CorrelationResponse =
        await response.json();

      /*
        Only update the live incident when
        the backend actually has one.

        Once AI resolution has completed,
        preserve the existing incident.
      */

      if (data.incidents?.length > 0) {

        setIncident(
          data.incidents[0]
        );

      } else if (
        !resolutionStarted &&
        !resolutionComplete
      ) {

        setIncident(null);

      }

      setError("");

    } catch (err) {

      console.error(err);

      setError(
        "AI Agent backend is unavailable."
      );

    } finally {

      setLoading(false);

    }
  };


  /* =======================================================
     RUN AI RESOLUTION
  ======================================================= */

  const runResolution = async () => {

    try {

      setResolving(true);
      setResolutionStarted(true);
      setResolutionComplete(false);
      setError("");

      /*
        Scroll to the AI progress section.
      */

      setTimeout(() => {

        document
          .getElementById(
            "ai-resolution"
          )
          ?.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });

      }, 100);


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
        data.results?.[0] || null;


      /*
        Store the complete AI result.
      */

      setResolution(result);


      /*
        Preserve the incident that AI
        actually investigated.
      */

      if (result?.incident) {

        setIncident(
          result.incident
        );

      }


      /*
        AI work is finished.
      */

      setResolutionComplete(true);


      /*
        Move the user to the first AI
        result after React renders it.
      */

      setTimeout(() => {

        document
          .getElementById(
            "ai-root-cause"
          )
          ?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });

      }, 300);

    } catch (err) {

      console.error(err);

      setError(
        "AI resolution could not be completed."
      );

      setResolutionComplete(false);

    } finally {

      setResolving(false);

    }
  };


  /* =======================================================
     POLLING
  ======================================================= */

  useEffect(() => {

    loadIncident();

    const interval =
      setInterval(
        loadIncident,
        3000
      );

    return () => {

      clearInterval(interval);

    };

  }, [resolutionStarted, resolutionComplete]);


  /* =======================================================
     DISPLAY INCIDENT
  ======================================================= */

  const displayIncident =
    incident;


  /* =======================================================
     DERIVED STATE
  ======================================================= */

  const severity =
    resolution
      ?.ai_decision
      ?.severity ||
    "HIGH";

  const recovered =
    resolution
      ?.verification
      ?.recovered ||
    false;

  const confidence =
    resolution
      ?.ai_decision
      ?.root_cause
      ?.confidence ?? null;

  const confidencePercent =
    confidence !== null
      ? Math.round(
          confidence * 100
        )
      : null;

  const selectedAction =
    resolution
      ?.ai_decision
      ?.selected_action;

  const executionStatus =
    resolution
      ?.execution
      ?.status;

  const verificationStatus =
    resolution
      ?.verification
      ?.status;


  /* =======================================================
     RENDER
  ======================================================= */

  return (
    <>

      <div className="bar"></div>


      <div className="tunnel-wrap">

        <div className="stage">

          <div className="tunnel">


            {/* =================================================
                01 — SYSTEM OVERVIEW
            ================================================= */}

            <section
              className="panel"
              data-step="01"
            >

              <p className="eyebrow">
                INCIDENT COMMAND CENTER
              </p>

              <h2>
                System Overview
              </h2>

              <p>
                Monitor enterprise services,
                correlate operational signals,
                and resolve incidents through
                an autonomous AI workflow.
              </p>

              <div className="incident-grid">

                <div>

                  <span className="label">
                    ACTIVE INCIDENT
                  </span>

                  <strong>
                    {displayIncident
                      ? "01"
                      : "00"}
                  </strong>

                </div>


                <div>

                  <span className="label">
                    SERVICE
                  </span>

                  <strong>
                    {displayIncident?.service ||
                      "payment-service"}
                  </strong>

                </div>


                <div>

                  <span className="label">
                    SEVERITY
                  </span>

                  <strong>
                    {displayIncident
                      ? severity
                      : "NONE"}
                  </strong>

                </div>


                <div>

                  <span className="label">
                    SYSTEM STATE
                  </span>

                  <strong>
                    {recovered
                      ? "HEALTHY"
                      : displayIncident
                      ? "DEGRADED"
                      : "NORMAL"}
                  </strong>

                </div>

              </div>

            </section>


            {/* =================================================
                02 — INCIDENT
            ================================================= */}

            <section
              className="panel"
              data-step="02"
            >

              <p className="eyebrow">
                INCIDENT DETECTION
              </p>

              <h2>
                {recovered
                  ? "Resolved Incident"
                  : "Active Incident"}
              </h2>


              {loading ? (

                <p>
                  Collecting operational
                  data...
                </p>

              ) : displayIncident ? (

                <>

                  <div className="incident-card">

                    <span className="label">
                      INCIDENT DESCRIPTION
                    </span>

                    <p>
                      {
                        displayIncident.description
                      }
                    </p>

                  </div>


                  <div
                    className="incident-grid"
                    style={{
                      marginTop: "20px",
                    }}
                  >

                    <div>

                      <span className="label">
                        INCIDENT ID
                      </span>

                      <strong>
                        {
                          displayIncident
                            .incident_id
                        }
                      </strong>

                    </div>


                    <div>

                      <span className="label">
                        CORRELATED ALERTS
                      </span>

                      <strong>
                        {
                          displayIncident
                            .alerts
                            .length
                        }
                      </strong>

                    </div>


                    <div>

                      <span className="label">
                        ERROR RATE
                      </span>

                      <strong>
                        {
                          displayIncident
                            .metrics
                            ?.error_rate ??
                          0
                        }
                      </strong>

                    </div>


                    <div>

                      <span className="label">
                        LATENCY
                      </span>

                      <strong>
                        {
                          displayIncident
                            .metrics
                            ?.latency ??
                          0
                        }s
                      </strong>

                    </div>

                  </div>

                </>

              ) : (

                <div className="incident-card">

                  <span className="label">
                    CURRENT STATE
                  </span>

                  <p>
                    No active incident
                    detected.
                  </p>

                </div>

              )}

            </section>


            {/* =================================================
                03 — PIPELINE
            ================================================= */}

            <section
              className="panel"
              data-step="03"
            >

              <p className="eyebrow">
                AUTONOMOUS WORKFLOW
              </p>

              <h2>
                Resolution Pipeline
              </h2>

              <p>
                Every incident moves through
                an evidence-driven operational
                lifecycle.
              </p>


              <div className="pipeline">

                <div className="pipeline-step completed">

                  <span>
                    01
                  </span>

                  <strong>
                    Detection
                  </strong>

                  <small>
                    Signals collected
                  </small>

                </div>


                <div className="pipeline-line" />


                <div className="pipeline-step completed">

                  <span>
                    02
                  </span>

                  <strong>
                    Correlation
                  </strong>

                  <small>
                    Alerts grouped
                  </small>

                </div>


                <div className="pipeline-line" />


                <div
                  className={
                    `pipeline-step ${
                      resolving
                        ? "active"
                        : resolution
                        ? "completed"
                        : ""
                    }`
                  }
                >

                  <span>
                    03
                  </span>

                  <strong>
                    Investigation
                  </strong>

                  <small>
                    {resolving
                      ? "AI investigating"
                      : resolution
                      ? "Complete"
                      : "Waiting"}
                  </small>

                </div>


                <div className="pipeline-line" />


                <div
                  className={
                    `pipeline-step ${
                      resolution
                        ? "completed"
                        : ""
                    }`
                  }
                >

                  <span>
                    04
                  </span>

                  <strong>
                    Decision
                  </strong>

                  <small>
                    {resolution
                      ? "Action selected"
                      : "Waiting"}
                  </small>

                </div>


                <div className="pipeline-line" />


                <div
                  className={
                    `pipeline-step ${
                      executionStatus ===
                      "executed"
                        ? "completed"
                        : ""
                    }`
                  }
                >

                  <span>
                    05
                  </span>

                  <strong>
                    Remediation
                  </strong>

                  <small>
                    {executionStatus ||
                      "Waiting"}
                  </small>

                </div>


                <div className="pipeline-line" />


                <div
                  className={
                    `pipeline-step ${
                      recovered
                        ? "completed"
                        : ""
                    }`
                  }
                >

                  <span>
                    06
                  </span>

                  <strong>
                    Verification
                  </strong>

                  <small>
                    {recovered
                      ? "Recovered"
                      : "Waiting"}
                  </small>

                </div>

              </div>

            </section>


            {/* =================================================
                04 — CORRELATED ALERTS
            ================================================= */}

            <section
              className="panel"
              data-step="04"
            >

              <p className="eyebrow">
                CORRELATION
              </p>

              <h2>
                Correlated Alerts
              </h2>

              <p>
                Multiple operational symptoms
                are grouped into one incident
                instead of being treated as
                unrelated failures.
              </p>


              {displayIncident
                ?.alerts
                ?.length ? (

                <div className="resolution-grid">

                  {displayIncident.alerts.map(
                    (alert) => (

                      <div
                        className="result-card"
                        key={
                          alert.alert_id
                        }
                      >

                        <span className="label">
                          {
                            alert.alert_type
                          }
                        </span>

                        <p>
                          {
                            alert.original_message
                          }
                        </p>

                        <small>
                          {alert.source}
                        </small>

                      </div>

                    )
                  )}

                </div>

              ) : (

                <div className="incident-card">

                  <p>
                    No correlated alerts
                    available.
                  </p>

                </div>

              )}

            </section>


            {/* =================================================
                05 — SYSTEM EVIDENCE
            ================================================= */}

            <section
              className="panel"
              data-step="05"
            >

              <p className="eyebrow">
                INVESTIGATION INPUT
              </p>

              <h2>
                System Evidence
              </h2>

              <p>
                The AI receives operational
                evidence before making a
                remediation decision.
              </p>


              <div className="resolution-grid">

                <div className="result-card">

                  <span className="label">
                    LOGS
                  </span>

                  {displayIncident
                    ?.logs
                    ?.length ? (

                    displayIncident.logs.map(
                      (
                        log,
                        index
                      ) => (

                        <p key={index}>
                          {log}
                        </p>

                      )
                    )

                  ) : (

                    <p>
                      No logs available.
                    </p>

                  )}

                </div>


                <div className="result-card">

                  <span className="label">
                    METRICS
                  </span>

                  <p>
                    Error Rate:{" "}
                    {
                      displayIncident
                        ?.metrics
                        ?.error_rate ??
                      0
                    }
                  </p>

                  <p>
                    Latency:{" "}
                    {
                      displayIncident
                        ?.metrics
                        ?.latency ??
                      0
                    }s
                  </p>

                </div>


                <div className="result-card">

                  <span className="label">
                    DEPENDENCIES
                  </span>

                  {displayIncident
                    ?.dependencies
                    ?.length ? (

                    displayIncident.dependencies.map(
                      (
                        dependency,
                        index
                      ) => (

                        <p key={index}>
                          {dependency}
                        </p>

                      )
                    )

                  ) : (

                    <p>
                      No dependency
                      information.
                    </p>

                  )}

                </div>


                <div className="result-card">

                  <span className="label">
                    RECENT CHANGES
                  </span>

                  {displayIncident
                    ?.recent_changes
                    ?.length ? (

                    displayIncident.recent_changes.map(
                      (
                        change,
                        index
                      ) => (

                        <p key={index}>
                          {change}
                        </p>

                      )
                    )

                  ) : (

                    <p>
                      No recent changes.
                    </p>

                  )}

                </div>

              </div>

            </section>


            {/* =================================================
                06 — AI RESOLUTION
            ================================================= */}

            <section
              id="ai-resolution"
              className="panel ai-launch-panel"
              data-step="06"
            >

              <p className="eyebrow">
                AI INVESTIGATION
              </p>

              <h2>
                Ready for AI Resolution
              </h2>


              {!resolutionStarted ? (

                <>

                  <p>
                    The incident has been
                    detected, correlated,
                    and its operational
                    evidence has been collected.
                  </p>

                  <p>
                    Start the AI investigation
                    to identify the probable
                    root cause, evaluate
                    remediation options,
                    and determine the
                    appropriate action.
                  </p>


                  <button
                    className="primary-button"
                    onClick={
                      runResolution
                    }
                    disabled={
                      !displayIncident ||
                      resolving
                    }
                  >
                    RUN AI RESOLUTION
                  </button>

                </>

              ) : resolving ? (

                <div className="ai-progress">

                  <div className="progress-step active">
                    <span>
                      01
                    </span>

                    Collecting evidence
                  </div>


                  <div className="progress-step active">
                    <span>
                      02
                    </span>

                    Investigating incident
                  </div>


                  <div className="progress-step active">
                    <span>
                      03
                    </span>

                    Identifying root cause
                  </div>


                  <div className="progress-step active">
                    <span>
                      04
                    </span>

                    Evaluating remediation
                  </div>


                  <div className="progress-step">
                    <span>
                      05
                    </span>

                    Verifying recovery
                  </div>

                </div>

              ) : (

                <div className="incident-card">

                  <span className="label">
                    AI INVESTIGATION COMPLETE
                  </span>

                  <p>
                    The AI has completed
                    investigation and selected
                    a remediation decision.
                  </p>

                </div>

              )}

            </section>


            {/* =================================================
                07 — ROOT CAUSE
            ================================================= */}

            {resolutionComplete && (

              <section
                id="ai-root-cause"
                className="panel"
                data-step="07"
              >

                <p className="eyebrow">
                  AI INVESTIGATION
                </p>

                <h2>
                  Root Cause Analysis
                </h2>


                {resolution ? (

                  <>

                    <div className="incident-card">

                      <span className="label">
                        PROBABLE ROOT CAUSE
                      </span>

                      <p>
                        {
                          resolution
                            .ai_decision
                            ?.root_cause
                            ?.description ||
                          "No root cause identified."
                        }
                      </p>

                    </div>


                    <div
                      className="incident-grid"
                      style={{
                        marginTop:
                          "20px",
                      }}
                    >

                      <div>

                        <span className="label">
                          AI CONFIDENCE
                        </span>

                        <strong>
                          {
                            confidencePercent !==
                            null
                              ? `${confidencePercent}%`
                              : "N/A"
                          }
                        </strong>

                        <small>
                          Based on available
                          evidence
                        </small>

                      </div>


                      <div>

                        <span className="label">
                          SEVERITY
                        </span>

                        <strong>
                          {severity}
                        </strong>

                      </div>


                      <div>

                        <span className="label">
                          EVIDENCE SIGNALS
                        </span>

                        <strong>
                          {
                            resolution
                              .ai_decision
                              ?.evidence
                              ?.length ||
                            0
                          }
                        </strong>

                      </div>

                    </div>


                    <div
                      className="incident-card"
                      style={{
                        marginTop:
                          "20px",
                      }}
                    >

                      <span className="label">
                        BUSINESS IMPACT
                      </span>

                      <p>
                        {
                          resolution
                            .ai_decision
                            ?.business_impact ||
                          "No business impact assessment."
                        }
                      </p>

                    </div>


                    <div
                      className="incident-card"
                      style={{
                        marginTop:
                          "20px",
                      }}
                    >

                      <span className="label">
                        SUPPORTING EVIDENCE
                      </span>

                      {resolution
                        .ai_decision
                        ?.evidence
                        ?.length ? (

                        resolution.ai_decision.evidence.map(
                          (
                            evidence,
                            index
                          ) => (

                            <p key={index}>
                              ✓ {evidence}
                            </p>

                          )
                        )

                      ) : (

                        <p>
                          No supporting
                          evidence returned.
                        </p>

                      )}

                    </div>

                  </>

                ) : (

                  <div className="incident-card">

                    <p>
                      AI investigation
                      did not return a
                      result.
                    </p>

                  </div>

                )}

              </section>

            )}


            {/* =================================================
                08 — AI DECISION
            ================================================= */}

            {resolutionComplete && (

              <section
                className="panel"
                data-step="08"
              >

                <p className="eyebrow">
                  AI DECISION ENGINE
                </p>

                <h2>
                  Remediation Decision
                </h2>


                {resolution ? (

                  <>

                    <div className="resolution-grid">

                      <div className="result-card">

                        <span className="label">
                          SELECTED ACTION
                        </span>

                        <p>
                          {
                            selectedAction
                              ?.action ||
                            "No action selected."
                          }
                        </p>

                      </div>


                      <div className="result-card">

                        <span className="label">
                          ACTION ID
                        </span>

                        <strong>
                          {
                            selectedAction
                              ?.action_id ||
                            "N/A"
                          }
                        </strong>

                      </div>


                      <div className="result-card">

                        <span className="label">
                          EXECUTION MODE
                        </span>

                        <strong>
                          {
                            resolution
                              .ai_decision
                              ?.execution_mode
                              ?.toUpperCase() ||
                            "UNKNOWN"
                          }
                        </strong>

                      </div>

                    </div>


                    <div
                      className="incident-card"
                      style={{
                        marginTop:
                          "20px",
                      }}
                    >

                      <span className="label">
                        AI EVALUATED OPTIONS
                      </span>

                      {resolution
                        .ai_decision
                        ?.possible_actions
                        ?.length ? (

                        resolution.ai_decision.possible_actions.map(
                          (
                            option,
                            index
                          ) => (

                            <div
                              className="action-option"
                              key={
                                option.action_id ||
                                index
                              }
                            >

                              <strong>
                                {option.action}
                              </strong>

                              <small>
                                {option.reason}
                              </small>

                            </div>

                          )
                        )

                      ) : (

                        <p>
                          No alternative
                          actions returned.
                        </p>

                      )}

                    </div>


                    <div
                      className="incident-card"
                      style={{
                        marginTop:
                          "20px",
                      }}
                    >

                      <span className="label">
                        DECISION REASON
                      </span>

                      <p>
                        {
                          selectedAction
                            ?.reason ||
                          "No decision reason provided."
                        }
                      </p>

                    </div>

                  </>

                ) : (

                  <p>
                    No AI decision
                    available.
                  </p>

                )}

              </section>

            )}


            {/* =================================================
                09 — EXECUTION
            ================================================= */}

            {resolutionComplete && (

              <section
                className="panel"
                data-step="09"
              >

                <p className="eyebrow">
                  REMEDIATION
                </p>

                <h2>
                  Action Execution
                </h2>


                {resolution ? (

                  <div className="incident-grid">

                    <div>

                      <span className="label">
                        REQUESTED ACTION
                      </span>

                      <strong>
                        {
                          resolution
                            .action_request
                            ?.requested_action ||
                          resolution
                            .execution
                            ?.action ||
                          "N/A"
                        }
                      </strong>

                    </div>


                    <div>

                      <span className="label">
                        EXECUTION MODE
                      </span>

                      <strong>
                        {
                          resolution
                            .action_request
                            ?.execution_mode
                            ?.toUpperCase() ||
                          resolution
                            .ai_decision
                            ?.execution_mode
                            ?.toUpperCase() ||
                          "UNKNOWN"
                        }
                      </strong>

                    </div>


                    <div>

                      <span className="label">
                        STATUS
                      </span>

                      <strong>
                        {
                          executionStatus
                            ?.toUpperCase() ||
                          "UNKNOWN"
                        }
                      </strong>

                    </div>


                    <div>

                      <span className="label">
                        RESULT
                      </span>

                      <strong>
                        {
                          resolution
                            .execution
                            ?.result
                            ?.status
                            ?.toUpperCase() ||
                          "N/A"
                        }
                      </strong>

                    </div>

                  </div>

                ) : (

                  <p>
                    No execution result
                    available.
                  </p>

                )}

              </section>

            )}


            {/* =================================================
                10 — VERIFICATION
            ================================================= */}

            {resolutionComplete && (

              <section
                className="panel"
                data-step="10"
              >

                <p className="eyebrow">
                  POST-REMEDIATION
                </p>

                <h2>
                  Verification
                </h2>


                {resolution ? (

                  <>

                    <div className="incident-grid">

                      <div>

                        <span className="label">
                          VERIFICATION
                        </span>

                        <strong>
                          {
                            verificationStatus
                              ?.toUpperCase() ||
                            "UNKNOWN"
                          }
                        </strong>

                      </div>


                      <div>

                        <span className="label">
                          SERVICE
                        </span>

                        <strong>
                          {
                            resolution
                              .verification
                              ?.service ||
                            displayIncident
                              ?.service ||
                            "N/A"
                          }
                        </strong>

                      </div>


                      <div>

                        <span className="label">
                          RECOVERED
                        </span>

                        <strong>
                          {recovered
                            ? "YES"
                            : "NO"}
                        </strong>

                      </div>


                      <div>

                        <span className="label">
                          FINAL STATE
                        </span>

                        <strong>
                          {recovered
                            ? "HEALTHY"
                            : "UNRESOLVED"}
                        </strong>

                      </div>

                    </div>


                    <div
                      className="verification-result"
                      style={{
                        marginTop:
                          "25px",
                      }}
                    >

                      <strong>
                        {recovered
                          ? "✓ INCIDENT RECOVERED"
                          : "INCIDENT NOT RECOVERED"}
                      </strong>

                      <p>
                        {
                          resolution
                            .verification
                            ?.reason ||
                          "Verification completed."
                        }
                      </p>

                    </div>

                  </>

                ) : (

                  <p>
                    Verification result
                    unavailable.
                  </p>

                )}

              </section>

            )}


            {/* =================================================
                11 — AUDIT
            ================================================= */}

            {resolutionComplete && (

              <section
                className="panel"
                data-step="11"
              >

                <p className="eyebrow">
                  AUDITABILITY
                </p>

                <h2>
                  Audit Trail
                </h2>

                <p>
                  The complete incident
                  resolution decision and
                  execution result are
                  recorded for review.
                </p>


                <div className="audit-list">

                  <div className="audit-item">

                    <span>
                      01
                    </span>

                    <div>

                      <strong>
                        Incident detected
                      </strong>

                      <small>
                        {
                          displayIncident
                            ?.incident_id ||
                          "N/A"
                        }
                      </small>

                    </div>

                  </div>


                  <div className="audit-item">

                    <span>
                      02
                    </span>

                    <div>

                      <strong>
                        Alerts correlated
                      </strong>

                      <small>
                        {
                          displayIncident
                            ?.alerts
                            ?.length ||
                          0
                        } signals grouped
                        into one incident
                      </small>

                    </div>

                  </div>


                  <div className="audit-item">

                    <span>
                      03
                    </span>

                    <div>

                      <strong>
                        AI investigation
                        completed
                      </strong>

                      <small>
                        Root cause and
                        evidence recorded
                      </small>

                    </div>

                  </div>


                  <div className="audit-item">

                    <span>
                      04
                    </span>

                    <div>

                      <strong>
                        Remediation decision
                      </strong>

                      <small>
                        {
                          selectedAction
                            ?.action ||
                          "N/A"
                        }
                      </small>

                    </div>

                  </div>


                  <div className="audit-item">

                    <span>
                      05
                    </span>

                    <div>

                      <strong>
                        Action executed
                      </strong>

                      <small>
                        {
                          executionStatus
                            ?.toUpperCase() ||
                          "N/A"
                        }
                      </small>

                    </div>

                  </div>


                  <div className="audit-item">

                    <span>
                      06
                    </span>

                    <div>

                      <strong>
                        Recovery verified
                      </strong>

                      <small>
                        {recovered
                          ? "Service healthy"
                          : "Recovery not confirmed"}
                      </small>

                    </div>

                  </div>

                </div>


                {resolution
                  ?.ai_decision
                  ?.explanation && (

                  <div
                    className="incident-card"
                    style={{
                      marginTop:
                        "25px",
                    }}
                  >

                    <span className="label">
                      AI EXPLANATION
                    </span>

                    <p>
                      {
                        resolution
                          .ai_decision
                          .explanation
                      }
                    </p>

                  </div>

                )}

              </section>

            )}

          </div>

          <div className="fog"></div>

        </div>

      </div>


      {/* =====================================================
          ERROR
      ===================================================== */}

      {error && (

        <div
          className="error-banner"
          style={{
            position: "fixed",
            bottom: "20px",
            left: "50%",
            transform:
              "translateX(-50%)",
            zIndex: 1000,
            width:
              "min(600px, 90vw)",
          }}
        >
          {error}
        </div>

      )}

    </>
  );
}

export default Dashboard;