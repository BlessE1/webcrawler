import requests
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
from time import sleep
import asyncio
import aiohttp

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

class AsyncCrawler():
    def __init__(self, base_url: str, max_concurrency: int, max_pages: int):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.visited: set[str] = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session: aiohttp.ClientSession | None = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks: set[asyncio.Task] = set()

    # Open and close the aiohttp session using async context manager
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()

    async def add_page_visit(self, normalised_url: str):
        if self.should_stop:
            return False

        #print(len(self.visited))
        if len(self.visited) >= self.max_pages:
            self.should_stop = True
            print(f"Reached maximum number of pages to crawl")
            await asyncio.gather(*[task for task in self.all_tasks if task != asyncio.current_task()], return_exceptions=True)  # Wait for all tasks to finish
            return False
        
        async with self.lock:
            if normalised_url in self.visited:
                return False
            
            self.visited.add(normalised_url)
            return True

    async def get_html(self, url: str) -> str:
        #print(f"Fetching HTML for: {url}")
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
            if response.status >= 400:
                raise Exception(f"Failed to fetch {url}: {response.status} {response.reason}") 
            elif not response.headers.get("Content-Type", "").startswith("text/html"):
                raise Exception(f"Unexpected content type for {url}: {response.headers.get('Content-Type', '')}")
            elif not await response.text():
                raise Exception(f"Empty response for {url}")

            #print(f"Successfully fetched {url} with status {response.status}")
            return await response.text() 

    async def crawl_page(self, base_url: str, current_url: str = "", page_data: dict[str, PageData] = {}) -> dict[str, PageData]:
        #print(f"Crawling: {current_url}")
        #await asyncio.sleep(1)  # Delay to avoid overwhelming the server
        if self.should_stop:
            return page_data
        
        if base_url not in current_url:
            #print(f"Skipping external link: {current_url}")
            return page_data

        if not current_url:
            current_url = base_url

        new_page = await self.add_page_visit(normalize_url(current_url))
        if not new_page:
            #print(f"Already visited: {current_url}")
            return page_data

        async with self.semaphore:
            #print(f"Fetching: {current_url}")
            try:
                html = await self.get_html(current_url)
                #print(f"Fetched: {current_url}")
            except Exception as e:
                #print(f"Error fetching {current_url}: {e}")
                return page_data

            async with self.lock:
                page_data[normalize_url(current_url)] = extract_page_data(html, current_url)

            tasks = []
            for link in page_data[normalize_url(current_url)]["outgoing_links"]:
                #print(f"Found link: {link}")
                task = asyncio.create_task(self.crawl_page(base_url, link, page_data))
                self.all_tasks.add(task)
                tasks.append(task)
                task.add_done_callback(self.all_tasks.discard)

            await asyncio.gather(*tasks)

            return page_data

    async def crawl(self) -> dict[str, PageData]:
        return await self.crawl_page(self.base_url, self.base_url, self.page_data)

async def crawl_site_async(base_url: str, max_concurrency: int, max_pages: int) -> dict[str, PageData]:
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()

def normalize_url(url: str) -> str:
    if not url:
        return ""

    parsed = urlsplit(url)

    return f"{parsed.netloc}{parsed.path}".rstrip("/")

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1_tag: Tag = soup.find("h1")
    h2_tag: Tag = soup.find("h2")

    if h1_tag:
        return h1_tag.get_text(strip=True)

    if h2_tag:
        return h2_tag.get_text(strip=True)

    return ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main_tag: Tag = soup.find("main")

    # Search for the first <p> tag within the <main> tag if it exists
    if main_tag:
        main_p_tag: Tag = main_tag.find("p")
        if main_p_tag:
            return main_p_tag.get_text(strip=True)

    # Fallback to just the first <p> tag
    p_tag: Tag = soup.find("p")
    if p_tag:
        return p_tag.get_text(strip=True)

    return ""

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("http://") or href.startswith("https://"):
            urls.append(href)
        else:
            # Handle relative URLs
            urls.append(urljoin(base_url, href))

    return urls

def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    images = []

    for img_tag in soup.find_all("img", src=True):
        src = img_tag["src"]
        if src.startswith("http://") or src.startswith("https://"):
            images.append(src)
        else:
            # Handle relative URLs
            images.append(urljoin(base_url, src))

    return images

def extract_page_data(html: str, page_url: str) -> PageData:
    return PageData(
        url=page_url,
        heading=get_heading_from_html(html),
        first_paragraph=get_first_paragraph_from_html(html),
        outgoing_links=get_urls_from_html(html, page_url),
        image_urls=get_images_from_html(html, page_url),
    )

