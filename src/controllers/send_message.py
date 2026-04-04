from src.services.genai_service import is_product_query, search_product


async def process_user_message(user_message: str) -> str:
    if not is_product_query(user_message):
        return "Eu respondo apenas sobre produtos e ofertas. Envie o nome de um produto para eu buscar as melhores opções."

    return await search_product(user_message)