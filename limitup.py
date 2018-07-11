import datetime, re, time, os, sys, sqlite3, random
import requests
import pandas as pd
import tushare as ts

class LimitUp:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), 'data')
        self.header = {
                        "Host": "home.flashdata2.jrj.com.cn",
                        "Referer": "http://stock.jrj.com.cn/tzzs/zdtwdj/zdtList.shtml",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
                      }
        self.columns = [u'代码', u'名称', u'涨停时间', u'最新价（元）', u'涨跌幅（%）', u'成交额（元）', u'振幅（%）', u'换手率（%）', u'五日涨跌幅（%）', u'？？？',
                        u'所属概念（代码）', u'所属概念']

    # 要爬取的js地址
    def getUrl(self, date):
        return 'http://home.flashdata2.jrj.com.cn/limitStatistic/zt/' + date + ".js?_dc=" + str(int(round(time.time() * 1000)))

    # 请求原始内容
    def getData(self, date, retry=5):
        req = requests.get(self.getUrl(date), headers=self.header)
        for i in range(retry):
            try:
                content = req.text
                md_check = re.findall(r'"Data":\[\[',content)
                if content and len(md_check)>0:
                    return content
                else:
                    time.sleep(60)
                    print('failed to get content, retry: {}'.format(i))
                    continue
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
        return None

    # 将原始内容转化为json
    def convertToJson(self, content):
        p = re.compile(r'"Data":(.*)};', re.S)
        if len(content)<=0:
            print('Content\'s length is 0')
            exit(0)
        result = p.findall(content)
        if result:
            try:
                t1 = result[0]
                t2 = list(eval(t1))
                return t2
            except Exception as e:
                print(e)
                return None
        else:
            return None

    # 保存数据至csv文件和sqlite数据库
    def saveData(self, data, date):
        if not data:
            exit()
        df = pd.DataFrame(data, columns=self.columns)
        filename = os.path.join(self.path, date + "_limit_up" + ".csv")
        df.to_csv(filename, encoding='gbk')
        try:
            df.to_sql(date, sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db_limit_up.db')), if_exists='fail')
        except Exception as e:
            print(e)

    # 爬取、保存数据
    def crawlData(self, startDate, endDate):
        date_list = [datetime.datetime.strftime(i,'%Y%m%d') for i in list(pd.date_range(startDate, endDate))]
        for date in date_list:
            if not ts.is_holiday(datetime.datetime.strptime(date,'%Y%m%d').strftime('%Y-%m-%d')):
                print(date)
                content = self.getData(date)
                json = self.convertToJson(content)
                self.saveData(json, date)
                time.sleep(5)
            else:
                print('Holiday')

if __name__ == '__main__':
    lu = LimitUp()
    start = '20160201'
    end = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    if len(sys.argv) > 1:
        start = sys.argv[1]
    if len(sys.argv) > 2:
        end = sys.arv[2]
    lu.crawlData(start, end)