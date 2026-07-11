import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def ask_llm(system_prompt: str, user_text: str, model: str = "openrouter/free") -> str:
    """
    Shared helper function to call OpenRouter.
    Uses 'openrouter/free' to automatically route to an active free model.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenRouter: {str(e)}"

# Quick test
if __name__ == "__main__":
    print("Testing OpenRouter connection with openrouter.....")
    test_response = ask_llm(
        system_prompt="You are a helpful cybersecurity assistant.",
        user_text="Say 'RakshaSootra AI LLM Client is online and working!'"
    )
    print(f"Response: {test_response}")
