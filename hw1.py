import asyncio
from connection import config
from agents import (
    Agent, Runner, InputGuardrailTripwireTriggered,
    input_guardrail, GuardrailFunctionOutput, trace
)

from dotenv import load_dotenv
load_dotenv()

@input_guardrail
async def class_change_guardrail(ctx, agent, input: str):
    if "change my class timings" in input.lower():
        return GuardrailFunctionOutput(
            output_info="Class timing change not allowed.",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info=input,
        tripwire_triggered=False
    )

student_agent = Agent(
    name="Student Agent",
    instructions="You are a helpful student assistant.",
    input_guardrails=[class_change_guardrail]
)

async def main():
    with trace("guardrail..."):
        try:
            result = await Runner.run(
                student_agent,
                "I dont want to change my class timings 😭😭",
                run_config=config
            )
            print("Allowed:", result.final_output)
            
        except InputGuardrailTripwireTriggered:
            print("Guardrail triggered: Class timing changes are not allowed.")

if __name__ == "__main__":
    asyncio.run(main())
