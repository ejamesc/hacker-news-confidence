# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import os

path = os.path.join(os.getcwd(), "index.html")

header = u"""\
<html>
    <head>
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
        <title>HN Confidence</title>
    </head>
    <body>
        <h1>Hacker News - Confidence</h1>
        <ol>
"""

tail = u"""\
</ol>
</body></html>
"""

class HNConfPipeline(object):
    def __init__(self):
        self.file = open(path, 'w')
        self.file.write(header)

    def process_item(self, item, spider):
        line = u"<li>%s (%s votes, %s comments)</li>\n" % (item['title'], item['vote'], item['comment'])
        self.file.write(line.encode('ascii', 'xmlcharrefreplace'))
        return item

    def close_spider(self, spider):
        self.file.write(tail)
        self.file.close()
