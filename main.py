import sys
from crawl import crawl_page

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")

    try:
        page_data = crawl_page(base_url, base_url)
        print("\nCrawled Page Data:")

        for url, data in page_data.items():
            print(f"URL: {url}")
            print(f"Heading: {data['heading']}")
            #print(f"First Paragraph: {data['first_paragraph']}")
            #print(f"Outgoing Links: {data['outgoing_links']}")
            #print(f"Image URLs: {data['image_urls']}")
            print("-" * 50)

        print(f"Crawled {len(page_data)} pages from {base_url}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
