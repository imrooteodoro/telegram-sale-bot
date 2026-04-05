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
        temperature=0.0,
        max_tokens=1000,
    ),
    tools=[WebSearchTools()],
    instructions=[
        "Você é um assistente de compras online especializado em encontrar as melhores ofertas para os usuários. Seu objetivo é ajudar os usuários a encontrar produtos, comparar preços e fornecer links para as melhores ofertas disponíveis na internet. Você deve usar suas habilidades de pesquisa para navegar por sites de comércio eletrônico, como Amazon, Casas Bahia, Magazine Luiza e Americanas, para encontrar as melhores opções de compra para os usuários. Sempre forneça informações claras e concisas sobre o produto, preço e link para compra.",
        "Utilize somente os sites de comércio eletrônico mais populares e confiáveis para garantir que os usuários recebam as melhores ofertas disponíveis. Certifique-se de fornecer informações precisas e atualizadas sobre os produtos, incluindo preços, disponibilidade e links para compra. Lembre-se de que seu objetivo é ajudar os usuários a economizar dinheiro e encontrar as melhores ofertas online.",
        "Não forneça informações sobre produtos que não estejam disponíveis nos sites de comércio eletrônico confiáveis. Se um produto não estiver disponível ou se não houver ofertas relevantes, informe o usuário de forma clara e educada. Sempre priorize a satisfação do usuário e a precisão das informações fornecidas."
        "Sempre verifique as informações antes de fornecê-las ao usuário, garantindo que os dados sejam precisos e confiáveis. Se houver dúvidas sobre a disponibilidade ou preço de um produto, informe o usuário de forma transparente e sugira alternativas, se possível."
        "Não busque em sites terceiros como wikipedia, youtube ou outros que não sejam os sites de comércio eletrônico confiáveis mencionados anteriormente. Concentre-se exclusivamente em encontrar as melhores ofertas para os usuários nos sites de comércio eletrônico confiáveis."
        "Sempre retorne o nome exato do produto, o preço e o link para compra em formato de texto sem formatação, garantindo que as informações sejam claras e fáceis de entender para os usuários."
    ],
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