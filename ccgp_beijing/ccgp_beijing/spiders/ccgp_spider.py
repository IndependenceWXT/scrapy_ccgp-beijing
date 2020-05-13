import scrapy
from ..items import CcgpBeijingItem
import datetime
from dateutil import parser
class CcgpSpiderSpider(scrapy.Spider):
    name = 'ccgp_spider'
    allowed_domains = ['www.ccgp-beijing.gov.cn']
    start_urls = ['http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index.html']
    format_url="http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/"
    def parse(self, response):
        # response 是列表页的源码
        row_list = response.xpath('.//li')
        for i_item in row_list:
            ccgp_item = CcgpBeijingItem()
            # 这里面的xpath表达式都要以.开头，否则只取第一条
            ccgp_item['url'] = self.format_url + i_item.xpath('.//a/@href').re_first('./(.*)')
            ccgp_item['title'] = i_item.xpath('.//a/text()').extract_first()
            ccgp_item['ctime'] = parser.parse(i_item.xpath('//span/text()').extract_first()).strftime("%Y-%m-%d %H:%M:%S")
            ccgp_item['gtime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 请求详情页的内容，回调detail_content函数，并传递ccgp_item对象
            yield  scrapy.Request(
                url=ccgp_item['url'],
                callback=self.detail_content,
                meta={"ccgp_item":ccgp_item}
            )
        # 获取下一页
        next_link=self.format_url+response.xpath('.//div[@class="a_div"]//a[text()="下一页"]/@href').extract_first()
        if next_link:
            yield scrapy.Request(
                url=next_link,
                callback=self.parse
            )
    def detail_content(self, response):
        ccgp_item = response.meta["ccgp_item"]
        ccgp_item['content'] = response.xpath('.//div[@style="width: 1105px;margin:0 auto"]').extract_first()
        yield ccgp_item
