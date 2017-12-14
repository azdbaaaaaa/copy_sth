START_PAGE_NUMBER = 1
URL = 'https://www.lagou.com/jobs/positionAjax.json'
BASE_URL = 'https://www.lagou.com/jobs'
header1 = {
    'user-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'SSL': 'TLSv1.2 (TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256)',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Code': '0',
#    'Referer': 'https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput='.format(quote(keyword.encode('utf-8'))),
}

