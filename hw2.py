from connection import config
import asyncio
from agents import (
    Agent, trace,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    Runner
)

son_agent = Agent(
    name="Son Agent",
    instructions="You are a child who wants to run around."
)

@input_guardrail
def father_guardrail(ctx, agent, input: str):
    if "26" in input or "25" in input or "24" in input:
        return GuardrailFunctionOutput(
            output_info="Too cold!",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(
        output_info="Temperature okay.",
        tripwire_triggered=False
    )


father_agent = Agent(
    name="Father Agent",
    instructions="You are a strict father. Don't allow running below 27°C.",
    input_guardrails=[father_guardrail]
)


async def main():
    try:
        result = await Runner.run(father_agent, "I want to run. AC is at 26C", run_config=config)
        print("Son is allowed to run.")
        
    except InputGuardrailTripwireTriggered:
            print("Father stopped the son. AC is too cold!")

if __name__ == "__main__":
    asyncio.run(main())
