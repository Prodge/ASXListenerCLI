'''

    ASX Listener by Prodge

        github.com/prodge
        prodge.net
        prodge@prodge.net

    Released under the MIT licence

'''
import requests

# Url of the asx search page
BASE_URL = 'http://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes='

# Cells in order of appearance on the asx website
DATA_CELLS = ['price', 'change', 'percent_change', 'bid', 'offer', 'open', 'high', 'low', 'volume']

def compile_url(stocks):
    return BASE_URL + ' '.join(stocks)

def get_stocks_page_html(stocks):
    return requests.get(compile_url(stocks)).content

def strip_to_after_prefix(page, prefix):
    for i in range(len(page) - len(prefix)):
        if page[i: i+len(prefix)] == prefix:
            return page[i + len(prefix):]
    raise Exception('Could not strip to prefix [{}], ASX page html has changed.'.format(prefix))

def get_page_to_postfix(page, postfix):
    for i in range(len(page) - len(postfix)):
        if page[i: i+len(postfix)] == postfix:
            return page[: i]
    raise Exception('Could not find postfix, ASX page html has changed.')

def get_content_of_next_tag(page, tag):
    page = strip_to_after_prefix(page, '<{}'.format(tag))
    page = strip_to_after_prefix(page, '>'.format(tag))
    closing_tag = '</{}>'.format(tag)
    content = get_page_to_postfix(page, closing_tag)
    page = strip_to_after_prefix(page, closing_tag)
    return page, content

def get_stock_map(page, stocks):
    stock_map = {}
    for stock in stocks:
        this_stock_map = {}
        page = strip_to_after_prefix(page, 'href="/asx/research/company.do#!/{}'.format(stock.upper()))
        for cell in DATA_CELLS:
            page, this_stock_map[cell] = get_content_of_next_tag(page, 'td')
        page = strip_to_after_prefix(page, '</tr>')
        stock_map[stock] = this_stock_map
    return stock_map

def strip_breaks(page):
    return str(page).replace('\\r', '').replace('\\n', '').replace('\\t', '')

def main():
    # Make these command line args
    stocks = ['nab', 'mts']

    stock_map = get_stock_map(strip_breaks(get_stocks_page_html(stocks)), stocks)
    print(stock_map)

main()
