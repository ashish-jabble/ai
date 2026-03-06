"""
RAG Agent — Local AI Agent with Web Search & Context Retrieval

Uses Qwen3:8b via Ollama + DuckDuckGo search + web scraping
to answer questions with current, real-world information.

Pipeline:
  User prompt → Web Search → Retrieve articles → Extract content → Inject context → Qwen generates response
"""

import os
import textwrap

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

load_dotenv()

# ── Constants ──────────────────────────────────────────────────────

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:8b")
MAX_SEARCH_RESULTS = 5
MAX_ARTICLE_LENGTH = 3000  # chars per article to keep context manageable
REQUEST_TIMEOUT = 10

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


# ── Tools ──────────────────────────────────────────────────────────

@tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo and return top results.
    Use this tool to find current information about any topic — news, product launches,
    specs, pricing, events, people, companies, etc.

    Args:
        query: The search query string. Be specific for better results.

    Returns:
        A formatted string with search results including titles, URLs, and snippets.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=MAX_SEARCH_RESULTS))

        if not results:
            return f"No search results found for: {query}"

        output = f"Search results for: '{query}'\n{'=' * 50}\n\n"
        for i, r in enumerate(results, 1):
            output += f"{i}. {r['title']}\n"
            output += f"   URL: {r['href']}\n"
            output += f"   {r.get('body', 'No snippet available.')}\n\n"

        return output

    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def fetch_webpage(url: str) -> str:
    """
    Fetch and extract the main text content from a webpage URL.
    Use this tool AFTER web_search to read the full content of a specific article or page.
    This gives you detailed information beyond what the search snippet provides.

    Args:
        url: The full URL of the webpage to fetch (e.g., https://example.com/article).

    Returns:
        The extracted text content of the page, truncated to a reasonable length.
    """
    try:
        resp = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")

        # Remove noise elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]):
            tag.decompose()

        # Try to find main content
        main = soup.find("article") or soup.find("main") or soup.find("body")
        if not main:
            return "Could not extract content from this page."

        # Get text, clean up whitespace
        text = main.get_text(separator="\n", strip=True)

        # Remove excessive blank lines
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        text = "\n".join(lines)

        if len(text) > MAX_ARTICLE_LENGTH:
            text = text[:MAX_ARTICLE_LENGTH] + "\n\n[... content truncated for brevity ...]"

        return f"Content from: {url}\n{'=' * 50}\n\n{text}"

    except requests.exceptions.Timeout:
        return f"Timeout fetching {url} — the site took too long to respond."
    except requests.exceptions.HTTPError as e:
        return f"HTTP error fetching {url}: {e.response.status_code}"
    except Exception as e:
        return f"Failed to fetch {url}: {str(e)}"


# ── Agent Setup ────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful AI assistant with access to real-time web search and webpage reading tools.

Your workflow for answering questions:
1. ALWAYS use the web_search tool first to find current, relevant information
2. If you need more detail from a specific result, use fetch_webpage to read the full article
3. Synthesize the information you gathered and give a clear, well-structured response
4. Cite your sources — mention where the information came from

Important rules:
- Always search the web for current information before answering factual questions
- Don't make up facts — if you can't find the information, say so
- When creating marketing copy, ads, or content: search for real product specs, features, and announcements first
- Keep responses practical and actionable
"""

TOOLS = [web_search, fetch_webpage]


def create_rag_agent(model_name=MODEL_NAME, temperature=0.3):
    """Creates the RAG agent with web search tools and Qwen3 via Ollama."""

    print(f"Initializing Qwen3 ({model_name}) via Ollama...")
    llm = ChatOllama(
        model=model_name,
        temperature=temperature,
        num_ctx=8192,  # Larger context window for RAG
    )

    print("Creating RAG agent with tools: web_search, fetch_webpage")
    agent = create_agent(
        llm,
        TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )

    print("RAG Agent ready!\n")
    return agent


def run_query(agent, query):
    """Run a single query through the agent and print the response."""
    print(f"\n{'─' * 60}")
    print(f"📝 Query: {query}")
    print(f"{'─' * 60}\n")

    response = agent.invoke({"messages": [{"role": "user", "content": query}]})

    # Extract the final AI message
    messages = response.get("messages", [])
    if messages:
        final = messages[-1]
        print(f"🤖 Response:\n")
        # Word-wrap for terminal readability
        for line in final.content.split("\n"):
            if len(line) > 100:
                print(textwrap.fill(line, width=100))
            else:
                print(line)
    else:
        print("No response from agent.")

    print(f"\n{'─' * 60}\n")
    return response


def interactive_mode(agent):
    """Run the agent in interactive chat mode."""
    print("=" * 60)
    print("  RAG Agent — Interactive Mode")
    print("  Model: Qwen3:8b via Ollama")
    print("  Tools: Web Search, Page Reader")
    print("  Type 'quit' or 'exit' to stop")
    print("=" * 60)

    while True:
        try:
            query = input("\n🔍 You: ").strip()
            if not query:
                continue
            if query.lower() in ("quit", "exit", "q"):
                print("Bye!")
                break

            run_query(agent, query)

        except KeyboardInterrupt:
            print("\nBye!")
            break


# ── Main ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    agent = create_rag_agent()

    # If arguments passed, run them as queries
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        run_query(agent, query)
    else:
        # Demo queries, then drop into interactive mode
        print("Running demo queries...\n")

        run_query(agent, "Create Google Ads copy for the latest iPhone launch. Include key specs and features.")

        # run_query(agent, "What are the top trending AI tools in March 2026? Give me a brief summary of each.")

        # Drop into interactive mode
        interactive_mode(agent)
