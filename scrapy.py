#!/usr/bin/env python
# -*- coding: utf-8 -*-

#accountInfos爬取

import requests
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class scrapy(object):
    def __init__(self):
        print u'开始爬取内容'

    #获取网页内容
    def getResource(self, url):
        html = requests.get(url)
        return html.text
    #geteveryclass用来抓取每个课程块的信息
    def geteveryclass(self,source):
        everyclass = re.findall('<tr>(.*?)</tr>',source,re.S)
        return everyclass

    def getAccountInfo(self, accountInfo):
        info = {}
        if accountInfo.find('uploadTime') != -1:
            info['uploadTime'] = re.search(r'uploadTime">(.*?)</td>', accountInfo, re.S).group(1)
            info['accountCode'] = re.search(r'accountCode">(.*?)</td>', accountInfo, re.S).group(1)
            info['creditorCity'] = re.search(r'creditorCity">(.*?)</td>', accountInfo, re.S).group(1)
            info['debtorCity'] = re.search(r'debtorCity">(.*?)</td>', accountInfo, re.S).group(1)
            info['account_yuan'] = re.search(r'account_yuan">(.*?)</td>', accountInfo, re.S).group(1)
            info['currency'] = re.search(r'currency">(.*?)</td>', accountInfo, re.S).group(1)
            return info

    def saveAsTxt(self, infos):
        f = open('accounts.txt', 'a')
        for account in infos:
            f.writelines('uploadTime:' + account['uploadTime'] + '\t')
            f.writelines('accountCode:' + account['accountCode'] + '\t')
            f.writelines('creditorCity:' + account['creditorCity'] + '\t')
            f.writelines('debtorCity:' + account['debtorCity'] + '\t')
            f.writelines('account_yuan:' + account['account_yuan'] + '\t')
            f.writelines('currency:' + account['currency'] + '\n')
        f.close()

if __name__ == '__main__':
    spy = scrapy()
    url = 'http://www.crcrfsp.com/account.do'
    index = spy.getResource(url)
    totleNum = re.findall('pageTotal" value="(.*?)"', index, re.S)[0]
    if totleNum :
        for i in range(int(totleNum)):
            url = 'http://www.crcrfsp.com/account.do' + '?pageNum=' + str(i)
            html = spy.getResource(url)
            table = spy.geteveryclass(html)
            accounts=[]
            for a in table:
                info = spy.getAccountInfo(a)
                if info != None:
                    accounts.append(info)

            spy.saveAsTxt(accounts)

