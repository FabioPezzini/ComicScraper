import scrapy

from ..items import PaniniItem
from scrapy.loader import ItemLoader


class PaniniSpider(scrapy.Spider):
    name = "panini"
    start_urls = ["http://comics.panini.it/store/pub_ita_it/magazines.html"]

    def parse(self, response):
        # Get all the <a> tags
        for sel in response.xpath("//div[@class='list-group']//h3/a"):
            l = ItemLoader(item=PaniniItem(), selector=sel)
            l.add_xpath('title', './text()')
            l.add_xpath('link', './@href')

            request = scrapy.Request(sel.xpath('./@href').get(), callback=self.parse_2page,
                                     dont_filter=True)
            request.meta['l'] = l
            yield request

            next_page = response.xpath("//a[@class='next i-next']/@href").extract_first()
            if next_page is "http://comics.panini.it/store/pub_ita_it/magazines.html?p=15":  #Scrape only fist 15 pages, set is Not None for scrape all list
                next_page_link = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_link)

    def parse_2page(self, response):
        l = response.meta['l']
        l.add_value('price', response.xpath("//p[@class='special-price']//span/text()").get())
        l.add_value('publication_date', response.xpath("//div[@id='data-pubblicazione']//h3/text()").get())
        l.add_value('series', response.xpath("//h3[@class='serie']/text()").get())
        l.add_value('subtitle', response.xpath("//small[@class='subtitle']/text()").get())
        l.add_value('authors', response.xpath("//div[@id='authors']//div/text()").get())
        l.add_value('include', response.xpath("//div[@id='includes']//div/text()").get())
        l.add_value('image_url', response.xpath("//a[@id='aImgProd']/@href").get())
        l.add_value('description', response.xpath("//div[@id='description']/text()").get())
        l.add_value('pages', response.xpath("//div[@id='pages']//div/text()").get())

        return l.load_item()
