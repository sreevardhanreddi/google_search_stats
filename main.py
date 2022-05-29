import csv
from datetime import datetime
import json
import os
import pandas as pd
import re

import requests
from bs4 import BeautifulSoup


def _get_urls():
    urls = []
    with open("input.txt") as f:
        for i in f.readlines():
            url = i.strip("\r\n").strip("\n")
            if url:
                urls.append(url)

    return urls


def _get_result(url: str):
    url_path = url.replace("https://", "site:")
    url_path = "https://www.google.com/search?q={}".format(url_path)
    res = requests.get(
        url_path,
        headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        },
    )
    if res.ok:
        soup = BeautifulSoup(res.content, "html.parser")
        result = soup.find("div", {"id": "result-stats"})
        result = result.text.replace(",", "")
        re_pattern = "About ([0-9]+) results"
        matches = re.findall(re_pattern, result)
        if len(matches):
            return matches[0]

    return 0


def write_to_file(results=[], date_time=""):
    df = pd.DataFrame(results)
    if os.path.exists("results.csv"):
        df.to_csv("results.csv", mode="a", index=False, header=False)
        return
    df.to_csv("results.csv", mode="a", index=False, header=True)


def main():
    urls = _get_urls()
    results = []
    date_time = datetime.now()

    for url in urls:
        temp = {}
        try:
            val = _get_result(url)
            temp["url"] = url
            temp["results"] = val
            temp["date"] = date_time.strftime("%Y-%m-%d %H:%M:%S")
            results.append(temp)
            print("Results for url {} {}".format(url, val))
        except Exception as e:
            print(e)

    write_to_file(results=results, date_time=date_time)


if __name__ == "__main__":
    main()
