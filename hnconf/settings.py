# Scrapy settings for hnconf project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'hnconf'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['hnconf.spiders']
NEWSPIDER_MODULE = 'hnconf.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
	'hnconf.pipelines.HNConfPipeline',
]