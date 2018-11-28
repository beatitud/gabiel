# Gabiel - A great mass hours bot-scraper

Gabiel tends to be a very clever bot-scraper, browsing parish sites and collecting all detected events.

## 1. Get started

How to launch the scraper?

First install requirements in a virtual env:
```shell
$ pip3 install -r requirements.pip
```

Then, run:
```shell
$ python3 main.py
```

## 2. How Gabiel (will) work(s)

**INPUT** : the list of domain names to visit, corresponding each to a unique parish entity.

From this list, Gabiel: 
- browses all the web pages available from the entry web page linked to the domain name 
- tries to find in each page mass hours, and keep it in memory
- can detect whether the parish uses a mass hours widget such as MesseInfo widget or not (if it is the case, we need to know it not to loose time to collect redundant or nonexistent information)
- remembers which url is containing the relevant data we're looking for
- is able to check only these relevant urls when we ask for a quick update, or deep checks the whole website when we ask for it
- is able to detect any change between the current and the last check up

**OUTPUT** : Gabiel (should) returns for each parish the following information:

```json
{
    "useMassWidget": false,
    "widget": "",
    "massEvents": 
        [  
             {  
                "start": "2018-11-18T06:30:00+0000",
                "end": "2018-11-18T07:30:00+0000",
                "isAllDay": false,
                "description": "",
                "sourceUrl": "<PARISH_WEB_PAGE_URL>",
                "repetitions": {  
                }
             },
             {
                "...": "..."
             }
        ]
}
``` 

