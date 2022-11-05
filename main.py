import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import argparse
import logging
logging.basicConfig(level=logging.INFO)

import config
import ocr
import sku_process
import utils

ap = argparse.ArgumentParser(description='淘宝双十一猜价格助手')
ap.add_argument('--input', type=str, required=False, help='可选，输入图片的文件名，请将图片放置在 root/image/ 目录下。如果不提供，则默认为该目录下最新的文件。')
ap.add_argument('--size', type=int, default=config.image_size, help='可选，结果网页上图片的大小(px)，默认为200。')
ap.add_argument('--candidates', type=int, default=config.candidates, help='可选，结果网页上每个商品的候选数目，默认为10。')

if __name__ == '__main__':
    os.makedirs(config.sku_image_path, exist_ok=True)
    os.makedirs(config.input_image_path, exist_ok=True)

    args = ap.parse_args()
    input_filename = args.input
    size = args.size
    candidates = args.candidates

    if input_filename is None:
        input_filename = utils.get_latest_file(config.input_image_path)

    sku_list = ocr.get_sku_list(os.path.join(config.input_image_path, input_filename))
    sku_process.render_sku_prices(
        sku_list, 
        size=size, 
        candidates=candidates, 
        title=f'{os.path.basename(input_filename)} 的识别结果'
    )