import os

from agno import tools
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.tools.jina import JinaReaderTools
# from agno.tools.website import WebsiteTools
from agno.tools.websearch import WebSearchTools

load_dotenv()

mistral_api_key = os.getenv("GENAI_API_KEY")

agent = Agent(
    model=MistralChat(
        id="mistral-large-latest",
        api_key=mistral_api_key,
    ),
    tools=[WebSearchTools()],
    markdown=True
)

product = input("Digite o produto que deseja buscar: ")

agent.print_response(f"""
                    Navegue pelos sites e busque  por {product} e me traga as melhores ofertas.
                    https://www.casasbahia.com.br/
                    https://www.amazon.com.br/
                    https://www.magazineluiza.com.br/
                    https://www.americanas.com.br/
                    Traga nome do produto/marca, preço e link para compra em uma tabela.
                    
                     """)