import json as real_json

__author__ = 'bromix'

import urllib
import urllib2
from StringIO import StringIO
import gzip


class Response():
    def __init__(self):
        self.headers = {}
        self.code = -1
        self.text = u''
        self.status_code = -1
        pass

    def read(self):
        return self.text

    def json(self):
        return real_json.loads(self.text)

    pass


def _request(method, url,
             params=None,
             data=None,
             headers=None,
             cookies=None,
             files=None,
             auth=None,
             timeout=None,
             allow_redirects=True,
             proxies=None,
             hooks=None,
             stream=None,
             verify=None,
             cert=None,
             json=None):

    if not headers:
        headers = {}
        pass

    proxy_handler = urllib2.ProxyHandler()
    opener = urllib2.build_opener(proxy_handler)

    query = ''
    if params:
        for key in params:
            params[key] = str(unicode(params[key]).encode('utf-8'))
            pass
        query = urllib.urlencode(params)
        pass
    if query:
        url += '?%s' % query
        pass
    request = urllib2.Request(url)
    if headers:
        for key in headers:
            request.add_header(key, str(unicode(headers[key]).encode('utf-8')))
            pass
        pass
    if data:
        if headers.get('Content-Type', '').startswith('application/x-www-form-urlencoded'):
            for key in data:
                data[key] = data[key].encode('utf-8')
                pass
            request.data = urllib.urlencode(data)
            pass
        elif headers.get('Content-Type', '').startswith('application/json'):
            request.data = real_json.dumps(data).encode('utf-8')
            pass
        elif json:
            request.data = real_json.dumps(json).encode('utf-8')
        else:
            if not isinstance(data, basestring):
                data = str(data)
                pass

            if isinstance(data, str):
                data = data.encode('utf-8')
                pass
            request.data = data
            pass
        pass
    request.get_method = lambda: method
    result = Response()
    response = None
    try:
         response = opener.open(request)
         result.headers.update(response.headers)
         result.status_code = response.getcode()
    except urllib2.HTTPError, e:
        from .. import logging

        logging.log_error(e.__str__())
        pass

    if response.headers.get('Content-Encoding', '').startswith('gzip'):
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        result.text = f.read()
        pass
    else:
        result.text = response.read()

    return result


def get(url, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return _request('GET', url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return _request('POST', url, data=data, json=json, **kwargs)


def put(url, data=None, json=None, **kwargs):
    return _request('PUT', url, data=data, json=json, **kwargs)


def delete(url, **kwargs):
    return _request('DELETE', url, **kwargs)
