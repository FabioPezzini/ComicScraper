import scrapy

from ..items import ComicsITAItem
from ..items import ComicsImage


class ComicsITASpider(scrapy.Spider):
    name = "comicsITA"
    custom_settings = {'ITEM_PIPELINES': {'comicscraper.pipelines.ComicscraperPipeline': 300,
                                          'comicscraper.pipelines.CustomImageNamePipeline': 1}}
    start_urls = [""]  # TO ADD THE URL, SEE IN settings.py

    def parse(self, response):
        row = response.xpath("//*[@id='lista-table']//tr")
        for sel in row[1:]:
            item = ComicsITAItem()
            item['serie_title'] = sel.xpath('./td[1]//a/text()').extract()[0]
            item['serie_year'] = sel.xpath('./td[2]/text()').extract()[0]
            item['serie_numbers'] = sel.xpath('./td[3]/text()').extract()[0]
            item['publisher'] = sel.xpath('./td[5]/text()').extract()[0]

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
            for i in range(50, int(second) + 50, 50):
                next2url = "https://www.comicsbox.it" + first + "=" + str(i)
                yield scrapy.Request(next2url, callback=self.parse_2page, meta={'item': item})

    def parse_3page(self, response):
        item = ComicsITAItem(response.request.meta["item"])

        if response.xpath("//*[@id='subtitolo_issue']/text()").get() is not None:
            item['issue_subtitle'] = response.xpath("//*[@id='subtitolo_issue']/text()").get()

        item['issue_date'] = response.xpath("//*[@id='data_issue']/text()").get()
        imgurl = "https://www.comicsbox.it" + response.xpath("//*[@id='container_cover_cb']//img/@src").get()
        item['issue_link_image'] = imgurl

        itemI = ComicsImage()
        itemI['image_urls'] = [imgurl]
        itemI['image_names'] = [imgurl.split('/')[5].split('&')[0]]

        selDel = response.xpath("//*[@id='descrizione_ita']//p/text()")
        if len(selDel) >= 1:
            item['issue_description'] = selDel.get()

        trans_table = {ord(c): None for c in u'\r\n\t'}
        item['issue_title'] = ''.join(
            s.translate(trans_table) for s in response.xpath("//div[@id='intestazione']//h1/text()").get()).replace(
            "# ", "#")

        selIss = response.xpath("//div[@id='maintext_cb']//div[@class='alboita_right']")
        if len(selIss) >= 1:
            item['issue_originalstories'] = selIss.xpath("./strong//a/text()").extract()

            # Check if exits authors
            selAuthors = response.xpath("//div[@class='alboita_dettagli']/a/text()")
            if selAuthors is not None:
                item['authors'] = selAuthors.extract()

            # Check if exits protagonists
            selProtagonists = response.xpath("//div[@class='alboita_right']/a/text()")
            selTypeOf = response.xpath("//div[@class='alboita_right']/em/text()")
            if selProtagonists is not None and selTypeOf.get() == 'protagonisti:':
                item['protagonists'] = selProtagonists.extract()

            # Check if exits a description of the issue
            selDesc = response.xpath("//div[@id='descrizione_ita']/p/text()")
            selDescNoDefault = response.xpath("//div[@class='sinossi']/text()")
            if len(selDesc) > 0:
                item['issue_description'] = selDesc.extract()
            elif len(selDescNoDefault) > 0:
                item['issue_description'] = selDescNoDefault.extract()

        return item, itemI