import scrapy

from ..items import ComicsBoxItem


class ComicsBoxSpider(scrapy.Spider):
    name = "comicsbox"
    start_urls = ["https://www.comicsbox.it/serieitaliane"]

    def parse(self, response):
        row = response.xpath("//*[@id='lista-table']//tr")
        for sel in row[1:]:
            item = ComicsBoxItem()
            item['titleEdizione'] = sel.xpath('./td[1]//a/text()').extract()[0]
            item['linkEdizione'] = sel.xpath('.//td[1]//a/@href').extract()[0]
            item['year'] = sel.xpath('./td[2]/text()').extract()[0]
            item['numbers'] = sel.xpath('./td[3]/text()').extract()[0]
            item['publisher'] = sel.xpath('./td[5]/text()').extract()[0]
            # if doesn't is in corso allora itera dentro
            link_2page = 'https://www.comicsbox.it/' + sel.xpath('./td[1]//a/@href').get()
            yield scrapy.Request(link_2page, callback=self.parse_2page, meta={'item': item})

            # next_page = response.xpath("//a[@class='next i-next']/@href").extract_first()
            # if next_page is "http://comics.panini.it/store/pub_ita_it/magazines.html?p=15":  #Scrape only fist 15 pages, set is Not None for scrape all list
            # next_page_link = response.urljoin(next_page)
            # yield scrapy.Request(url=next_page_link)

    def parse_2page(self, response):
        item = ComicsBoxItem(response.request.meta["item"])
        # print(response.xpath("//div[@class='dettagli_testo']/text()").get())
        # l.add_xpath('dettagliEdizione', "./div[@class='dettagli_testo']/text()")

        row2page = response.xpath("//*[@id='lista-table']//tr")
        for sel2page in row2page[1:]:
            item = ComicsBoxItem(response.request.meta["item"])
            n3page = sel2page.xpath('.//td[1]//a/@href').get()
            # print(n3page)
            link_3page = 'https://www.comicsbox.it/' + n3page
            yield scrapy.Request(link_3page, callback=self.parse_3page, meta={'item': item})

        # CONTROLLARE CHE NON CI SIANO ALTRE PAGINE DELLA TABELLA

    def parse_3page(self, response):
        item = ComicsBoxItem(response.request.meta["item"])
        # print(response.xpath("//div[@id='intestazione']//h1/text()").get())
        # l.add_xpath('issueTitle', "//div[@id='intestazione']//h1/text()")
        trans_table = {ord(c): None for c in u'\r\n\t'}
        item['issueTitle'] = ''.join(
            s.translate(trans_table) for s in response.xpath("//div[@id='intestazione']//h1/text()").get()).replace(
            "# ", "#")

        return item
