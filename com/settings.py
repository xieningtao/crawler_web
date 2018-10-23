# -*- coding: utf-8 -*-

# Scrapy settings for testXNT project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'com'

SPIDER_MODULES = ['com.spiders']
NEWSPIDER_MODULE = 'com.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'testXNT (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie': 'SINAGLOBAL=1618305396374.9795.1496912991585; _s_tentry=-; Apache=3563552099314.0625.1539855770645; ULV=1539855770671:21:2:1:3563552099314.0625.1539855770645:1538997930311; TC-V5-G0=784f6a787212ec9cddcc6f4608a78097; TC-Page-G0=841d8e04c4761f733a87c822f72195f3; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; login_sid_t=370c9fe7d2010bf4a5d5ad1d9870af8f; cross_origin_proto=SSL; WBtopGlobal_register_version=030d061db77a53e5; un=389124248@qq.com; appkey=; SCF=AoH65CzQyP0lsDraBgcU-Jz41EywKxxNqU5AYrvo7hURdNL2fhWy0fCoYndgHHVSexLM3ujuSJpH92tY3z5SzO4.; SUHB=0S7Sk8WUZ1SUtK; un=389124248@qq.com; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W5AEhE9j_WnEeSIiw5JIqsw5JpV2heR1K2EShzX12WpMC4odcXt; SUB=_2AkMslA7ldcNxrABXnf4TxWvjaI9H-jyfQWcTAn7uJhMyAxh77m8zqSVutBF-XGbS0qmLS7jDZvpsWX5lPZqdmnYo; UOR=www.huangbowen.net,widget.weibo.com,www.google.com.hk; wb_view_log_6655726689=1536*8641.25',
#     'Host': 'www.weibo.com',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'testXNT.middlewares.TestxntSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
  'com.middlewares.TestxntDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#后面的数字决定pipeline执行的顺序，顺序由低到高
ITEM_PIPELINES = {
   'com.pipelines.TestxntPipeline': 300,
   # 'com.pipelines.BaiduJiepaiImgDownloadPipeline': 301,
   # 'com.pipelines.UploadJiePaiPicPipeline': 302,
}
IMAGES_STORE = 'C:\\Users\\g8876\\Desktop\\jiepai'
# MEDIA_ALLOW_REDIRECTS = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
# ROBOTSTXT_OBEY = False
# COOKIES_ENABLED = False
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
