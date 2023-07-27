import pytest

from analyze_webpage_content.analyze_webpage_content import AnalyzeWebpageContent


def mock_llm(text_in: str):
    return text_in.upper()


async def mock_allm(text_in: str):
    return text_in.upper()


def test_analyze_webpage_content_sync_no_question():
    pack = AnalyzeWebpageContent(llm=mock_llm)
    results = pack.run(url="https://www.bbc.com/news")
    assert "SPECIFIC QUESTION" not in results
    assert "PROVIDE A SUMMARY" in results
    assert "BBC" in results


def test_analyze_webpage_content_sync_question():
    pack = AnalyzeWebpageContent(llm=mock_llm)
    results = pack.run(
        url="https://www.bbc.com/news", question="What are the top headlines?"
    )
    assert "SPECIFIC QUESTION" in results
    assert "BBC" in results


@pytest.mark.asyncio
async def test_analyze_webpage_content_async_no_question():
    pack = AnalyzeWebpageContent(allm=mock_allm)
    results = await pack.arun(url="https://www.bbc.com/news")
    assert "SPECIFIC QUESTION" not in results
    assert "PROVIDE A SUMMARY" in results
    assert "BBC" in results


@pytest.mark.asyncio
async def test_analyze_webpage_content_async_question():
    pack = AnalyzeWebpageContent(allm=mock_allm)
    results = await pack.arun(
        url="https://www.bbc.com/news", question="What are the top headlines?"
    )
    assert "SPECIFIC QUESTION" in results
    assert "BBC" in results
