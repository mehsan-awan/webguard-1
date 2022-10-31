import requests
from threading import Thread, Lock
from queue import Queue

from .OrignalData2 import getFullSiteNameWithHTTP
from . crawler import crawler
q = Queue()
list_lock = Lock()
# discovered_domains = []


class SubDomains:
    def __init__(self):
        self.discovered_domains = []

    def scan_subdomains(self, domain):
        global q
        while True:
            # get the subdomain from the queue
            subdomain = q.get()
            # scan the subdomain
            url = f"http://{subdomain}.{domain}"
            try:
                requests.get(url)
            except requests.ConnectionError:
                pass
            else:
                print("[+] Discovered subdomain:", url[7:])

                # add the subdomain to the global list
                with list_lock:
                    self.discovered_domains.append(url[7:])

            # we're done with scanning that subdomain
            q.task_done()

    def main(self, domain, n_threads, subdomains):
        global q

        # fill the queue with all the subdomains
        for subdomain in subdomains:
            q.put(subdomain)

        for t in range(n_threads):
            # start all threads
            worker = Thread(target=self.scan_subdomains, args=(domain,))
            # daemon thread means a thread that will end when the main thread ends
            worker.daemon = True
            worker.start()

    def get_subdomains(self, domain):
        # domain = 'nust.edu.pk'
        # self.output_file = "nust.txt"
        # wordlist = "/home/jzm/Desktop/OfficeWorkFromH/FullProject/UI/app/home/subdomains.txt"
        # num_threads = 10
        #
        # self.main(domain=domain, n_threads=num_threads, subdomains=open(wordlist).read().splitlines())
        # q.join()
        crawl_handler = crawler()
        if "http" in domain:
            crawl_handler.crawl(domain)
        else:
            # url1 = "https://" + url
            url1 = [domain]
            fullsitename = getFullSiteNameWithHTTP(url1)
            crawl_handler.crawl(fullsitename[0])

        internal = crawl_handler.internal_urls
        external = crawl_handler.external_urls
        file_link = []
        for internal_link in internal:
            if internal_link.split(".")[-1] in ["jpg", "docx", "doc", "txt", "docs", "jpeg", "png", "PNG", "pdf",
                                                "gif", "tiff", "svg"]:
                file_link.append(internal_link)
            else:
                a = internal_link.split("/")
                if a[2] != str(domain):
                    # b = internal_link
                    self.discovered_domains.append(a[2])


'''
if __name__ == "__main__":
    # import argparse
    # parser = argparse.ArgumentParser(description="Faster Subdomain Scanner using Threads")
    # parser.add_argument("domain", help="Domain to scan for subdomains without protocol (e.g without 'http://' or 'https://')")
    # parser.add_argument("-l", "--wordlist", help="File that contains all subdomains to scan, line by line. Default is subdomains.txt",
    #                     default="subdomains.txt")
    # parser.add_argument("-t", "--num-threads", help="Number of threads to use to scan the domain. Default is 10", default=10, type=int)
    # parser.add_argument("-o", "--output-file", help="Specify the output text file to write discovered subdomains")
    #
    # args = parser.parse_args()
    # domain = args.domain
    # wordlist = args.wordlist
    # num_threads = args.num_threads
    # output_file = args.output_file

    domain = 'nust.edu.pk'
    output_file = "nust.txt"
    wordlist = "subdomains.txt"
    num_threads = 10

    handle = SubDomains()
    handle.main(domain=domain, n_threads=num_threads, subdomains=open(wordlist).read().splitlines())
    q.join()

    # save the file
    # with open(output_file, "w") as f:
    #     for url in discovered_domains:
    #         print(url, file=f)
'''
