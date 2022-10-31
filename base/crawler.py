import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0


class crawler:
    def __init__(self):
        self.internal_urls = set()
        self.external_urls = set()
        self.total_urls_visited = 0

    def is_valid(self, url):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_all_website_links(self, url):
        """
        Returns all URLs that is found on `url` in which it belongs to the same website
        """
        # all URLs of `url`
        urls = set()
        # domain name of the URL without the protocol
        domain_name = urlparse(url).netloc

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'}

        soup = BeautifulSoup(requests.get(url, headers=headers, verify=False).content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue
            # join the URL if it's relative (not absolute link)
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not self.is_valid(href):
                # not a valid URL
                continue
            if "mailto://" in href:
                continue
            if href in self.internal_urls or href.split(".")[-1] in ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "pdf",
                                                                     "PDF", "gif", "GIF","tiff", "TIFF", "svg", "SVG"]:
                # already in the set
                continue
            if domain_name not in href:
                # external link
                if href not in self.external_urls:
                    print(f"{GRAY}[!] External link: {href}{RESET}")
                    self.external_urls.add(href)
                continue
            print(f"{GREEN}[*] Internal link: {href}{RESET}")
            urls.add(href)
            self.internal_urls.add(href)
        return urls

    def crawl(self, url, max_urls=50):
        """
        Crawls a web page and extracts all links.
        You'll find all links in `external_urls` and `internal_urls` global set variables.
        params:
            max_urls (int): number of max urls to crawl, default is 30.
        """

        global total_urls_visited
        total_urls_visited += 1
        links = self.get_all_website_links(url)
        for link in links:

            if total_urls_visited > max_urls:
                break
            self.crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    import argparse

    # parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    # parser.add_argument("url", help="The URL to extract links from.")
    # parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)

    # args = parser.parse_args()
    url = "https://mcs.nust.edu.pk/"  # args.url
    max_urls = 30  # args.max_urls

    crawler.crawl(url)  # , max_urls=max_urls)

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))

    domain_name = urlparse(url).netloc

    # save the internal links to a file
    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    # save the external links to a file
    with open(f"{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)

