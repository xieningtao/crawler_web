# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
from selenium import webdriver
import time
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options

class TestxntSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TestxntDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    driver = None

    @classmethod
    def from_crawler(cls, crawler):
        logging.debug("method->from_crawler")
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        logging.debug("method->process_request request+ "+str(request))
        if "huaban.com" in request.url:
            driver = webdriver.Chrome();
            # driver = webdriver.PhantomJS(executable_path="/Users/mac/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")
            driver.get(request.url)
            logging.debug("method->process_response huaban.com+ " + str(request.url))
            time.sleep(3)
            originResult = HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request)
            # logging.debug("another page : " + driver.page_source)
            return originResult
        # elif "weibo.com" in request.url:
        #     # driver = webdriver.Chrome();
        #     driver = webdriver.PhantomJS(executable_path="/Users/mac/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")
        #     driver.get(request.url)
        #     # driver.get("https://weibo.com/u/1304494805?is_all=1")#街拍美
        #     # driver.get("https://weibo.com/u/3757458303?is_all=1")#街拍摄美
        #     # real_url = request._meta["redirect_urls"][0]
        #     # driver.get(real_url)
        #     time.sleep(5)
        #     originResult = HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request)
        #     # logging.debug("another page : " + driver.page_source)
        #     return originResult
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        logging.debug("method->process_response request+ " + str(request))
        if "www.3ajiepai.com" in request.url:
            driver = webdriver.Chrome();
            # driver = webdriver.PhantomJS(executable_path="/Users/mac/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")
            driver.get(request.url)
            logging.debug("method->process_response three_m+ " + str(request.url))
            time.sleep(3)
            originResult = HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request)
            # logging.debug("another page : " + driver.page_source)
            return originResult
        elif "passport.weibo.com" in request.url:
            driver = webdriver.Chrome();
            # driver.get(request.url)
            # driver.get("https://weibo.com/u/1304494805?is_all=1")#街拍美
            # driver.get("https://weibo.com/u/3757458303?is_all=1")#街拍摄美
            real_url=request._meta["redirect_urls"][0]
            driver.get(real_url)
            time.sleep(5)
            originResult = HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request)
            # logging.debug("another page : " + driver.page_source)
            return originResult
        elif "id_91374690" in request.url:
            driver = webdriver.PhantomJS(executable_path="/Users/mac/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")
            driver.get(request.url)
            time.sleep(1)
            element = driver.find_element_by_css_selector(".videos-list .v-link")
            el_tag = element.find_element_by_tag_name("a")
            logging.debug("element: "+str(el_tag))
            el_tag.click();
            time.sleep(5)

            originResult = HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request)
            driver.switch_to.window(driver.window_handles[1])
            logging.debug("another page : " + driver.page_source)
            return originResult
        elif "dict.youdao.com" in request.url:
            driver = webdriver.Chrome();
            # driver = webdriver.PhantomJS(executable_path="/Users/mac/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")
            driver.get("http://id.tudou.com/i/id_91374690")
            logging.debug("before click window handler: "+str(driver.current_window_handle))
            time.sleep(3)
            # element = driver.find_element_by_id("nav").find_elements_by_tag_name("ul")[1].find_elements_by_tag_name("li")[6].find_element_by_tag_name("a")
            # element.click();
            # time.sleep(5)

            element = driver.find_element_by_css_selector(".videos-list .v-link")
            el_tag = element.find_element_by_tag_name("a")
            logging.debug("element: " + str(el_tag))
            el_tag.click();
            time.sleep(3)
            logging.debug("after click window handler: " + str(driver.current_window_handle))
            driver.switch_to.window(driver.window_handles[1])
            logging.debug("another page : " + driver.title)
            # driver.quit()
            return HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request)

        elif "www.meipai.com" in request.url:
            driver = webdriver.Chrome();
            # driver = webdriver.PhantomJS(executable_path="/Users/mac/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")
            driver.get("http://www.meipai.com/medias/hot")
            logging.debug("before click window handler: " + str(driver.current_window_handle))
            time.sleep(3)
            # element = driver.find_element_by_id("nav").find_elements_by_tag_name("ul")[1].find_elements_by_tag_name("li")[6].find_element_by_tag_name("a")
            # element.click();
            # time.sleep(5)
            preHandler = driver.current_window_handle;
            elements = driver.find_elements_by_class_name("content-l-video")
            for element in elements:
                driver.execute_script("window.scrollBy(0,200)")
                time.sleep(3)
                element.click()
                time.sleep(3)
                logging.debug("after click window handler: " + str(driver.current_window_handle))
                driver.switch_to.window(driver.window_handles[1])
                logging.debug("another page : " + driver.title)
                videoTag = driver.find_element_by_tag_name("video");
                logging.debug("videoTag : " + videoTag.get_attribute("src"))
                driver.close()
                driver.switch_to.window(preHandler)
                time.sleep(3)
            # driver.quit()
            return HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request)
        elif "www.pearvideo.com" in request.url:
            # chrome_options = Options()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            # driver = webdriver.Chrome(chrome_options=chrome_options,executable_path="/Users/mac/Desktop/chromedriver");
            if self.driver is None:
                mac_phantomjs_path="/Users/mac/Desktop/chromedriver"
                linux_phantomjs_path="/root/application/chromedriver"
                # self.driver = webdriver.PhantomJS(executable_path=mac_phantomjs_path)
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=linux_phantomjs_path);

                logging.info("create drive")
            logging.info("request url: "+request.url)
            self.driver.get(request.url)
            time.sleep(3)
            logging.info("page_source: "+self.driver.page_source)
            return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)
        else:
            return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

