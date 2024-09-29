import scrapy
from scrapy_playwright.page import PageMethod



class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["www.imdb.com"]

    start_urls = ["http://www.imdb.com/chart/top/"]
    

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,  
                    "playwright_page_pagemethod": [
                        PageMethod("wait_for_selector", "li.ipc-metadata-list-summary-item"),
                    ],
                },
                callback=self.parse
            )


    def parse(self, response):
        movies=response.css('li.ipc-metadata-list-summary-item')

        for movie in movies:
            yield{
                'Title': movie.css('h3::text').get().split(". ")[1],
                'Release year': movie.css('.cli-title-metadata span::text').get(),
                'IMDB Rating':movie.css("span::attr(aria-label)").get().split(": ")[1],


            }

