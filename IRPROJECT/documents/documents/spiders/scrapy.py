import scrapy
from scrapy.exceptions import CloseSpider
import os

class DocumentSpider(scrapy.Spider):
    name = 'scrapy'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Cricket']

    def __init__(self, max_pages=100, max_depth=3, *args, **kwargs):
        super(DocumentSpider, self).__init__(*args, **kwargs)
        self.max_pages = int(max_pages)
        self.max_depth = int(max_depth)
        self.pages_count = 0
        self.output_directory = 'output'  # Define output directory for HTML files

        # Ensure the output directory exists
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def parse(self, response):
        if self.pages_count >= self.max_pages:
            raise CloseSpider(reason="Reached max page limit")

        self.pages_count += 1
        filename = os.path.join(self.output_directory, f'wiki_cricket_{self.pages_count}.html')
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        if response.meta.get('depth', 0) < self.max_depth:
            for href in response.css('a::attr(href)').getall():
                if href.startswith("/wiki/") and not any(x in href for x in [':', '#']):
                    yield response.follow(href, callback=self.parse)

# Running the spider typically requires a Scrapy framework and command line
# For example:
# scrapy runspider <filename.py>
