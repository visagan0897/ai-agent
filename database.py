import json
from datetime import datetime
from typing import Any

import mysql.connector
from mysql.connector import Error

from models.incidents import Incident


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "suryakeerthana95",
    "database": "incident_resolution",
}


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

    except Error as error:
        raise RuntimeError(
            f"MySQL connection failed: {error}"
        ) from error

    raise RuntimeError("MySQL connection failed.")


def save_incident(incident: Incident) -> None:
    connection = get_connection()

    cursor = None

    try:
        cursor = connection.cursor()

        incident_query = """
        INSERT INTO incidents (
            incident_id,
            created_at,
            service,
            description,
            cluster_id,
            logs,
            metrics,
            recent_changes,
            dependencies,
            system_state
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            service = VALUES(service),
            description = VALUES(description),
            cluster_id = VALUES(cluster_id),
            logs = VALUES(logs),
            metrics = VALUES(metrics),
            recent_changes = VALUES(recent_changes),
            dependencies = VALUES(dependencies),
            system_state = VALUES(system_state)
        """

        cursor.execute(
            incident_query,
            (
                incident.incident_id,
                incident.created_at.replace(tzinfo=None),
                incident.service,
                incident.description,
                incident.cluster_id,
                json.dumps(incident.logs),
                json.dumps(incident.metrics),
                json.dumps(incident.recent_changes),
                json.dumps(incident.dependencies),
                json.dumps(incident.system_state),
            ),
        )

        alert_query = """
        INSERT INTO alerts (
            alert_id,
            incident_id,
            timestamp,
            source,
            service,
            original_message,
            normalized_message,
            alert_type,
            severity,
            metadata
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            incident_id = VALUES(incident_id),
            timestamp = VALUES(timestamp),
            source = VALUES(source),
            service = VALUES(service),
            original_message = VALUES(original_message),
            normalized_message = VALUES(normalized_message),
            alert_type = VALUES(alert_type),
            severity = VALUES(severity),
            metadata = VALUES(metadata)
        """

        for alert in incident.alerts:
            cursor.execute(
                alert_query,
                (
                    alert.alert_id,
                    incident.incident_id,
                    alert.timestamp.replace(tzinfo=None),
                    alert.source,
                    alert.service,
                    alert.original_message,
                    alert.normalized_message,
                    alert.alert_type,
                    alert.severity,
                    json.dumps(alert.metadata),
                ),
            )

        connection.commit()

    except Error as error:
        connection.rollback()
        raise RuntimeError(
            f"Failed to save incident to MySQL: {error}"
        ) from error

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def save_resolution(
    incident_id: str,
    ai_decision: dict[str, Any],
    execution_result: dict[str, Any],
    verification_result: dict[str, Any],
) -> None:

    connection = get_connection()

    cursor = None

    try:
        cursor = connection.cursor()

        root_cause = ai_decision.get("root_cause", {})
        selected_action = ai_decision.get("selected_action", {})

        query = """
        INSERT INTO resolutions (
            incident_id,
            root_cause,
            confidence,
            evidence,
            severity,
            business_impact,
            possible_actions,
            selected_action_id,
            selected_action,
            execution_mode,
            explanation,
            execution_status,
            verification_status,
            created_at
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """

        cursor.execute(
            query,
            (
                incident_id,
                root_cause.get("description"),
                root_cause.get("confidence"),
                json.dumps(ai_decision.get("evidence", [])),
                ai_decision.get("severity"),
                ai_decision.get("business_impact"),
                json.dumps(ai_decision.get("possible_actions", [])),
                selected_action.get("action_id"),
                selected_action.get("action"),
                ai_decision.get("execution_mode"),
                ai_decision.get("explanation"),
                execution_result.get("status"),
                verification_result.get("status"),
                datetime.now(),
            ),
        )

        connection.commit()

    except Error as error:
        connection.rollback()
        raise RuntimeError(
            f"Failed to save resolution to MySQL: {error}"
        ) from error

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()