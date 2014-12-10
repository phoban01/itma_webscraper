from lxml import html
import requests

def make_request(url,data_store,get_total_pages=False):
    global total_pages
    page = requests.get(url)
    tree = html.fromstring(page.text)
    if get_total_pages == True:
        total_pages = int(tree.xpath('//p[@class="pagLinks"]/text()')[0].split()[3])
        if total_pages == 2:
            total_pages += 1
    next_page_link = tree.xpath('//p[@class="pagLinks"]/a/@href')[-2]
    img_links = [x.encode('utf-8') for x in tree.xpath('//div[@class="listArticle"]/a/@href')]
    img_titles = [x.encode('utf-8') for x in tree.xpath('//div[@class="listArticle"]/a/@title')]
    img_thumbs = [x.encode('utf-8') for x in tree.xpath('//div[@class="listArticle"]/a/img/@src')]
    data_store.extend(zip(img_titles,img_links,img_thumbs))
    return next_page_link

def get_itma_thumbnails(url):
    data_store = []
    next_page_link = make_request(url,data_store,True)
    current_page = 2

    while current_page < total_pages:
        print next_page_link
        next_page_link = make_request(next_page_link,data_store)
        current_page += 1
    return data_store

base_path = "/Users/piarashoban/Documents/CodingProjects/itma_webscraper/"
base_url = "http://www.itma.ie/digitallibrary/"
ext_urls = ["images-all","printed-items-all","interactivescores-all"]

for url in ext_urls:
    outputfile = open(base_path+"%s_thumbnail_data.txt"%url.replace('-','_'),"w")
    scraped_data = get_itma_thumbnails(base_url+url)
    for i,data in enumerate(scraped_data):
        outputfile.write("%s\t%s , %s , %s\n" % (i+1,data[0],data[1],data[2]))
    outputfile.close()

