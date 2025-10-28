from browser_use import Tools, ActionResult, Browser, Agent, ChatGoogle
from dotenv import load_dotenv
import os
import asyncio  

load_dotenv()
tools = Tools()

os.environ["ANONYMIZED_TELEMETRY"] = "false"

print(tools)

@tools.action('Ask human for help with a question')
def ask_human(question: str, browser: Browser) -> ActionResult:
    print(f"Tool called with question: {question}")
    answer = input(f'{question} > ')
    return ActionResult(extracted_content=f'The human responded with: {answer}')

async def main():
    agent = Agent(
        llm = ChatGoogle(model="gemini-flash-latest"),
        task='You must use the ask_human function to ask the user what their favorite color is. Do not complete the task without calling ask_human.',
        tools=tools,
    )

    result = await agent.run()
    print("Final result:", result)

if __name__ == "__main__":
    asyncio.run(main())