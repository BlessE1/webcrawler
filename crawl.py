import requests
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

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

def extract_page_data(html: str, page_url: str) -> dict[str, str | list[str] ]:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }

def get_html(url: str) -> str | Exception:
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if response.status_code >= 400:
        raise Exception(f"Failed to fetch {url}: {response.status_code} {response.reason}") 
    elif not response.headers.get("Content-Type", "").startswith("text/html"):
        raise Exception(f"Unexpected content type for {url}: {response.headers.get('Content-Type', '')}")
    elif not response.text:
        raise Exception(f"Empty response for {url}")
    return response.text