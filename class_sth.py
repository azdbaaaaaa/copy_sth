#!/usr/bin/env python
# -*- coding:utf-8 -*-

import constants
import requests
import json
from urllib import urlencode, quote
import pymysql
import sys
import logging
from time import sleep
reload(sys)
sys.setdefaultencoding('utf8')

#cities = ['北京', '上海', '深圳']


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='class_sth.log',
                filemode='w')

#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')


def get_params(city):
    params = {'city': city, 'needAddtionalResult': 'false', 'isSchoolJob': 0}
    return params


cookies = dict(user_trace_token='20170908112439-3fa23357-9445-11e7-9139-5254005c3644',
               LGUID='20170908112439-3fa2397e-9445-11e7-9139-5254005c3644',
               JSESSIONID='ABAAABAAAIAACBIB819299D9C3E9E314144C15FE5DA6F99',
               X_HTTP_TOKEN='5bc01e7b558d5364b042c1ad7229da33',
               _putrc='494B857499965BF6',
               login='true',
               unick='%E7%8E%8B%E6%98%A5%E8%8B%97',
               showExpriedIndex='1',
               showExpriedCompanyHome='1',
               showExpriedMyPublish='1',
               hasDeliver='51',
               _gid='GA1.2.1224863091.1505042857',
               _ga='GA1.2.1159525725.1504840650',
               Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6='1504840651',
               Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6='1505134352',
               LGSID='20170911195822-82c9c706-96e8-11e7-8f1a-525400f775ce',
               LGRID='20170911205950-18f7ac11-96f1-11e7-8f40-525400f775ce',
               SEARCH_ID='1f97f27a1f5d47298217bd5eba24dc8b',
               index_location_city='%E4%B8%8A%E6%B5%B7',
               )

#cookies = dict (ticketGrantingTicketId='_CAS_TGT_TGT-748a3c1af1534c4b835bc24017d2f650-20171007212436-_CAS_TGT_')


#keyword = u'测试'
# headers = {
#     'user-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'SSL': 'TLSv1.2 (TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256)',
#     'X-Requested-With': 'XMLHttpRequest',
#     'X-Anit-Forge-Code': '0',
#     'Referer': 'https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput='.format(quote(keyword.encode('utf-8'))),
# }


def get_page(page_num, keyword):
    if page_num == 1:
        boo = 'true'
    else:
        boo = 'false'

    page_data = {'first': boo,
                 'pn': page_num,
                 'kd': keyword
                 }
    return page_data


def execute(sql):
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'lagou',
        'charset': 'utf8mb4'
    }
    with pymysql.connect(**config) as cur:
        cur.execute(sql)
        return cur.fetchall()


def create_table():
    try:
        execute('DROP TABLE IF EXISTS jobinfo;')
        execute('''CREATE TABLE IF NOT EXISTS jobinfo(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                city VARCHAR(50) NOT NULL,
                district VARCHAR(50) NOT NULL,
                companyId INT NOT NULL,
                companyFullName VARCHAR(50) NOT NULL,
                salary VARCHAR(50) NOT NULL,
                positionId INT NOT NULL,
                positionName VARCHAR(50) NOT NULL);'''
                )
        return True
    except Exception, e:
        print e
        return False


class MySession(object):
    def __init__(self):
        self.session = requests.session()

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def get(self,*args,**kwargs):
        return self.session.get(*args,**kwargs)


class FindJob(object):
    def __init__(self, city, keyword):
        self.city = city
        self.keyword = keyword
#        self.content_positionResult_result_list = []
        self.get_totalpage()

    def get_totalpage(self):
        #        r = requests.post(constants.URL, cookies=cookies, headers=headers, params=get_params(self.city),
        #                          data=get_page(constants.START_PAGE_NUMBER, self.keyword))
        req = MySession()
        header2 = {'Referer': 'https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput='.format(quote(self.keyword.encode('utf-8'))),
        }
        headers = dict(constants.header1.items()+header2.items())
        r = req.post(url=constants.URL, cookies=cookies, headers=headers, params=get_params(self.city),
                     data=get_page(constants.START_PAGE_NUMBER, self.keyword))
        info = r.json()
        positionresult = info.get('content').get('positionResult')
        total_num = positionresult.get('totalCount')
        self.total_page = int(total_num / 15)
        return self.total_page

    def insert_information_to_sql(self, information):
        a = information
        for index, data in enumerate(information):
            city = data.get('city').encode('utf-8')
            district = data.get('district')
            companyId = data.get('companyId')
            companyFullName = data.get('companyFullName')
            salary = data.get('salary')
            positionId = data.get('positionId')
            positionName = data.get('positionName')
            sql1 = '''insert into jobinfo(city, district, companyId, companyFullName, salary, positionId, positionName) values('%s', '%s', %d, '%s', '%s', %d,'%s')'''% (city, district, companyId, companyFullName, salary,  positionId, positionName)
            sql = '''insert into jobinfo(city, district, companyId, companyFullName, salary, positionId, positionName) values('{}', '{}', {}, '{}', '{}', {}, '{}')'''.format(
                    city, district, companyId, companyFullName, salary, positionId, positionName)
            print sql1
            execute(sql1)

    def get_information(self):
        for page_num in range(1, self.total_page):
            #            if page_num < 97:
            #                continue
            header2 = {'Referer': 'https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput='.format(quote(self.keyword.encode('utf-8'))),
        }
            headers = dict(constants.header1.items() + header2.items())
            r = requests.post(constants.URL, cookies=cookies, headers=headers, params=get_params(self.city),
                              data=get_page(page_num, self.keyword))
            logging.debug('返回的json为[{}]'.format(r.json()))
            result = r.json().get('content').get('positionResult').get('result')
            self.insert_information_to_sql(result)
#            sleep(5)
            # self.content_positionResult_result_list.append(r.json().get('content').get('positionResult').get('result'))
        # print self.content_positionResult_result_list
        return


if __name__ == '__main__':
    create_table()
    a = FindJob('上海', '测试')
    # print a.get_totalpage()
    a.get_information()

    # for city in cities:
    #     a = FindJob(city, 'kw')
    #     a_list.append(a)
