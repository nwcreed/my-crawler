import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

async def main():
    # Configure a 2-level deep crawl
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            max_pages=5,
            include_external=False
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )
    

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun("https://www.firecrawl.dev/", config=config)

        print(f"Crawled {len(results)} pages in total")

        # Access individual results
        for result in results[:5]:  # Show first 3 results
            print(f"URL: {result.url}")
            print(f"Depth: {result.metadata.get('depth', 0)}")

            # Display the content in markdown format
            print("\nMarkdown content:\n")
            print(result.markdown)  # Afficher le contenu en Markdown

if __name__ == "__main__":
    asyncio.run(main())
