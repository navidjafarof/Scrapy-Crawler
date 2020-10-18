def basic_url_generator(name):
    return 'http://www.fipiran.com/Symbol/HistoryPrice?symbolpara=' + name


def crawl_url_generator(name, row_number, page_number):
    return 'http://www.fipiran.com/Symbol/HistoryPricePaging?symbolpara=' + str(name) + '&_search=false&nd=1602018067855&rows=' + str(row_number) + '&page=' + str(page_number) + '&sidx=id&sord=desc'
