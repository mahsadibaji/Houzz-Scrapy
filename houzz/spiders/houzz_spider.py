import scrapy
from houzz.items import HouzzItem
import re

class HouzzSpider(scrapy.Spider):
    name = "houzz"

    def start_requests(self):

        urls = [
            f"https://www.houzz.com/products/{self.category}",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        product_urls = response.css(".hz-product-card a::attr(href)").extract()
        page_no = response.css(".hz-pagination-link--selected ::text").extract_first()
        category = response.css(".hz-br-resultset-header h1::text").extract_first()
        for url in product_urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_product,
                                 meta={'category': category})

        next_page = response.css(".hz-pagination-bottom .hz-pagination-link--next ::attr(href)").extract_first()

        if next_page and page_no < self.to_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_product(self, response):
        item = HouzzItem()

        item['url'] = response.request.url
        item['category'] = response.meta['category']
        item['name'] = response.css(".hz-view-product-title .view-product-title ::text").extract_first()
        item['keywords'] = response.css(".product-keywords .product-keywords__word::text").extract()
        item['image1'] = response.css(".view-product-image img::attr(style)").re_first(r'url\(([^\)]+)')
        small_images = response.css(".alt-images__thumb[data-compid='product_thumb'] img::attr(src)").extract()[0:2]

        
        # convert the url of small image to the format of big image urls according to the url of item[image1](first big image)
        if len(small_images)>1:

            big_img_url=item['image1']
            small_img_url=small_images[1]

            s_str1='fimgs/'
            b_str1='simgs/'
            str2='_'
                
            reg=f"(?<={s_str1}).*?(?={str2})"
            r=re.compile(reg,re.DOTALL)
            small_img_id=r.findall(small_img_url)[0]

            reg=f"(?<={b_str1}).*?(?={str2})"
            r=re.compile(reg,re.DOTALL)
            item['image2']=r.sub(small_img_id,big_img_url)


        yield item
