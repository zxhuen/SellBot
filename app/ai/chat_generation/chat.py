from app.ai.providers.gemini import client


async def product_description_gemini_response(content: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=content
    )

    print(response.text)
    return response.text
