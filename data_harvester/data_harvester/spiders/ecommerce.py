import scrapy

class EcommerceSpider(scrapy.Spider):
    name = "ecommerce"
    allowed_domains = ["jumia.co.ke"]
    start_urls = ['https://www.jumia.co.ke/']

    def parse(self, response):
        # Follow a category link or search results; for example, electronics
        category_url = "https://www.jumia.co.ke/electronics/"
        yield scrapy.Request(url=category_url, callback=self.parse_category)

    def parse_category(self, response):
        products = response.css('article.c-prd')  # Product container

        for product in products:
            yield {
                'title': product.css('h3.name::text').get(),
                'price': product.css('div.prc::text').get(),
                'url': response.urljoin(product.css('a::attr(href)').get()),
            }

        # Follow pagination
        next_page = response.css('a.pg::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_category)