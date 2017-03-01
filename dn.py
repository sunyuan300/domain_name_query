import requests
from bs4 import BeautifulSoup
import re
class Spider():
    def __init__(self):
        self.header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
        self.start_dataurl="https://who.is/whois/"
        self.start_jsonurl="https://who.is/api/whois/checkDomainAvailability/"
        self.data=""
        self.result=None
    def getdata(self,dn):
        mg=re.compile('var pendingDomainCheck = "(.*?)";')
        url=self.start_dataurl+dn
        data_response=requests.get(url,headers=self.header) 
        data_response.encoding="utf-8"
        data_html=data_response.text
        soup=BeautifulSoup(data_html,"html.parser")
        self.data=mg.findall(str(soup("script")[3]))[0]
    def getjson(self,dn):
        form_data={"pendingDomainCheck":self.data}
        jsonurl=self.start_jsonurl+dn
        json_response=requests.post(jsonurl,headers=self.header,data=form_data)
        #print(json_response.json())
        self.result=json_response.json()["domains"][dn]["avail"]
    def work(self,dn):
        self.getdata(dn)
        self.getjson(dn)
        if self.result==False:
            print("%s-------->已注册"%dn)
        elif self.result==True:
            print("%s-------->未注册"%dn)
        else:
            print("出错了。。。。。。。")
if __name__=="__main__":
    spider=Spider()
    while True:
        dn=input("请输入要查询的域名(输入q或Q可退出程序)：")
        if dn=="q" or dn=="Q":
            print("退出成功！")
            break
        else:
            print("正在查询，请稍等！")
            spider.work(dn)
            print("\n\n")
    
    
        
