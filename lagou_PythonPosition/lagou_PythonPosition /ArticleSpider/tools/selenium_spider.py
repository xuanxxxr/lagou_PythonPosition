# _*_ coding:utf-8 _*_

from selenium import webdriver
from scrapy.selector import Selector

#设置browser的位置和类型
# browser = webdriver.Chrome(executable_path="/Users/xuanren/Downloads/chromedriver")

#模拟知乎登陆
# browser.get("https://www.zhihu.com/#signin")
# print(browser.page_source)
# browser.find_element_by_css_selector(".signin-switch-password").click()
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("295644935@qq.com")
# browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys("82120963")
# browser.find_element_by_css_selector(".view-signin button.sign-button").click()

#测试
# t_selecter = Selector(text=browser.page_source)
# print (t_selecter.css(".tm-price::text").extract())


#模拟微博登录
#
# browser.get("https://www.weibo.com")

import time
time.sleep(5)
# browser.find_element_by_css_selector("#loginname").send_keys("17691183665")
# browser.find_element_by_css_selector(".info_list.password input[name='password']").send_keys("82120963")
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()


#下拉页面
# browser.get("https://www.oschina.net/blog")
# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; "
#                        "return lenOfPage;")
#     time.sleep(3)


#设置Chromedriver不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(executable_path="/Users/xuanren/Downloads/chromedriver", chrome_options=chrome_opt)
# browser.get("https://www.taobao.com")

#phantomjs 无界面浏览器，多进程情况下phantomjs性能下降严重
browser = webdriver.PhantomJS(executable_path="/Users/xuanren/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.1.c09a295vXgCl0&id=560257961625&cm_id=140105335569ed55e27b&abbucket=16&sku_properties=10004:709990523")

print(browser.page_source)
browser.quit()