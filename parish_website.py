from parish_webpage import ParishWebPage
from utils.url import Url


class ParishWebSite:
    def __init__(self, base_url):
        self.url = Url(base_url)
        self.index = dict()  # dict with urls as keys, and potential mass hours list as values
        # It will allow us to visit only once each url, keeping in memory what we already visited

    def search_mass_hours(self, quick_check_up=False):
        # We start to search with our entry point: base url
        self.index[str(self.url)] = None

        # While we find at least one url in index we did not checked yet, we continue
        not_checked_yet = [k for k, v in self.index.items() if not v]
        while len(not_checked_yet):
            for url in not_checked_yet:
                page = ParishWebPage(url=url)

                # We try to reach the page. We make sure url is valid.
                if not page.is_valid_url():
                    self.index[str(page.url)] = page
                    break

                # We try to find urls where mass hours are, if we are still on the same host
                if str(Url(url).host) == str(self.url.host):
                    links = page.get_links(filter_on_mass_kw=False)
                    for link in links:
                        # We update our index
                        if not self.index.get(str(link), None):
                            self.index[str(link)] = None

                # Then we try to find mass hours in this page
                page.get_page_mass_hours()

                print("[*] For url: {}".format(url))
                print("[*] Hours detected: {}".format(page.mass_hours))
                self.index[str(page.url)] = page

                not_checked_yet = [k for k, v in self.index.items() if not v]
