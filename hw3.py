from connection import config
import asyncio
from agents import (
    Agent,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    Runner
)

@input_guardrail
def gatekeeper_guardrail(ctx, agent, input):
    if "ABC School" not in input:
        return GuardrailFunctionOutput(
            output_info="Student is from another school.",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(
        output_info="Student is from ABC School.",
        tripwire_triggered=False
    )


gatekeeper_agent = Agent(
    name="Gate Keeper Agent",
    instructions="You are a strict gatekeeper. Only allow students from ABC School.",
    input_guardrails=[gatekeeper_guardrail]
)


async def main():
    try:
        result = await Runner.run(
            gatekeeper_agent,
            "Hi, I'm a student from XYZ School.",
            run_config=config
        )
        print("Student is allowed to enter.")
    except InputGuardrailTripwireTriggered:
        print("Gate Keeper: Access denied. You're not from ABC School!")

if __name__ == "__main__":
    asyncio.run(main())
