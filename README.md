# 🤖 Autonomous Enterprise Incident Resolution Engine

An AI-powered incident management system that detects, correlates, investigates, decides, remediates, and verifies enterprise incidents autonomously.

## 🚀 Overview

Modern enterprise systems generate large volumes of operational alerts from applications, infrastructure, databases, services, and business systems.

Multiple alerts can represent different symptoms of the same underlying incident. Manually investigating these incidents can be slow and error-prone.

This project demonstrates an autonomous AI workflow that goes beyond simply displaying alerts:

**Detection → Correlation → Investigation → Decision → Remediation → Verification → Audit**

## 🎯 Key Features

- 🔍 **Automated Detection** — Collects service health, logs, metrics, and operational alerts.
- 🔗 **Alert Correlation** — Groups related alerts into a single incident.
- 🧠 **AI Investigation** — Analyzes evidence to identify the probable root cause.
- ⚖️ **Dynamic Decision Making** — Evaluates remediation options based on incident evidence.
- 🛠️ **Controlled Remediation** — Executes only actions registered in the Action Registry.
- 🤖 **Autonomous Execution** — Supports autonomous actions where permitted.
- 👤 **Human Approval** — Supports actions requiring human intervention.
- ✅ **Verification** — Checks whether the affected service actually recovered.
- 📋 **Audit Trail** — Records incident, decision, execution, and verification details.
- 🗄️ **Persistent Storage** — Uses MySQL for incident-resolution records.
- 🔒 **Local AI** — Uses Ollama and Qwen3 for local AI inference.

## 🧠 Core Workflow

```text
Operational Signals
        ↓
    Detection
        ↓
   Correlation
        ↓
 Incident Formation
        ↓
    Investigation
        ↓
   AI Decision
        ↓
 Remediation Planning
        ↓
     Execution
        ↓
    Verification
        ↓
      Audit

🏗️ Architecture

┌─────────────────────────┐
│    React Dashboard      │
│    Incident Console     │
└────────────┬────────────┘
             │ REST / JSON
             ▼
┌─────────────────────────┐
│      FastAPI Backend    │
└────────────┬────────────┘
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
 Monitoring Correlation Prioritization
     │       │        │
     └───────┼────────┘
             ▼
┌─────────────────────────┐
│       AI Brain          │
│ Investigation + Decision│
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│      Ollama + Qwen3     │
│       Local AI          │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Action Planner +        │
│ Action Registry         │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Remediation Executor    │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Enterprise Simulator    │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ Verification + Audit    │
└─────────────────────────┘

🛠️ Technology Stack
Frontend :-

React
TypeScript
Vite
CSS

Backend:-

Python
FastAPI
Pydantic
HTTPX

AI:-

Ollama
Qwen3

Machine Learning:-

Scikit-learn
DBSCAN
ONNX
ONNX Runtime

Database:-
MySQL

Communication:-
REST API
JSON

Infrastructure Simulation:-
Python
FastAPI

Public Demonstration:-
Cloudflare Tunnel


