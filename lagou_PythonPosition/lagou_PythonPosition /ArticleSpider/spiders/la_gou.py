# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import json
from scrapy.http import Request, FormRequest, HtmlResponse
from ArticleSpider.items import LagouJobItemLoader, LagouJobItem
from ArticleSpider.utils.common import get_md5
from datetime import datetime
try:
    import urlparse as parse
except:
    from urllib import parse


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ["lagou.com"]
    start_urls = ['https://www.lagou.com/zhaopin/Python/']

    rules = (
        Rule(LinkExtractor(allow=('zhaopin/.*',)), follow=True),
        Rule(LinkExtractor(allow=('gongsi/j/\d+.html',)), follow=True),
        Rule(LinkExtractor(allow=(r'jobs/\d+.html',)), callback='parse_job'),
    )



    # 为了模拟浏览器，我们定义httpheader
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
    }

    def parse_question(self, response):
        pass

    def parse_answer(self, reponse):
        pass

    def start_requests(self):
        return [scrapy.Request('https://passport.lagou.com/login/login.html',
                               meta={'cookiejar': 1},headers=self.headers,callback=self.login)]

    def login(self, response):
        # 先去拿隐藏的表单参数authenticity_token
        match = re.search("X_Anti_Forge_Token = '(.*)';", response.text)
        if match:
            X_Anti_Forge_Token = match.group(1)

        match = re.search("X_Anti_Forge_Code = '(.*)';", response.text)
        if match:
            X_Anti_Forge_Code = match.group(1)

        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
            "X-Anit-Forge-Code": X_Anti_Forge_Code,
            "X-Anit-Forge-Token": X_Anti_Forge_Token
        }

        post_url = "https://passport.lagou.com/login/login.json"
        post_data = {
            "isValidate": "true",
            "username":	"17691183665",
            "password":	"6c3f4889ad2818bec5cae13f9ca6ca32",
            "request_form_verifyCode": "",
            "submit": ""
        }

        return [scrapy.FormRequest(
            url=post_url,
            meta={'cookiejar': response.meta['cookiejar']},
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "message" in text_json and text_json["message"] == "操作成功":
            for url in self.start_urls:
                yield scrapy.Request(url,meta={'cookiejar': response.meta['cookiejar']},headers=self.headers)

    # def _requests_to_follow(self, response):
    #     """重写加入cookiejar的更新"""
    #     if not isinstance(response, HtmlResponse):
    #         return
    #     seen = set()
    #     for n, rule in enumerate(self._rules):
    #         links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]
    #         if links and rule.process_links:
    #             links = rule.process_links(links)
    #         for link in links:
    #             seen.add(link)
    #             r = Request(url=link.url, callback=self._response_downloaded, headers=self.headers)
    #             # 下面这句是我重写的
    #             r.meta.update(rule=n, link_text=link.text)
    #             yield rule.process_request(r)

    def parse_job(self, response):
        # 解析拉勾网的职位
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("tags", '.position-label li::text')
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.now())

        job_item = item_loader.load_item()

        return job_item