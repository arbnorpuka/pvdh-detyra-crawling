
from utils import get_main_mainArticles,get_articles
import csv
import time


timeStart = time.time()

mainArticlesLists = get_main_mainArticles()
csv_file = 'articles.csv'
csv_columns = ['loc', 'lastmod', 'image_loc', 'image_caption', 'link_alternate']
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()

    for mainArticlesList in mainArticlesLists:
        print(f"Getting articles from {mainArticlesList['article_url']}")
        progress = (mainArticlesLists.index(mainArticlesList) + 1) / len(mainArticlesLists) * 100
        print(f"Progress: {mainArticlesLists.index(mainArticlesList) + 1}/{len(mainArticlesLists)}", f"percent complete: {progress:.2f}%")
        articles = get_articles(mainArticlesList)
        print(f"Writing {len(articles)} articles to {csv_file}")
        for article in articles:
            writer.writerow(article)

timeEnd = time.time()
print(f"Time taken: {timeEnd - timeStart} seconds")


# print count rows in csv file
with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    print(f"Total articles written to {csv_file}: {len(list(reader)) - 1}")
