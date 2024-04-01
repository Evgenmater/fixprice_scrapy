from time import sleep

from selenium import webdriver

from selectolax.parser import HTMLParser


def extract(url):
    driver = webdriver.Firefox()
    driver.get(url)
    sleep(2.5)
    html = driver.page_source
    driver.close()

    return html


def parse_price(url):
    """Парсинг цены продукта."""
    web_html = extract(url)
    html = HTMLParser(web_html)
    prices = html.css("div.price-in-cart")
    price_discount = prices[0]
    original_price = price_discount.css_first(
        "div.regular-price"
    ).text().replace(',', '.')
    price_list = [original_price]
    if price_discount.css_first("div.special-price"):
        special_price = price_discount.css_first(
            "div.special-price"
        ).text().replace(',', '.')
        price_list.insert(0, special_price)
        discount_percentage = (
            (
                float(original_price.strip('₽')) - float(
                    special_price.strip('₽')
                )
            ) / float(original_price.strip('₽'))) * 100
        price_list.append(round(discount_percentage, 2))
    else:
        discount_percentage = 0
        price_list.append(discount_percentage)
    return price_list
