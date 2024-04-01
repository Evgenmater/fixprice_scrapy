from datetime import datetime

import scrapy

from fixprice_scrapy.items import FixpriceScrapyItem
from .price import parse_price


class ExampleSpider(scrapy.Spider):
    name = 'fixprice'
    allowed_domains = ['fix-price.com']
    start_urls = ['https://fix-price.com/catalog/kosmetika-i-gigiena/ukhod-za-polostyu-rta'] # noqa

    def parse(self, response):
        """
        Парсинг всех продуктов на данной странице и переход к следующей стр.
        """
        products = response.css('div.product__wrapper a::attr(href)').getall()
        for product in products:
            yield response.follow(
                product,
                callback=self.parse_product
            )

        next_page = response.css(
            'div.controls a.button.next::attr(href)'
        ).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        """Парсинг конкретного продукта."""
        url = str(response).strip('<200 >')
        price_data = parse_price(url)
        metadata_key = response.css(
            'div.properties span.title::text'
        ).getall()
        metadata_value = response.css(
            'div.properties span.value::text'
        ).getall()
        brand = ''

        if response.css('p.property span.value a::text').get():
            brand += response.css('p.property span.value a::text').get()
        data = {
            'timestamp': datetime.now(),
            'RPC': response.css('p.property span.value::text').get(),
            'url': url,
            'title': response.css('h1.title::text').get(),
            'marketing_tags': [],
            'brand': brand,
            'section': response.css('div.crumb span.text::text').getall(),
            'price_data': {
                'current': price_data[0],
                'original': price_data[-2],
                'sale_tag': f'Скидка {price_data[-1]} %'
            },
            'stock': {
                "in_stock": None,
                "count": None,
            },
            'assets': {
                'main_image': response.css(
                    'div.swiper-wrapper img::attr(src)'
                ).get(),
                'set_images': response.css(
                    'img.thumbs-image::attr(src)'
                ).getall(),
                'view360': [],
                'video': []
            },
            'metadata': {
                'description': response.css(
                    'div.product-details div.description::text'
                ).get(),
            },
            'variants': len(
                response.css('img.thumbs-image::attr(src)').getall()
            ),
        }
        if len(metadata_key) != len(metadata_value):
            for i in range(len(metadata_value)):
                data['metadata'][metadata_key[i+1]] = metadata_value[i]
        else:
            for i in range(len(metadata_value)):
                data['metadata'][metadata_key[i]] = metadata_value[i]
        yield FixpriceScrapyItem(data)
