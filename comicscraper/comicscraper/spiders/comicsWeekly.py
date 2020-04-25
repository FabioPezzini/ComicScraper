import scrapy

from ..items import ComicsBoxWeeklyItem
from ..items import ComicsImage


class ComicsWeeklySpider(scrapy.Spider):
    name = "comicsWeekly"
    custom_settings = {'ITEM_PIPELINES': {'comicscraper.pipelines.ComicscraperWeeklyPipeline': 300,
                                          'comicscraper.pipelines.CustomImageNamePipeline': 1}}
    start_urls = [""]  # TO ADD THE URL, SEE IN settings.py

    def parse(self, response):
        row = response.xpath("//*[@id='lista-table']//tr")
        for sel in row[1:]:
            item = ComicsBoxWeeklyItem()
            date_time = sel.xpath('./td[1]/text()').get()
            item['date'] = date_time.split(" ", 1)[0]
            item['action'] = sel.xpath('./td[3]/text()').get()
            section = sel.xpath('./td[4]/text()').get()
            # It is possibile to add section = 'Storia' if you want more comics
            if section == 'Albo italiano':
                item['link_albo'] = sel.xpath('.//td[5]//a/@href').get()
                link_3page = 'https://www.comicsbox.it/' + sel.xpath('./td[5]//a/@href').get()
                yield scrapy.Request(link_3page, callback=self.parse_3page, meta={'item': item})
            # Here is possible to change the number of page to scrape
            for i in range(50, 1800 + 50, 50):
                next2url = "https://www.comicsbox.it/editlog.php?&limite=" + str(i)
                yield scrapy.Request(next2url, callback=self.parse, meta={'item': item})

    def parse_3page(self, response):
        item = ComicsBoxWeeklyItem(response.request.meta["item"])

        titleEdizione = response.xpath("//*[@id='serielista']//a/text()").get()
        edition = titleEdizione.split("di ", 1)[1]
        item['serie_title'] = edition
        if response.xpath("//*[@id='subtitolo_issue']/text()").get() is not None:
            item['issue_subtitle'] = response.xpath("//*[@id='subtitolo_issue']/text()").get()

        item['publisher'] = response.xpath("//*[@id='editore_issue']/text()").get()
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

        selDescNoDefault = response.xpath("//div[@class='sinossi']/text()")
        if len(selDel) == 0 and len(selIss) == 1 and len(selDescNoDefault) == 1:
            item['issue_description'] = response.xpath("//div[@class='sinossi']/text()").extract()

        return item, itemI
