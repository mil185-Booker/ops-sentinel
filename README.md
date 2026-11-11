# OpsSentinel

An automated Site Reliability Engineering (SRE) incident triage agent built using the OpenAI Agents SDK.

## Overview
OpsSentinel assists on-call engineers during production outages by:
- Analyzing anomalous HTTP telemetry, latency spikes, and log traces.
- Hypothesizing distributed system failure modes (connection pool exhaustion, thread starvation, CPU throttling).
- Providing non-destructive, read-only diagnostic commands.

## Getting Started
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export LOCAL_MODEL="qwen2.5:14b"
python main.py
