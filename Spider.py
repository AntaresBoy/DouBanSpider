"""
爬虫：
1、明确目的
2、找到数据对应的网页
3、分析网页结构找到数据在网页中所在的标签位置
4、模拟http请求，向服务器发送这个请求，获取服务器返回给我们的html
5、用正则表达式提取我们的数据
"""
from urllib import request
import re
class Spider:
    url = "https://m.huya.com/g/lol"
    root_patten = '<span class="txt">([\s\S]*?)</li>'
    name_patten = '<i class="nick" title=[\s\S]*?>([\s\S]*?)</i>'
    number_patten = '<i class="js-num">([\s\S]*?)</i>'
    #返回一个htmls文件
    def __fetch_content(self):
        response = request.urlopen(Spider.url)
        html = response.read()
        htmls = str(html, encoding="utf-8")
        return htmls

    # 解析htmls文件
    def __analysis(self, htmls):
        root_html = re.findall(Spider.root_patten, htmls)
        name_num_list=[]
        for html in root_html:
            name = re.findall(Spider.name_patten, html)
            number = re.findall(Spider.number_patten, html)
            name_num_dict = {"name":name, "number":number}
            name_num_list.append(name_num_dict)
        return name_num_list

    def __refine(self, name_list):
        lambda_dict = lambda item:{"name":item["name"][0], "number":item["number"][0]} # lambda表达式返回一个函数

        return map(lambda_dict, name_list)# map类型的对象

    def __sort(self,item_list):
        # key表示按照什么内容开始排序，reverse=True表示从大到小排序
        item_list = sorted(item_list, key=self.__sort_seed,reverse=True)
        return item_list

    def __sort_seed(self,name_num_list):
        r = re.findall("\d*\.*\d*", name_num_list["number"])# 将列表中“”number属性的所有数字提取出来，返回一个列表
        print(r)
        number = float(r[0])

        if "万" in name_num_list["number"]:
            number *= 10000
        return number

    def __show(self,sort_list):
        for rank in range(0, len(sort_list)):
            print("rank" + str(rank+1) + ":" + "主播：" + sort_list[rank]["name"] + "--->" + sort_list[rank]["number"])

    def go(self):
        htmls = self.__fetch_content()
        name_num_list = self.__analysis(htmls)
        item_list = list(self.__refine(name_num_list))

        sort_list = self.__sort(item_list)

        self.__show(sort_list)

spider = Spider()
spider.go()
