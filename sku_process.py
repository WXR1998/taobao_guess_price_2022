import time
import requests
from urllib import parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import webbrowser
import logging

import config
import parser
import renderer


def query(keyword: str):
    """
    对一个关键词进行查询，获取其html原始文档
    """

    keyword_encoding = parse.quote(keyword)
    query_url = config.query_url.format(keyword_encoding)

    resp = requests.get(query_url, headers=config.headers).text
    obj = parser.parse(resp)

    return keyword, obj

def parse_skus(obj: dict):
    """
    把html中的原始文档parse成格式化的sku信息
    """

    item_list = obj['mods']['itemlist']
    if 'data' not in item_list:
        return []
    else:
        item_list = item_list['data']['auctions']

    skus = []
    for item in item_list:
        title = item['raw_title']
        price = item['view_price']
        picture_url = item['pic_url']
        if not picture_url.startswith('https'):
            picture_url = 'https:' + picture_url
        skus.append((title, price, picture_url))

    return skus

def batch_get_skus(keywords: list):
    """
    根据搜索关键词列表查询商品信息
    """

    t0 = time.time()
    ex = ThreadPoolExecutor(max_workers=10)
    futures = [ex.submit(query, k) for k in keywords]

    results = [f.result() for f in as_completed(futures)]
    results = [(_[0], parse_skus(_[1])) for _ in results]
    result_dict = dict()

    for keyword, sku_info in results:
        result_dict[keyword] = sku_info
    t1 = time.time()
    logging.info(f'查询商品信息用时 {t1 - t0:.2f} s')

    return result_dict

def render_sku_prices(keywords: list, size: int, candidates: int):
    """
    将所得的价格信息渲染到html网页上，并打开浏览器展示
    """

    result_dict = batch_get_skus(keywords)

    html_context = renderer.render(result_dict, size=size, len_lim=candidates)
    tmp_html_name = os.path.join(config.root_path, 'templates', 'tmp.html')
    with open(tmp_html_name, 'w') as fout:
        fout.write(html_context)

    webbrowser.open(f'file://{tmp_html_name}', new=1, autoraise=True)