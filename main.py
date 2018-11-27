from data.parish_list import parish_list
from parish_website import ParishWebSite

# parish_list = ["https://www.paroisses-hennebont.org/"]

for index, url in enumerate(parish_list):
    if index < 100:
        print("[*] Working on url {}".format(url))
        website = ParishWebSite(base_url=url)
        website.search_mass_hours()
