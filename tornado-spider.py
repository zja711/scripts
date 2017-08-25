from tornado.ioloop import IOLoop
from tornado.gen import coroutine,Return
from tornado.concurrent import Future
from tornado.httpclient import HTTPRequest
try:
    from tornado.curl_httpclient import CurlAsyncHTTPClient as AsyncHTTPClient
except:
    from tornado.httpclient import AsyncHTTPClient
from functools import partial
from datetime import datetime

def async_request(url):
    future = Future()
    def handle_response(response):
        if response.error:
            future.set_result('')
        else:
            future.set_result(len(response.body))
    curl_client = AsyncHTTPClient()
    request = HTTPRequest(url=url,headers={})
    curl_client.fetch(request, handle_response)
    return future

def parse_html(html):
    return html

@coroutine
def get_data(url):
    html = yield async_request(url)
    data = parse_html(html)
    raise Return(data)

def deal_with_data(data):
    pass

@coroutine
def crawler(url):
    from datetime import datetime,timedelta
    _start = datetime.now()
    print('start:',str(_start),'>>>',url)
    data = yield get_data(url)
    deal_with_data(data)
    print('finish:',str(datetime.now()),str(datetime.now()-_start),'>>>',url)
    IOLoop.instance().add_timeout(timedelta(seconds=30),partial(crawler,url))

@coroutine
def fetch_pages(urls):
    for url in urls:
        crawler(url)


def start():
    urls = [
            'http://www.tornadoweb.org/en/stable/guide.html',
            'http://www.tornadoweb.org/en/stable/guide/intro.html',
            'http://www.tornadoweb.org/en/stable/guide/queues.html'
            ]
    IOLoop.instance().add_callback(partial(fetch_pages,urls))
    IOLoop.instance().start()

if __name__ == '__main__':
    start()