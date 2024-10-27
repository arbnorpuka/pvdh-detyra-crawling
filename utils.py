import requests
import xml.etree.ElementTree as ET

def get_main_mainArticles():
    url = 'https://edition.cnn.com/sitemap/article.xml'
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to get articles')
        return None
    root = ET.fromstring(response.content)
    mainArticles = []
    for child in root:
        mainArticles.append({
            'article_url': child[0].text,
            'last_updated': child[1].text
        })

    return mainArticles


'''
 <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">
   <url>
      <loc>https://www.cnn.com/2024/10/25/us/taylor-swift-new-orleans-superdome-homeless/index.html</loc>
      <lastmod>2024-10-27T14:32:11.019000+00:00</lastmod>
      <image:image>
         <image:loc>https://media.cnn.com/api/v1/images/stellar/prod/ap24297682957790.jpg?c=original/w_800</image:loc>
         <image:caption>Louisiana State police give instructions to people living in a homeless encampment to move to a different pre-designated location as they perform a sweep in advance of a Taylor Swift concert in New Orleans, Wednesday, Oct. 23, 2024.</image:caption>
      </image:image>
      <xhtml:link rel="alternate" hreflang="en-gb" href="https://edition.cnn.com/2024/10/25/us/taylor-swift-new-orleans-superdome-homeless/index.html"/>
      <xhtml:link rel="alternate" hreflang="en-ca" href="https://www.cnn.com/2024/10/25/us/taylor-swift-new-orleans-superdome-homeless/index.html"/>
      <xhtml:link rel="alternate" hreflang="en-us" href="https://www.cnn.com/2024/10/25/us/taylor-swift-new-orleans-superdome-homeless/index.html"/>
      <xhtml:link rel="alternate" hreflang="x-default" href="https://edition.cnn.com/2024/10/25/us/taylor-swift-new-orleans-superdome-homeless/index.html"/>
   </url>
   ...
</urlset>

'''

def get_articles(mainArticle):
    response = requests.get(mainArticle['article_url'])
    if response.status_code != 200:
        print('Failed to get article')
        return []
    root = ET.fromstring(response.content)

    namespaces = {
        '': "http://www.sitemaps.org/schemas/sitemap/0.9",
        'image': "http://www.google.com/schemas/sitemap-image/1.1",
        'xhtml': "http://www.w3.org/1999/xhtml"
    }


    urls = root.findall(f'.//url', namespaces)
    article = []
    for url in urls:
        
        image_loc = url.findall(".//image:image/image:loc", namespaces)
        image_caption = url.findall(".//image:image/image:caption", namespaces)
        #  <xhtml:link rel="alternate" hreflang="x-default" href="https://edition.cnn.com/2024/10/19/us/wanda-dench-breast-cancer-thanksgiving-grandma/index.html"/>
        link_alternate = url.findall(".//xhtml:link[@rel='alternate']", namespaces)
        article.append({
            'loc': url.find('loc', namespaces).text,
            'lastmod': url.find('lastmod', namespaces).text,
            'image_loc': image_loc[0].text if image_loc else None,
            'image_caption': image_caption[0].text if image_caption else None,
            'link_alternate': link_alternate[0].attrib['href'] if link_alternate else None
        })
    return article


