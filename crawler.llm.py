from dotenv import load_dotenv
import os, asyncio, json
from pydantic import BaseModel
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

load_dotenv()

async def main():
    llm_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="gemini/gemini-2.0-flash",  # ✅ le vrai provider ici
            api_token=os.getenv("GEMINI_API_KEY")
        ),
        schema=None,  # Aucune structuration de schéma explicite
        extraction_type="schema",  # Vous gardez "schema" pour le type d'extraction
        instruction="Extract a list of all the features offered on this page. For each feature",  # Demander à l'IA de structurer les données
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        input_format="markdown",
        extra_args={
            "temperature": 0.0,
            "max_tokens": 800,
        }
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS
    )

    browser_cfg = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url="https://www.waalaxy.com/",
            config=crawl_config
        )

        if result.success:
            print("Extracted items:", json.loads(result.extracted_content))
            llm_strategy.show_usage()
        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())
