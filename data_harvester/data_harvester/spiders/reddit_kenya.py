import scrapy

class RedditInterestsSpider(scrapy.Spider):
    name = "reddit_interests"
    allowed_domains = ["reddit.com"]
    # Example searching for real estate or consumer trends in Kenya
    start_urls = ["https://www.reddit.com/r/Kenya/search/?q=housing+rent+market&type=link"]    

    def parse(self, response):
        # Select post items from Reddit's search results layout
        for post in response.css('a[data-testid="search-post-title"], div.search-result-link'):
            title = post.css('span::text, h3::text').get()
            url = post.attrib.get('href')
            
            # Extract score/upvotes if available
            score_text = post.xpath('.//span[contains(@id, "vote-score")]/text()').get() or "0"
            
            yield {
                'title': title.strip() if title else "No Title",
                'upvotes': score_text.strip(),
                'url': url if url else ""
            }