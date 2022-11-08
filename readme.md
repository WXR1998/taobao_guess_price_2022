# 淘宝2022双十一猜价格游戏助手

## 概览

输入一张游戏过程中的截图，然后助手将自动为您查询截图中所有商品的前若干项的图片、标题和价格，一起显示在一个网页中。

<div align = "center" >
    <img src="docs_image/sample.jpg" height = "600" />
    <br>
    <img src="docs_image/output.png" height = "300" />
</div>

## 使用方法

### 找到cookie

先在根目录创建一个名为`cookie.txt`的文件，然后在**一行**中填写您淘宝网的cookie，不要换行。具体方法可参考其他教程，这里不再赘述。

### 依赖安装

Python 3.9

```shell
pip3 install -r requirements.txt
```

### 运行程序
- 先将输入截图放在`image`目录下，若目录没有则创建一个。
    - 此处收集截图的方法不限，如通过微信手机截图然后保存。但**需要保证文件名和路径不含中文文字**。
- 使用python3，在命令行中
    ```shell
    python3 main.py [--input INPUT_FILE.jpg] [--size int] [--candidates int] [--help]
    ```
    `[]`中的内容为可选，参数详细信息可见`--help`中的说明。
    - 第一次运行需要下载预训练模型，所以如果出现`http.client.RemoteDisconnected: Remote end closed connection without response`的报错，**需要挂代理**。
- 稍等片刻，一个显示所有商品信息的网页将自动弹出。
- 由于电脑配置、GPU等差异，程序运行用时可能在五到十秒不等。查询到的商品的价格的方差也较大，该问题暂时没有好的处理方案，故本助手给出的价格**仅供参考**，具体猜价格操作还需自行判断。
- 视频教程恕暂不提供，敬请谅解。

## 偶发问题
- 如果报错，请多试着运行几次，可能因为并发查询过多导致查询解析失败。
- 遇到其他问题可以查看Issue中的内容，我会不定期来查看。

