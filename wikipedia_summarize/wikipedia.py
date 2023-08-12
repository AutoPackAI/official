import asyncio
import wikipedia
from autopack import Pack
from autopack.utils import call_llm, acall_llm
from pydantic import BaseModel, Field
from wikipedia import WikipediaPage

PACK_DESCRIPTION = (
    "Searches Wikipedia based on a query and then analyzes the results. If a question is given, the analysis is based "
    "on that question. Otherwise, a general summary is provided. Enables quick access to factual knowledge. Useful "
    "for when you need to answer general questions about people, places, companies, facts, historical events, "
    "or other subjects."
)

PROMPT_TEMPLATE = """Given the following pages from Wikipedia, provide a detailed answer to the following question:

Question: {question}

Pages:
{pages}
"""


class WikipediaArgs(BaseModel):
    query: str = Field(
        ...,
        description="A search query to pull up pages which may include the answer to your question",
    )
    question: str = Field(
        description="The question you wish to answer, posed in the form of a question",
        default="Provide me with a detailed summary of the pages below.",
    )


def fetch_page(page_title: str) -> WikipediaPage:
    return wikipedia.page(page_title)


async def get_page(page_title: str) -> WikipediaPage:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch_page, page_title)


async def get_pages(query: str) -> str:
    page_titles = wikipedia.search(query, results=5)
    pages = await asyncio.gather(*(get_page(title) for title in page_titles))

    result = []
    for page in pages:
        result.append(f"-- Page: {page.title}\n{page.summary}")

    return "\n".join(result)


class WikipediaPack(Pack):
    name = "wikipedia"
    description = PACK_DESCRIPTION
    args_schema = WikipediaArgs
    dependencies = ["wikipedia"]
    categories = ["Information"]

    def _run(
        self,
        query: str,
        question: str = "Provide me with a general summary of the pages below.",
    ) -> list[str]:
        try:
            prompt = PROMPT_TEMPLATE.format(question=question, pages=get_pages(query))
            response = call_llm(prompt, self.llm)
            return response
        except Exception as e:
            return f"Error: {e}"

    async def _arun(
        self,
        query: str,
        question: str = "Provide me with a detailed summary of the pages below.",
    ):
        try:
            pages = await get_pages(query)
            prompt = PROMPT_TEMPLATE.format(question=question, pages=pages)
            response = await acall_llm(prompt, self.allm)
            return response
        except Exception as e:
            return f"Error: {e}"
