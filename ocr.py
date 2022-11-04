import easyocr
import os
import cv2
import logging
import time

import config

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
    result = [(_[1], _[0]) for _ in result if _[2] > prob_thres]
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
        # 此坐标偏移是为了从文字的bbox获取到商品对应图片的bbox，对于不同分辨率的截图需微调此值
        y_min -= 150
        # y_max -= 40
        cropped = img[y_min:y_max, x_min:x_max]
        if cropped.shape[0] * cropped.shape[1] > 0:
            cv2.imwrite(os.path.join(config.sku_image_path, f'{text}.jpg'), cropped)
    
    # bbox可以舍弃了，只需返回所有的商品名
    result = [_[0] for _ in result if not '已选' in _[0]]
    t1 = time.time()
    logging.info(f'OCR用时 {t1 - t0:.2f} s')

    return result