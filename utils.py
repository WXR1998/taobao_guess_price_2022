import os
import glob

def get_latest_file(path: str):
    """
    获取路径下最新的文件
    """
    files = []
    for f in glob.glob(os.path.join(path, '*')):
        files.append((os.path.getmtime(f), f))
    files.sort()
    
    if len(files) > 0:
        return files[-1][1]
    return None