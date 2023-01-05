import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0"
    }

    url = "https://ubr.ua/ukraine-and-world/technology/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="content_One_News_Block")

    news_dict = {}
    for article in articles_cards:
        article_title = article.find("p", class_="block_Info_Title").text.strip()
        article_desc = article.find("div", class_="block_Info_Subtitle").text.strip()
        article_url = article.find("a").get("href")
        article_time = article.find("p", class_="block_Info_Date").text.strip()

        article_id = article_url.split("/")[-1]

        # print(f"{article_title} | {article_url} | {article_time}")

        news_dict[article_id] = {
            "article_time": article_time,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0"
    }

    url = "https://ubr.ua/ukraine-and-world/technology/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="content_One_News_Block")

    fresh_news = {}
    for article in articles_cards:
        article_url = article.find("a").get("href")
        article_id = article_url.split("/")[-1]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("p", class_="block_Info_Title").text.strip()
            article_desc = article.find("div", class_="block_Info_Subtitle").text.strip()

            article_time = article.find("p", class_="block_Info_Date").text.strip()


        news_dict[article_id] = {
                "article_time": article_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

        fresh_news[article_id] = {
            "article_time": article_time,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    # get_first_news()
    print(check_news_update())


if __name__ == '__main__':
    main()

