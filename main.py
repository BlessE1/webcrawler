import asyncio
import sys
from crawl import crawl_site_async
from json_report import write_json_report

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    max_concurrency = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    print(f"starting crawl of: {base_url}")

    try:
        page_data = await crawl_site_async(base_url, max_concurrency, max_pages)
        # print("\nCrawled Page Data:")

        # for url, data in page_data.items():
        #     print(f"URL: {url}")
        #     print(f"Heading: {data['heading']}")
        #     #print(f"First Paragraph: {data['first_paragraph']}")
        #     #print(f"Outgoing Links: {data['outgoing_links']}")
        #     #print(f"Image URLs: {data['image_urls']}")
        #     print("-" * 50)

        print(f"Crawled {len(page_data)} pages from {base_url}")

        write_json_report(page_data)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    


if __name__ == "__main__":
    asyncio.run(main())