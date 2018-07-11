# limit-up-stock-crawler
沪深股市涨停板数据爬取器。  
## 运行环境
* Python3
* 需要Requests、Pandas、Tushare等第三方包
* 项目根目录需要建立`data`文件夹  

## 使用方法
在项目根目录执行：
```
python limitup.py [start [end]]  
```
（方括号表示可选参数）  
* `start`：开始日期，格式为YYmmdd，默认值为“20160201”（也是能爬到的最早数据）
* `end`：结束日期，格式为YYmmdd，默认值为今天  

该脚本会爬取这段时间范围内的涨停板数据，自动写入csv文件存入`./data`目录，并写入根目录下的sqlite数据库。