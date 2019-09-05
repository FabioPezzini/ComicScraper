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

    def parse_2page(self, response):
        item = ComicsBoxItem(response.request.meta["item"])

        row2page = response.xpath("//*[@id='lista-table']//tr")
        for sel2page in row2page[1:]:
            item = ComicsBoxItem(response.request.meta["item"])
            n3page = sel2page.xpath('.//td[1]//a/@href').get()

            link_3page = 'https://www.comicsbox.it/' + n3page
            yield scrapy.Request(link_3page, callback=self.parse_3page, meta={'item': item})

        pagination = response.xpath("//*[@class='pagination']//ul//li//a[text()='Last']/@href").get()
        if pagination is not None:
            first = pagination.split("=", 1)[0]
            second = pagination.split("=", 1)[1]
            for i in range(50, int(second)+50, 50):
                next2url = "https://www.comicsbox.it" + first + "=" + str(i)
                yield scrapy.Request(next2url, callback=self.parse_2page, meta={'item': item})

    def parse_3page(self, response):
        item = ComicsBoxItem(response.request.meta["item"])

        trans_table = {ord(c): None for c in u'\r\n\t'}
        item['issueTitle'] = ''.join(s.translate(trans_table) for s in response.xpath("//div[@id='intestazione']//h1/text()").get()).replace("# ", "#")

        selIss = response.xpath("//div[@id='maintext_cb']//div[@class='alboita_right']")
        if len(selIss) >= 1:
            item['issueOriginalStory'] = selIss.xpath("./strong//a/text()").extract()

        return item
