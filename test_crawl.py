import unittest
from crawl import extract_page_data, normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html 


class TestCrawl(unittest.TestCase):
    # Expected test cases for the normalize_url function
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_1(self):
            input_url = "https://www.boot.dev/blog/path/"
            actual = normalize_url(input_url)
            expected = "www.boot.dev/blog/path"
            self.assertEqual(actual, expected)

    def test_normalize_url_2(self):
            input_url = "https://www.boots.dev/blog/path"
            actual = normalize_url(input_url)
            expected = "www.boots.dev/blog/path"
            self.assertEqual(actual, expected)

    def test_normalize_url_3(self):
            input_url = "http://www.bot.dev/blog/path/"
            actual = normalize_url(input_url)
            expected = "www.bot.dev/blog/path"
            self.assertEqual(actual, expected)

    def test_normalize_url_4(self):
            input_url = "http://www.bots.dev/blog/path"
            actual = normalize_url(input_url)
            expected = "www.bots.dev/blog/path"
            self.assertEqual(actual, expected)

    # Edge cases for the normalize_url function
    def test_normalize_url_5(self):
            input_url = ""
            actual = normalize_url(input_url)
            expected = ""
            self.assertEqual(actual, expected)

    def test_normalize_url_6(self):
            input_url = "https://www.boot.dev/blog/path?query=param"
            actual = normalize_url(input_url)
            expected = "www.boot.dev/blog/path"
            self.assertEqual(actual, expected)

    # Expected test cases for the get_heading_from_html and get_first_paragraph_from_html functions

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self):
        input_body = "<html><body><h2>Test Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = """<html><body>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)

    # Test cases for get_urls_from_html
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/"><span>Boot.dev</span></a><a href="/about"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/", "https://crawler-test.com/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_links(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><span>Boot.dev</span></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    # Test cases for get_images_from_html
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><span>Boot.dev</span></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_with_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="image1.jpg"><img src="image2.png"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/image1.jpg", "https://crawler-test.com/image2.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_with_absolute_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://example.com/image1.jpg"><img src="https://example.com/image2.png"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://example.com/image1.jpg", "https://example.com/image2.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_with_relative_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/image1.jpg"><img src="/image2.png"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/image1.jpg", "https://crawler-test.com/image2.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_with_mixed_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://example.com/image1.jpg"><img src="/image2.png"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://example.com/image1.jpg", "https://crawler-test.com/image2.png"]
        self.assertEqual(actual, expected)

    # Test cases for extract_page_data
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_heading(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_paragraph(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_links(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_empty_html(self):
        input_url = "https://crawler-test.com"
        input_body = ""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_main_paragraph(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <main></main>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)
        
if __name__ == "__main__":
    unittest.main()