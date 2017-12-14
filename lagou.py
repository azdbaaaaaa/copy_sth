#!/usr/bin/env python
# -*- coding:utf-8 -*-
import constants
import requests
import json
from urllib import urlencode, quote
import sys
reload(sys)
sys.setdefaultencoding('utf8')


cities = ['北京', '上海', '深圳']

def get_params(city):
    params = {'city': city, 'needAddtionalResult': 'false', 'isSchoolJob': 0}
    return params


url = 'https://www.lagou.com/jobs/positionAjax.json'
# url_list=[]
# for city in cities:
#     url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false&isSchoolJob=0'.format(quote(city.encode('utf-8')))
#     url_list.append(url)
# print url_list

#city = ['上海']
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
#               TG_TRACK_CODE='index_navigation',
)

# salaries = ['10k-15k', '15k-20k']
#params = {'city': city, 'needAddtionalResult': 'false', 'isSchoolJob': 0}
#Form_data = {'first': 'true', 'pn': 1, 'kd': u'测试'}
keyword = u'测试'
headers = {
    'user-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'SSL':'TLSv1.2 (TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256)',
'X-Requested-With':'XMLHttpRequest',
'X-Anit-Forge-Code':'0',
'Referer':'https://www.lagou.com/jobs/list_%E6%B5%8B%E8%AF%95?labelWords=&fromSearch=true&suginput='.format(quote(keyword.encode('utf-8'))),
#'Referer':'https://www.lagou.com/jobs/list_%keyword?labelWords=&fromSearch=true&suginput=' %keyword,
}

# print quote(keyword.encode('utf-8'))
# print 'https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput='.format(quote(keyword.encode('utf-8')))
# print 'end'
# def get_page(url, page_num, keyword):
#     if pageno == 1:
#         boo = 'true'
#     else:
#         boo = 'false'
#
#     page_data = {'first': boo,
#                  'pn': page_num,
#                  'keyword': keyword
#                  }
#     page = requests.post(url, page_data)
#     return page.json()


def get_page(page_num, keyword):
    if page_num == 1:
        boo = 'true'
    else:
        boo = 'false'

    page_data = {'first' : boo,
                 'pn' : page_num,
                 'kd' : keyword

    }
    return page_data


def MyRequest(page_num,keyword):
    aa = []
    for city in cities:
        r = requests.post(url, cookies=cookies, headers=headers, params=get_params(city), data=get_page(page_num,keyword))
        json = r.json()
        positionresult = json.get('content').get('positionResult')
        aa.append(positionresult)
    return aa

def get_info_from_json(json):
    positionresult = json.get('content').get('positionResult')
    content_positionResult_result = positionresult.get('result')
    total_num = positionresult.get('totalCount')
    return content_positionResult_result,  total_num

# def get_total_page(totalCount):
#     return totalCount / 15

for city in cities:
    page_num = 1
    r = requests.post(url, cookies=cookies, headers=headers, params=get_params(city), data=get_page(page_num,keyword))
    json = r.json()
    # result, total_num = get_info_from_json(json)
    positionresult = json.get('content').get('positionResult')
    result = positionresult.get('result')
    total_num = positionresult.get('totalCount')
    # total_page = get_total_page()
    total_page = int(total_num/15)
    print "total_num is %d" %total_num
    print "total_page is %d" %total_page

    for page_num in range(1, total_page):
        r = requests.post(url, cookies=cookies, headers=headers, params=get_params(city), data=get_page(page_num,keyword))
        json = r.json()
#        print json
        content_positionResult_result = json.get('content').get('positionResult').get('result')
        get_company_info(content_positionResult_result)
        # for index, data in enumerate(content_positionResult_result):
        #     city, district, companyId, companyFullName, salary, positionName = get_company_info(data)


#    print result[index]['companyId']
# total_num = json['content']['positionResult']['totalCount']
# total_page = int(total_num/15)

def get_company_info(content_positionResult_result_list):
    for index, data in enumerate(content_positionResult_result_list):
        city = data.get('city')
        district = data.get('district')
        companyId = data.get('companyId')
        companyFullName = data.get('companyFullName')
        salary = data.get('salary')
        positionName = data.get('positionName')
        # mysql.insert()
        # result_list.append({'city': city, 'district': district, 'companyId': companyId, 'companyFullName': companyFullName, salary, positionName})
    return true
