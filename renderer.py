from jinja2 import Environment, FileSystemLoader
import os
import config

def render(result_dict: dict, size: int, len_lim: int, title: str):
    def lim(l: list):
        if len(l) > len_lim:
            l = l[:len_lim]
        return l

    env = Environment(
        loader=FileSystemLoader(f'{os.path.dirname(__file__)}/templates'),
    )
    data = {
        'data': {
            keyword: {
                'img_src': 'file://' + os.path.join(config.sku_image_path, f'{keyword}.jpg'),
                'sku_list': lim([{
                    'title': s[0],
                    'price': int(float(f'{float(s[1]):.2g}')),
                    'img_src': s[2]
                } for s in result_dict[keyword]])
            } for keyword in result_dict
        },
        'size': size,
        'title': title
    }
    template = env.get_template('index.html')
    return template.render(**data)