import scrapy

class SocialMediaSpider(scrapy.Spider):
    name = "socialmedia"
    allowed_domains = ["example-social-trends-site.com"]
    start_urls = ['http://example-social-trends-site.com/kenya-trends']

    def parse(self, response):
        trends = response.css('div.trend-card')  # Example selector, adjust per site
        for trend in trends:
            yield {
                'hashtag': trend.css('a.trend::text').get(),
                'tweet_count': trend.css('span.count::text').get(),
                'description': trend.css('p.desc::text').get(),
            }
