# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import os

#Something hacky
if os.getcwd() == "/home/shadowsun7/webapps/hnconf/htdocs":
    path = os.path.join("/home/shadowsun7/webapps/hnconf_serve/htdocs/", "index.html")
else:
    path = os.path.join(os.getcwd(), "index.html")

header = u"""\
<html>
    <head>
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
        <title>HN Confidence</title>
        <style>
            body {font: 14px Helvetica, Arial, sans-serif;}
            li {margin-bottom: 10px;}
            a {color: #19558D; text-decoration:none;}
            a:hover {text-decoration: underline;}
            span {color: #999;}
        </style>
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
        line = u"<li>%s <span>(%s votes | %s comments)</span></li>\n" % (item['title'], item['vote'], item['comment'])
        self.file.write(line.encode('ascii', 'xmlcharrefreplace'))
        return item

    def close_spider(self, spider):
        self.file.write(tail)
        self.file.close()
