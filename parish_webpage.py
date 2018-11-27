import requests
from bs4 import BeautifulSoup
import re
import io
import PyPDF2
from utils.url import Url


class ParishWebPage:
    def __init__(self, url):
        self.url = Url(url)
        self.content = None
        self.bs = None
        self.is_valid = None
        self.mass_hours = []

    def is_valid_url(self):
        try:
            self.content = self.get_html_content()
            self.bs = BeautifulSoup(self.content, 'html.parser').body
            self.is_valid = True
            return self.is_valid
        except Exception as ex:
            print(str(ex))
            self.is_valid = False
            return self.is_valid

    def get_html_content(self):
        res = requests.get(str(self.url))

        # We handle pdf files
        if self.is_pdf():
            pdf = PyPDF2.PdfFileReader(io.BytesIO(res.content))
            num_pages = pdf.getNumPages()
            html = "".join(["<div>{}</div>".format(pdf.getPage(i).extractText()) for i in range(num_pages)])
            html = "<body>{}</body>".format(html)
            return html

        return res.content

    def get_page_mass_hours(self):
        # We try to detect mass hours in page
        mass_hours_elements = self.bs.find_all(text=re.compile('[^\w\d](\d{1,2}h\d{1,2})[^\w\d]'))
        for mass_hours_element in mass_hours_elements:
            print(u"[*] {}".format(mass_hours_element.string.replace("\n", " ")))

        self.mass_hours = list(map(lambda e: e.string, mass_hours_elements))
        return self.mass_hours

    def is_pdf(self):
        return str(self.url)[:-3] == "pdf"

    def get_links(self, filter_on_mass_kw=True):
        # We collect all links in page
        a_elements = self.bs.find_all('a')

        # If requested, we filter on mass keywords
        if filter_on_mass_kw:
            a_elements = filter(lambda a_element: 'messe' in a_element.get_text().lower(), a_elements)

        # We extract paths from html elements
        links = list(map(lambda a_element: a_element.get("href", ""), a_elements))

        # We normalize links
        normalized_links = dict()
        for link in links:

            # If http in link, it is probably not a single path
            if 'http' in link and link not in normalized_links:
                normalized_links[link] = Url(link)
                continue

            # If we just have a path, we complete with host name
            if not str(self.url.host) in link:
                link = Url()
                link.set(host=str(self.url.host))
                link.set(host=str(self.url.host))
                link.normalize()

                if not str(link) in normalized_links:
                    normalized_links[str(link)] = link

        return normalized_links.values()
