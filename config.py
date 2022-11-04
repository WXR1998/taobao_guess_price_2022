import os

headers = {
    'cookie': '',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.taobao.com/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

query_url = 'https://s.taobao.com/search?q={}&\
        suggest=history_3&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&\
        spm=a21bo.jianhua.201856-taobao-item.2&ie=utf8&\
        initiative_id=tbindexz_20170306&_input_charset=utf-8&wq=&\
        suggest_query=&source=suggest'

image_size = 200
candidates = 10

root_path = os.path.dirname(__file__)
sku_image_path = os.path.join(root_path, 'sku_image')
input_image_path = os.path.join(root_path, 'image')