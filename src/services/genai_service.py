import asyncio
from src.config.variables_config import GENAI_API_KEY

from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.tools.websearch import WebSearchTools
from dotenv import load_dotenv

agent = Agent(
    model=MistralChat(
        id="mistral-large-latest",
        api_key=GENAI_API_KEY,
    ),
    tools=[WebSearchTools()],
    markdown=False,
)

PRODUCT_KEYWORDS = (
    "produto",
    "produtos",
    "oferta",
    "ofertas",
    "preco",
    "preço",
    "comprar",
    "compra",
    "marca",
    "amazon",
    "magalu",
    "casas bahia",
    "americanas",
    "tvs",
    "celulares",
    "notebooks",
    "smartphones",
    "geladeiras",
    "fogões",
    "eletrodomésticos",
    "teclados",
    "mouses",
    "fones de ouvido",
    "headphones",
    "smartwatches",
    "monitores"
)


def is_product_query(message: str) -> bool:
    normalized_message = message.strip().lower()
    if not normalized_message:
        return False

    return any(keyword in normalized_message for keyword in PRODUCT_KEYWORDS)


def _extract_response_text(response: object) -> str:
    if response is None:
        return "Não foi possível gerar uma resposta no momento."

    if isinstance(response, str):
        return response.strip()

    for attribute_name in ("content", "text", "response", "output"):
        value = getattr(response, attribute_name, None)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return str(response).strip()


async def search_product(product: str) -> str:
    query = product.strip()

    if not query:
        return "Informe o produto que deseja pesquisar."

    response = await asyncio.to_thread(
        agent.run,
        f"""
        Navegue pelos sites e busque por {query} e me traga as melhores ofertas.
        https://www.casasbahia.com.br/
        https://www.amazon.com.br/
        https://www.magazineluiza.com.br/
        https://www.americanas.com.br/
        

        Retorne o nome do produto/marca, preço e link para compra em formato de texto sem formatação.
        """
    )
    return _extract_response_text(response)