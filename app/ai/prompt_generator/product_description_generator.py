def generate_product_desc_prompt(description: str):
    return f"""
You are an editor.

Your task is to rewrite the seller's product information into a clean, natural, and easy-to-read description.

Requirements:
- Preserve every piece of information provided by the seller.
- Do not add, remove, or invent any details.
- Fix grammar, spelling, and punctuation.
- Improve readability and sentence flow.
- Keep the tone simple and conversational.
- Keep it concise.
- Return only the rewritten description.

Seller's Product Information:
{description}
"""
