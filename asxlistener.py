'''

    ASX Listener by Prodge

        github.com/prodge
        prodge.net
        prodge@prodge.net

    Released under the MIT licence

'''
import sys
import re
import json

import requests

from argparse import ArgumentParser
from time import sleep


# Url of the asx search page
BASE_URL = 'http://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes='

# Cells in order of appearance on the asx website
DATA_CELLS = ['price', 'change', 'percent_change', 'bid', 'offer', 'open', 'high', 'low', 'volume']


def compile_url(codes):
    return BASE_URL + ' '.join(codes)

def get_stocks_page_html(codes):
    return requests.get(compile_url(codes)).content

def strip_to_after_prefix(page, prefix):
    '''
    Returns 'page' sliced from the last character in 'prefix' to the end
    Eg. page = 'abcdef', prefix = 'cd', return = 'ef'
    '''
    for i in range(len(page) - len(prefix)):
        if page[i: i+len(prefix)] == prefix:
            return page[i + len(prefix):]
    raise Exception('Could not strip to prefix [{}], you may have used the wrong security code or the ASX page html has changed.'.format(prefix))

def get_page_to_postfix(page, postfix):
    '''
    Returns 'page' sliced from the begining to the first character in 'postfix'
    Eg. page = 'abcdef', prostfix = 'cd', return = 'ab'
    '''
    for i in range(len(page) - len(postfix)):
        if page[i: i+len(postfix)] == postfix:
            return page[: i]
    raise Exception('Could not find postfix, you may have used the wrong security code or the ASX page html has changed.')

def get_content_of_next_tag(page, tag):
    '''
    Finds the next occurance of 'tag' and returns its content
    Note: Only implemented for tags with no inner tags
    Eg.
        page = '<p class="foo">bar</p>'
        tag = 'p'
        return = 'bar'
    '''
    page = strip_to_after_prefix(page, '<{}'.format(tag))
    page = strip_to_after_prefix(page, '>'.format(tag))
    closing_tag = '</{}>'.format(tag)
    content = get_page_to_postfix(page, closing_tag)
    page = strip_to_after_prefix(page, closing_tag)
    return page, content

def get_code_map(page, codes):
    '''
    Given raw html from the asx stock prices page and stock codes,
    returns a list of dicts containing cell contents
    Example output: [{'code':'CBA', 'price': '2.245'...}, {'code':'NAB', 'price': '5.453'...}]
    '''
    code_map = []
    for code in codes:
        this_code_map = {'code': code}
        page = strip_to_after_prefix(page, 'href="/asx/research/company.do#!/{}'.format(code))
        for cell in DATA_CELLS:
            page, this_code_map[cell] = get_content_of_next_tag(page, 'td')
        page = strip_to_after_prefix(page, '</tr>')
        code_map.append(this_code_map)
    return code_map

def strip_breaks(page):
    return str(page).replace('\\r', '').replace('\\n', '').replace('\\t', '')

def parse_args():
    parser = ArgumentParser(description='Displays ASX stock information in a user defined format.')
    parser.add_argument(
        '-r', '--raw',
        dest='raw',
        action='store_const',
        const=True,
        default=False,
        help="Return a raw hash map for user processing."
    )
    parser.add_argument(
        '-s', '--subscribe',
        dest='subscribe',
        type=int,
        default=0,
        help="Subscribe to updates at the given interval (in minutes)."
    )
    parser.add_argument(
        '-c', '--codes',
        dest='codes',
        help="Comma seperated list of security codes."
    )
    parser.add_argument(
        '-f', '--format',
        dest='format',
        help="Format string for displaying stock information."
    )
    parser.add_argument(
        '-o', '--overwrite',
        dest='overwrite',
        action='store_const',
        const=True,
        default=False,
        help="If set subscribe will write over the previous line instead of a new line."
    )
    return parser.parse_args()

def validate_args(args):
    if not args.codes:
        fail_execution('-c option not specified')
    if not (args.raw or args.format):
        fail_execution('Neither -r or -f specified')
    if args.overwrite and not args.subscribe:
        fail_execution('Subscribe (-s) must be activated to use overwrite (-o)')
    if args.raw and args.format:
        fail_execution('Cannot display both raw (-r) and formatted (-f) string')
    if args.overwrite and len(args.codes.split(',')) > 1:
        fail_execution('Overwrite (-o) can only be used with one security code')
    return validate_format_string(args)

def fail_execution(msg):
    print('Fail: {}.'.format(msg))
    sys.exit(1)

def validate_security_codes(codes):
    if len(codes) > 10:
        fail_execution('Cannot display more than 10 security codes at once')
    return codes

def parse_security_codes(codes):
    return validate_security_codes([code.upper() for code in codes.split(',')])

def validate_format_string(args):
    looking_for_next = {'{': '}', '}': '{'}
    looking_for = '{'
    not_looking_for = '}'
    for char in args.format:
        if char == not_looking_for:
            fail_execution('Braces do not ballance correctly in format string')
        if char == looking_for:
            not_looking_for = looking_for
            looking_for = looking_for_next[looking_for]
    return args

def validate_specifiers(specifiers):
    for specifier in specifiers:
        if specifier not in DATA_CELLS + ['code']:
            fail_execution('Invalid format specifier "{}"'.format(specifier))
    return specifiers

def get_specifiers(split_string):
    return validate_specifiers(
        list(map(lambda a: a[1],
            list(filter(lambda a: a[0]%2==1, enumerate(split_string))))))

def merge_lists_into_string(a, b, string):
    if a:
        string += a.pop(0)
    if b:
        string += b.pop(0)
    if a or b:
        string = merge_lists_into_string(a, b, string)
    return string

def get_formatted_string(code, format):
    split = re.split('{|}', format)
    specifiers = get_specifiers(split)
    non_specifiers = list(filter(lambda a: a not in specifiers, split))
    converted_specifiers = list(map(lambda spec: code[spec], specifiers))
    return merge_lists_into_string(non_specifiers, converted_specifiers, '')

def get_formatted_strings(code_map, args):
    return list(map(lambda code: get_formatted_string(code, args.format), code_map))

def print_output(output, overwrite):
    if overwrite:
        print(' '+output, end='\r')
    else:
        print(output)

def display_output(code_map, args):
    if args.raw:
        print_output(json.dumps(code_map), args.overwrite)
    else:
        list(map(lambda s: print_output(s, args.overwrite), get_formatted_strings(code_map, args)))

def main():
    args = validate_args(parse_args())
    codes = parse_security_codes(args.codes)
    running = True
    while running:
        code_map = get_code_map(strip_breaks(get_stocks_page_html(codes)), codes)
        display_output(code_map, args)
        running = args.subscribe
        sleep(args.subscribe*60)
    sys.exit(0)

main()
