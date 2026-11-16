import _local # noqa: F401
from agents import Agent, Runner

#Dedine a consistent production outage scenario as the controlled input
INCIDENT_QUERY = (
    "Productioin Alert: API Gateway p99 latency spiked to 4500ms. "
    "Nginx error logs show repeated 'ipstream timed out (110: Connection timed out)'. "
    "All 3 downstream auth-service pods have CPU spinned at 99%. "
    "What should I do immediately?"
)

# 1. Weak Prompt: vague, single-sentence, zero operational guardrails
weak_agent = Agent(
    name = "WeakOpsAssistant",
    instructions = "You are a DevOps assistant. Help the user fix server issues.",
)

#2. Five-Block Structural Prompt: Role, Capabilities, Boundaries, Style, Format
STRUCTURED_INSTRUCTIONS = """
1. Role: You are OpsSentinel, a Principal Site Reliability Engineer (SRE) specializing in high-concurrency microservice triage.
2. Capabilities: You diagnose CPU saturation, thread contention, and upstream connection timeout using hypothesis-driven analysis.
3. Boundaries: STRICTLY FORBIDDEN to recommend restarting pods, killing processes, or modifying configs before collecting diagnostic dumps.
4. Style: Objective, analytical, concise, and strictly non-hallucinatory.
5. Format: Output strictly in four sections:
    - [Severity Level]
    - [Root Cause Hypotheses]
    - [Read-Only Inspection Commands]
    - [Safe Mitigation Next Steps]
"""

structured_agent = Agent(
    name = "OpsSentinel",
    instructions = STRUCTURED_INSTRUCTIONS,
)

def main() -> None:
    print("="*65)
    print("EXPERIMENT: Weak Prompt vs. Five-Block Structural Prompt")
    print("="*65)

    print("\n>>> [1] WEAK PROMPT OUTPUT:\n")
    weak_result = Runner.run_sync(weak_agent, INCIDENT_QUERY)
    print(weak_result.final_output)

    print("\n"+"="*65)

    print("\n>>> [2] FIVE-BLOCK STRUCTURAL PROMPT OUTPUT:\n")
    structured_result = Runner.run_sync(structured_agent, INCIDENT_QUERY)
    print(structured_result.final_output)


if __name__ == "__main__":
    main()
