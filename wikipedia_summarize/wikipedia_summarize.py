from autopack import Pack
from autopack.utils import call_llm, acall_llm
from langchain import WikipediaAPIWrapper
from pydantic import BaseModel, Field

PACK_DESCRIPTION = (
    "Retrieve information from Wikipedia based on a given search query and question. It provides a summary of the "
    "relevant Wikipedia page based on a given question, enabling quick access to factual knowledge.Useful for when "
    "you need to answer general questions about people, places, companies, facts, historical events, or other subjects."
)

PROMPT_TEMPLATE = """Given the following pages from Wikipedia, provide an answer to the following question:

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
        ...,
        description="The question you wish to answer, posed in the form of a question",
    )


def get_pages(query: str) -> str:
    page_text = []

    for page in WikipediaAPIWrapper().load(query):
        title = page.metadata.get("title", "Unknown title")
        # Assuming we don't want the summary? Returning just the summary is probably another tool
        page_text.append(f"-- Page: {title}\n{page.page_content}")

    return "\n".join(page_text)


class WikipediaPack(Pack):
    name = "wikipedia_summarize"
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
        question: str = "Provide me with a general summary of the pages below.",
    ):
        try:
            prompt = PROMPT_TEMPLATE.format(question=question, pages=get_pages(query))
            response = await acall_llm(prompt, self.allm or self.llm)
            return response
        except Exception as e:
            return f"Error: {e}"
