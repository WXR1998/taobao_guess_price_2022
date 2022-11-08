from html.parser import HTMLParser
import json

class TaobaoHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self._data = None

    def handle_data(self, data):
        if data.strip().startswith('g_page_config'):
            json_str = data.strip().split('\n')[0]
            json_str = json_str[json_str.find('{') : -1]
            obj = json.loads(json_str)

            self._data = obj

    def get_data(self):
        return self._data

parser = TaobaoHTMLParser()

def parse(resp: str):
    try:
        parser.feed(resp)
        parser.close()
    except:
        return {}

    return parser.get_data()
