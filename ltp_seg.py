# encoding: utf-8

import urllib2
import urllib
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def ltp_stc_seg(text, pattern):
    uri_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = "Q1m0d4M2x1sZNRdm0g0M7qcBtrUrbmaIkMjFKsvI"
    # text = "祝汤教授新年快乐"
    # Note that if your text contain special characters such as linefeed or '&',
    # you need to use urlencode to encode your data
    text = urllib.quote(text)
    format = "plain"
    # pattern = "ws"

    url = (uri_base + "api_key=" + api_key + "&" + "text=" + text + "&" + "pattern=" + pattern + "&"
           + "format=" + format)

    try:
        response = urllib2.urlopen(url)
        content = response.read().strip()
        print content
        return content

    except urllib2.HTTPError, e:
        print >> sys.stderr, e.reason

if __name__ == '__main__':
    test_text = "祝汤教授新年快乐"
    test_pattern = "ws"
    ltp_stc_seg(test_text, test_pattern)
