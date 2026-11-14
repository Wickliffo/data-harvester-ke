import scrapy

class RealestateSpider(scrapy.Spider):
    name = 'realestate'
    allowed_domains = ['property24.co.ke']
    start_urls = ['https://www.property24.co.ke/property-for-sale']

    def parse(self, response):
        # Select each listing's container (update selector if needed)
        listings = response.css('div.p24_regularTile')

        for listing in listings:
            yield {
                'price': listing.css('span.p24_price::text').get(default='').strip(),
                'title': listing.css('span.p24_propertyTitle::text').get(default='').strip(),
                'location': listing.css('span.p24_location::text').get(default='').strip(),
                'address': listing.css('span.p24_address::text').get(default='').strip(),
                'description': listing.css('span.p24_excerpt::attr(title)').get(default='').strip(),
                'url': listing.css('a::attr(href)').get()
            }

        # Pagination link selector (update as needed)
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)