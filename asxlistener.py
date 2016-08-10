from urllib3 import urlopen

# Make these command line args
stocks = ['nab', 'mts']

BASE_URL = 'http://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes='

def compile_url(stocks):
    return BASE_URL + ' '.join(stocks)

def get_stocks_page_html(stocks):
    return urlopen(compile_url(stocks)).read()

def strip_to_after_prefix(page, prefix):
    for i in range(len(page) - len(prefix)):
        if page[i:len(prefix)] == prefix:
            return page[i + len(prefix):]
    raise Exception('Could not strip to prefix, ASX page html has changed.')

def get_page_to_postfix(page, postfix):
    for i in range(len(page) - len(postfix)):
        if page[i:len(prefix)] == prefix:
            return page[i: i + len(prefix)]
    raise Exception('Could not find postfix, ASX page html has changed.')

def get_stock_map(page, stocks):
    for stock in stocks:
        page = strip_to_after_prefix(page, '/asx/research/company.d')


