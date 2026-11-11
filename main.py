import _local 
from agents import Agent, Runner, SQLiteSession
# Define SRE triage system instructions
SRE_INSTRUCTIONS = """You are OpsSentinel, an automated Site Reliability Engineer (SRE) incident triage agnet.
Your mission is to help on-call engineers diagnose productioin issues, analyze anomalous logs. and inspect infrastructure failures.

Core Workflow:
1. Identify the impacted service, status code, and failure symptoms from the user's description.
2. Formulate diagnostic hypotheses based on distributed systems failure modes, like database pool exhaustion, thread starvation, CPU throttling, network latency.
3. Recommend non-destructive inspection commands to verify assumptions. 

Safety Red Lines:
- NEVER recommend destructive actions like dropping database tables, rm -rf, blind container restart.
- Prioritize observability and triage: ask for metrics, thread dumps, or error logs before jumping to remediation. 
"""

agent = Agent(name="OpsSentinel", instructions=SRE_INSTRUCTIONS)

# Instantiate concrete SQLiteSession for conversation persistence
session = SQLiteSession("ops_sentinel_triage")

def main():
    print("=== OpsSentinel Incident Triage Console ===")
    print("Agent online. Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("Operator: ").strip()
            # if the user directly presses the Enter key, skip this loop
            # and wait for input again, which avoids wasting a token of the LLM for an empty input.
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Triage session terminated.")
                break
            # Execute Agent Loop with conversation state injected 
            result = Runner.run_sync(agent, user_input, session=session)
            print(f"\nOpsSentinel: {result.final_output}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nTriage session terminated.")
            break
        
if __name__ == "__main__":
    main()
            
            