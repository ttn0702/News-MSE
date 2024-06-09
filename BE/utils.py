
import requests
from bs4 import BeautifulSoup
from settings import PROXY

def get_soup(url):
    if PROXY.get('http') and PROXY.get('https'):
        _proxy = PROXY
    else:
        _proxy = {}
    print("_proxy: ",_proxy)
    req = requests.get(url, proxies=_proxy)
    soup = BeautifulSoup(req.content, 'xml')
    return soup

def get_article_content(url):
    soup = get_soup(url)
    news_list = []
    items = soup.find_all('item')
    for item in items:
        title = item.title.text if item.title else "No title"
        link = item.link.text if item.link else "No link"
        published = item.pubDate.text if item.pubDate else "No published date"

        if item.description:
            description = item.description.text
            description_soup = BeautifulSoup(description, 'html.parser')
            description_text = description_soup.get_text(separator=' ', strip=True)
            link_tag = description_soup.find('a')
            news_link = link_tag['href'] if link_tag else "No link"
        else:
            description_text = "No description"

        if item.enclosure:
            image_link = item.enclosure.get('url')
        else:
            image_link = ""

        news_item = {
            "title": title,
            "link": link,
            "published": published,
            "description": description_text,
            "url": news_link,
            "image_link": image_link
        }
        news_list.append(news_item)
    return news_list
