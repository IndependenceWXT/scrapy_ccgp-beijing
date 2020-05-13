import scrapy
class CcgpBeijingItem(scrapy.Item):
    # url
    url=scrapy.Field()
    # 标题
    title=scrapy.Field()
    # 发布时间
    ctime=scrapy.Field()
    # 爬取时间
    gtime=scrapy.Field()
    # 文章内容
    content=scrapy.Field()
