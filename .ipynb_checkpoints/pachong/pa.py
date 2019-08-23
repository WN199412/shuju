from urllib import request
import re
from time import sleep
import csv


def request_from(qu,page):
    page_url = "https://bj.lianjia.com/ershoufang/%s/pg%d/"%(qu,page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    return request.Request(url=page_url, headers=headers)

def request_data(qu_list,start,end):
    for qu in qu_list:
        item["region"] = chengqu[qu]
        for page in range(start,end+1):
            req = request_from(qu=qu,page=page)
            res = request.urlopen(req)
            print("当期正在请求第%d页...请求%s区"%(page,chengqu[qu]))
            sleep(1)
            yield res.read().decode("utf-8")

def analysis_data(data):
    for html in data:
        pat = re.compile(r'data-is_focus="" data-sl="">.*?</span></div></div></div>',re.S)
        ershou_list = pat.findall(html)
        # print(ershou_list)
        for ershou in ershou_list:
            # print(ershou)

            pat_dire = re.compile(r' </a> .*?</div></div><div class="flood">',re.S)
            zong = pat_dire.findall(ershou)[0].split("|")
            # print(zong)
            item["direction"] = zong[3]
            item["layout"] = zong[1]
            if zong[2].isalnum():

                item["size"] = float(zong[2].split("平米")[0])
            else:
                item["size"] = zong[2].split("平米")[0]

            if zong.__len__() == 5:
                item["renovation"] = zong[4].split("<")[0]
            else:
                item["renovation"] = "其他"
            pat_gar = re.compile(r'" data-el="region">.*? ',re.S)
            item["garden"] = pat_gar.findall(ershou)[0].split(">")[1]
            pat_yer = re.compile(r'<span class="positionIcon"></span>.*?  -  <', re.S)
            year = pat_yer.findall(ershou)[0]
            y = re.findall(r'\d+',year)
            if y.__len__() == 2:
                item["year"] = y[1]

            else:
                item["year"] = 0

            if y.__len__() > 1:
                item["floor"] = y[0]
            else:
                item["floor"] = 0
            pat_dis = re.compile(r' target="_blank">.*?</a', re.S)
            item["district"] = pat_dis.findall(ershou)[0].split(">")[1].split("<")[0]
            pat_pic = re.compile(r'"totalPrice"><span>.*?</span>',re.S)
            item["price"] = pat_pic.findall(ershou)[0].split("<span>")[1].split("</span>")[0]
            pat_dan = re.compile(r'单价.*?元/平米',re.S)
            item["danjia"] = pat_dan.findall(ershou)[0].split("元")[0].split("价")[1]
            yield item

def write_to_csv(data):
    csvfile = open("./ershou1.csv", "a+", encoding="utf-8", newline='')
    writer = csv.writer(csvfile)
    writer.writerow(
        ["region", "direction", "layout", "size", "renovation", "garden", "year", "floor", "district", "price","danjia"])
    for item in data:
        # csv表中每一行就是编程语言中的一个一维列表，所以在这里我们需要将item这个字典转化成列表
        # 创建一个空列表
        row = []
        row.append(item["region"])
        row.append(item["direction"])
        row.append(item["layout"])
        row.append(item["size"])
        row.append(item["renovation"])
        row.append(item["garden"])
        row.append(item["year"])
        row.append(item["floor"])
        row.append(item["district"])
        row.append(item["price"])
        row.append(item["danjia"])
        # 将row列表写入到csv中
        writer.writerow(row)

if __name__ == '__main__':
    item = {}
    chengqu = {"dongcheng":"东城","xicheng":"西城","chaoyang":"朝阳","haidian":"海淀","fengtai":"丰台","tonzhou":"通州","changping":"昌平","daxing":"大兴","shunyi":"顺义","fangshan":"房山"}
    qu_list = ["xicheng","chaoyang","haidian","fengtai","tonzhou","changping","daxing","shunyi","fangshan"]
    content_list = request_data(qu_list,1,100)
    list = analysis_data(content_list)
    write_to_csv(list)
