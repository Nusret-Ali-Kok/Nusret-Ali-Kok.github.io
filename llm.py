from openai import OpenAI

def API_call_chat(messages: list, api_key: str) -> str:
    """
    Calls Deepseek chat model via the OpenRouter API with a list of messages.

    Args:
        messages: List of messages in chat format, each dict with 'role' and 'content'.
        api_key: Your API key for OpenRouter.
    """
    if not api_key:
        raise Exception("OpenRouter API key not provided.")

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        completion = client.chat.completions.create(
            extra_headers={
              "HTTP-Referer": "<YOUR_SITE_URL>",
              "X-Title": "<YOUR_SITE_NAME>",
            },
            model="deepseek/deepseek-chat-v3-0324",
            messages=messages
        )

        return completion.choices[0].message.content

    except Exception as e:
        raise Exception(f"OpenRouter API call failed: {str(e)}")
