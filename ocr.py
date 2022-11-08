import easyocr
import os
import cv2
import logging
import time
import re

import config

def sku_name_filter(sku_name: str):
    """
    对某些sku的名称进行手工修改
    """
    if not sku_name.endswith(' '):
        sku_name = sku_name + ' '

    # k9 大概率是由 kg 误识别而来
    sku_name = re.sub(r'k9[^\d]', lambda m: 'kg' + m.group(0)[-1], sku_name)
    # m1 大概率是由 ml 误识别而来
    sku_name = re.sub(r'm1[^\d]', lambda m: 'ml' + m.group(0)[-1], sku_name)
    # GL/Gl/G1 大概率是由 6L 误识别而来
    sku_name = re.sub(r'G[Ll1][^\d]', lambda m: '6L' + m.group(0)[-1], sku_name)
    # 以1结尾的数字大概率是由 *L 误识别而来
    sku_name = re.sub(r'(\d+?)1[^\d]', lambda m: m.group(0)[:-2] + 'L' + m.group(0)[-1], sku_name)
    # 以9结尾的数字大概率是由 *g 误识别而来
    sku_name = re.sub(r'(\d+?)9[^\d]', lambda m: m.group(0)[:-2] + 'g' + m.group(0)[-1], sku_name)

    return sku_name.strip()

def get_sku_list(path: str, prob_thres: float = 0.3):
    """
    从path jpg图像文件中获取所有的商品名，筛选掉置信度较低的文字
    """

    logging.info(f'从文件 {path} 中执行OCR')
    t0 = time.time()
    decoder = easyocr.Reader(['ch_sim', 'en'])
    img = cv2.imread(path)
    img = cv2.resize(img, (603, 1304))
    result = decoder.readtext(img)

    # 筛选概率较高的bbox，筛选长度足够的商品名称
    # 对sku的名称中的一些pattern进行手工修正
    result = [(sku_name_filter(_[1]), _[0]) for _ in result if _[2] > prob_thres]
    result = [_ for _ in result if len(_[0]) >= 4]

    # 只筛选是商品的文字
    answer_idx = None
    for idx, value in enumerate(result):
        text, bbox = value
        if '晋级' in text or '概率' in text or '总价' in text or '接近' in text or '提交选择' in text:
            answer_idx = idx + 1
            break
    if answer_idx is not None:
        result = result[answer_idx:]
    
    logging.info(f'OCR结果\t{str(result)}')

    # 将商品图片存到对应的文件夹
    for text, bbox in result:
        x_min = int(bbox[0][0])
        x_max = int(bbox[1][0])
        y_min = int(bbox[0][1])
        y_max = int(bbox[2][1])
        y_min -= 150
        cropped = img[y_min:y_max, x_min:x_max]
        if cropped.shape[0] * cropped.shape[1] > 0:
            cv2.imwrite(os.path.join(config.sku_image_path, f'{text}.jpg'), cropped)
    
    # bbox可以舍弃了，只需返回所有的商品名
    result = [_[0] for _ in result if not '已选' in _[0]]
    t1 = time.time()
    logging.info(f'OCR用时 {t1 - t0:.2f} s')

    return result