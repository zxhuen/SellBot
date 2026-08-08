from app.ai.providers.gemini import client


async def chat_generate(content: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=content
    )

    return response.text
