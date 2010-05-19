import urllib, urllib2, cookielib
import re

required_auth = {'uid': 'text', 'password': 'password', 'auth_id': 'text'}

def get_future_transactions(auth, until=None):
    return [(10.13, 'ILS', datetime.datetime())]

def get_balance(auth):
    opener, user_dir = _login(**auth)

    return (10.13, 'ILS')

def _login(uid, password, auth_field):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPRedirectHandler)
    # mimic firefox 3.6 on windows 7
    # currently this isn't needed, but just for case...
    #opener.addheaders = [
    #                     ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
    #                     ("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.2) Gecko/20100115 Firefox/3.6"),
    #                     ("Accept-Language", "en-us,en;q=0.5"),
    #                     ("Accept-Encoding", "gzip,deflate"),
    #                     ("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.7"),
    #                     ("Keep-Alive", 300),
    #                     ("Connection", "keep-alive"),
    #                     ("Cache-Control", "max-age=0")
    #                    ]

    # gether required cookies from the login form page
    result = opener.open('https://hb2.bankleumi.co.il/H/login.html')

    # post the login details
    values = {'uid': '', 'password': '', 'auth_field': '', 'command': 'login', 'system': 'Test'}
    data = urllib.urlencode(values)
    opener.open('https://hb2.bankleumi.co.il/InternalSite/Validate.ASP', data)
    # the above url performs client-side (javascript) redirect to the following:
    opener.open('https://hb2.bankleumi.co.il/InternalSite/RedirectToOrigURL.asp?site_name=leumi&secure=1')
    # the above url performs client-side redirect to the following:
    result = opener.open('https://hb2.bankleumi.co.il/eBank/SSOLogin.aspx?SectorCheck=Override')

    # (Following the posix pathname terminology: "hostname:/directorypath/resource")
    # The last open request is being redirected to the user's leumi homepage, on
    # each login the path to that homepage is different. The directorypath of that
    # path is the base for all the user's pages, therefore it was named user_dir.
    user_dir = re.sub('/[^/]*$', '', result.geturl()) # delete the resource

    # Important: since the user can custom his homepage it's not reliable to
    # extract data from it

    return (opener, user_dir)
