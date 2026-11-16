import _local 
from agents import Agent, Runner, SQLiteSession
# Define SRE triage system instructions
SRE_INSTRUCTIONS = """
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
            
            