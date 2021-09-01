from bs4 import BeautifulSoup
from requests_html import HTMLSession
session = HTMLSession()


def scrape_product(url):
    
    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # ID
    id_index=url.split("/").index("listing")+1
    id = url.split("/")[id_index]
    
    # Title
    title = soup.title.string
    title = title.replace(" | Etsy", "")
    
    # Price
    price = soup.find("meta",  {"property":"product:price:amount"})["content"]
    
    #Currency
    currency = soup.find("meta",  {"property":"product:price:currency"})["content"]

    # Images
    img = soup.find("img", {"class":"wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded"})
    if img.get("src"):
        image = str(img.get("src"))
    else:
        image = str(img.get("data-src"))
   
    # Returns JSON data
    return {
        "product_id": id,
        "title": title,
        "price":price,
        "image": image,
        "currency": currency
    }