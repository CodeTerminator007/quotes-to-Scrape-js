import scrapy
from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']

 
    script = '''
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(1))
        splash:set_viewport_full()
        return {
            html = splash:html()
        }
    end
    '''
    def start_requests(self):
        yield SplashRequest(url = "http://quotes.toscrape.com/js" , callback = self.parse , endpoint ="execute" , args={
            'lua_source' : self.script
            })
    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                
                'Text' : quote.xpath('.//span[1]/text()').get(),
                'Aurthur' : quote.xpath('.//span[2]/small/text()').get(),
                'Tags' : quote.css("div.tags a.tag::text").extract()
            }
            next_page = response.xpath('//li[@class="next"]/a/@href').get()
            link = "http://quotes.toscrape.com"

            if next_page:

                yield SplashRequest(url=link + next_page,callback = self.parse)

