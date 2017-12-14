#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import class_sth
import requests
import sys
import pymysql
import constants
from bs4 import BeautifulSoup
import logging
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
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




positionId = class_sth.execute('select positionId from jobinfo')
print positionId

cookies = dict(user_trace_token='20170908112439-3fa23357-9445-11e7-9139-5254005c3644',
               LGUID='20170908112439-3fa2397e-9445-11e7-9139-5254005c3644',
               X_HTTP_TOKEN='5bc01e7b558d5364b042c1ad7229da33',
               JSESSIONID='ABAAABAAAIAACBIB819299D9C3E9E314144C15FE5DA6F99',
               index_location_city='%E4%B8%8A%E6%B5%B7',
               _putrc='494B857499965BF6',
               login='true',
               unick='%E7%8E%8B%E6%98%A5%E8%8B%97',
               showExpriedIndex='1',
               showExpriedCompanyHome='1',
               showExpriedMyPublish='1',
               hasDeliver='51',
               _gid='GA1.2.723762763.1505738034',
               _ga='GA1.2.1159525725.1504840650',
#               PRE_LAND='https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3160262.html',
               LGSID='20170919200446-bab23e0b-9d32-11e7-91ab-5254005c3644',
               LGRID='20170919200447-bb4264eb-9d32-11e7-91ab-5254005c3644',
               Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6='1504840651, 1505269875, 1505269887, 1505269892',
               Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6='1505822687',
               )


def create_table():
    try:
        class_sth.execute('DROP TABLE IF EXISTS jobdetails;')
        class_sth.execute('''CREATE TABLE IF NOT EXISTS jobdetails(
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        positionId INT NOT NULL,
        jobname CHAR(50) NOT NULL,
        companyname CHAR(100) NOT NULL,
        position_lable CHAR(100) NOT NULL,
        job_request CHAR(100) NOT NULL,
        jobdescription VARCHAR(500) NOT NULL,
        advantage VARCHAR(500) NOT NULL,
        job_address CHAR(100) NOT NULL);''')
        return True
    except Exception, e:
        print e
        return False


#create_table()


for i in range(len(positionId)):
#    req_JD = class_sth.MySession()
#    JD = req_JD.get(url=constants.BASE_URL + '/' + str(positionId[i][0]) + '.html', cookies=class_sth.cookies)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
               'Referer':'https://www.lagou.com/jobs/{}.html'.format(positionId[i][0])
    }
    url=constants.BASE_URL + '/{}.html'.format(positionId[i][0])
    print positionId[i][0]
    print url
    JD = requests.get(url=url, cookies=cookies, headers=headers, allow_redirects=False)
    logging.debug('**********************{}************'.format(positionId[i][0]))
    logging.debug('请求的url为[{}]'.format(url))
    logging.debug('返回码为[{}]'.format(JD.status_code))
    if JD.status_code > 200:
        continue
#    print JD.text
    soup = BeautifulSoup(JD.text,'html.parser')
#    print soup.prettify()
#     print soup.div
#     print type(soup.div)
#     print soup.body.div
#    print soup.find_all('div', 'job-name')
    logging.debug('job-name的标签为:[{}]'.format(soup.find('div', 'job-name')))
    job_name = soup.find('div', 'job-name').get('title') or ''
    companyname = soup.find('div', 'company').string or ''
#    print soup.find_all('ul', 'position-label clearfix')

    tmp1 = soup.find('ul', 'position-label clearfix')
    position_lables = tmp1.find_all('li')
    position_lables_string = ''
    for table in position_lables:
        position_lables_string += table.text + '/'
#        aa = table.text
    position_lables_string = position_lables_string.replace(',','，').replace("'",'’').replace('.','。')
    print position_lables_string
    # bv = [table.text for table in tables]
    # print 2
    tmp2 = soup.find('dd', 'job_request')
    job_requests = tmp2.find_all('span')
    job_request_string = ''
    for request in job_requests:
        job_request_string += request.text
    job_request_string = job_request_string.replace(',','，').replace("'",'’').replace('.','。')
    print job_request_string

    tmp3 = soup.find('dd', 'job_bt')
    job_description = tmp3.find_all('p')
    job_description_string = ''
    for description in job_description:
        job_description_string += description.text
    job_description_string = job_description_string.replace(',','，').replace("'",'’').replace('.','。')
    print job_description_string

    tmp4 = soup.find('dd', 'job-advantage')
    job_advantage = tmp4.find_all('p')
    job_advantage_string = ''
    for advantage in job_advantage:
        job_advantage_string += advantage.text
    job_advantage_string = job_advantage_string.replace(',','，').replace("'",'’').replace('.','。')
    print job_advantage_string

    tmp5 = soup.find('div', 'work_addr')
    job_address = tmp5.get_text().strip().replace(' ', '')
    job_address_string = job_address.replace('\n','')
    print job_address_string

    sql = '''insert into jobdetails (positionId, jobname, companyname, position_lable, job_request, jobdescription, advantage, job_address) values(%d, '%s', '%s', '%s', '%s', '%s', '%s','%s')'''% (positionId[i][0], job_name, companyname, position_lables_string, job_request_string, job_description_string,  job_advantage_string, job_address_string)
    logging.debug('执行的sql语句为:[{}]'.format(sql))
    class_sth.execute(sql)



# def get_jobdetail(html):
#     soup = BeautifulSoup(html,'html.parse')
#     jobName = soup.xxx
#     companyname = soup.xxx
#     position_lable = soup.xxx
#     jobdescription = soup.xxx
#     job_due = soup.xxx
#     advantage = soup.xxx
#     job_address = soup.xxx
#     review_anchor = soup.xxx


if __name__ == '__main__':
    create_table()




