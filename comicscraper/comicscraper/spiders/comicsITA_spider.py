import scrapy

from ..items import ComicsITAItem


class ComicsITASpider(scrapy.Spider):
    name = "comicsITA"
    custom_settings = {'ITEM_PIPELINES': {'comicscraper.pipelines.ComicscraperPipeline': 300}}
    start_urls = ["https://www.comicsbox.it/serieitaliane"]

    def parse(self, response):
        row = response.xpath("//*[@id='lista-table']//tr")
        for sel in row[1:]:
            item = ComicsITAItem()
            item['serie_title'] = sel.xpath('./td[1]//a/text()').extract()[0]
            item['serie_year'] = sel.xpath('./td[2]/text()').extract()[0]
            item['serie_numbers'] = sel.xpath('./td[3]/text()').extract()[0]
            item['publisher'] = sel.xpath('./td[5]/text()').extract()[0]
            # if doesn't is in corso allora itera dentro
            link_2page = 'https://www.comicsbox.it/' + sel.xpath('./td[1]//a/@href').get()
            yield scrapy.Request(link_2page, callback=self.parse_2page, meta={'item': item})

    def parse_2page(self, response):
        item = ComicsITAItem(response.request.meta["item"])

        row2page = response.xpath("//*[@id='lista-table']//tr")
        for sel2page in row2page[1:]:
            item = ComicsITAItem(response.request.meta["item"])
            n3page = sel2page.xpath('.//td[1]//a/@href').get()
            item['link_albo'] = n3page
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
        item = ComicsITAItem(response.request.meta["item"])

        if response.xpath("//*[@id='subtitolo_issue']/text()").get() is not None:
            item['issue_subtitle'] = response.xpath("//*[@id='subtitolo_issue']/text()").get()


        item['issue_date'] = response.xpath("//*[@id='data_issue']/text()").get()
        item['issue_link_image'] = "https://www.comicsbox.it" + response.xpath("//*[@id='container_cover_cb']//img/@src").get()
        selDel = response.xpath("//*[@id='descrizione_ita']//p/text()")
        if len(selDel) >= 1:
            item['issue_description'] = selDel.get()

        trans_table = {ord(c): None for c in u'\r\n\t'}
        item['issue_title'] = ''.join(s.translate(trans_table) for s in response.xpath("//div[@id='intestazione']//h1/text()").get()).replace("# ", "#")

        selIss = response.xpath("//div[@id='maintext_cb']//div[@class='alboita_right']")
        if len(selIss) >= 1:
            item['issue_originalstories'] = selIss.xpath("./strong//a/text()").extract()

        selDescNoDefault = response.xpath("//div[@class='sinossi']/text()")
        if len(selDel) == 0 and len(selIss) == 1 and len(selDescNoDefault) == 1:
            item['issue_description'] = response.xpath("//div[@class='sinossi']/text()").extract()

        return item
