# -*- coding: utf-8 -*-
import io
import sys
import mysql.connector
import requests
import urllib2 as urllib
import MySQLdb
from bs4 import BeautifulSoup
html = """
<div class="article_content clearfix csdn-tracking-statistics" data-dsm="post" data-mod="popu_307" data-pid="blog" id="article_content">
                    <link href="https://csdnimg.cn/release/phoenix/template/css/ck_htmledit_views-e2445db1a8.css" rel="stylesheet"/>
						<div class="htmledit_views">
                <p><strong><span style="color:#f33b45;">一、从</span><a href="https://link.jianshu.com/?t=https%3A%2F%2Fcode.visualstudio.com%2F" rel="nofollow"><span style="color:#f33b45;">VSCode官网</span></a><span style="color:#f33b45;">下载deb软件包</span></strong></p>

<p>下载地址：<a href="https://code.visualstudio.com/" rel="nofollow">https://code.visualstudio.com/</a></p>

<p><strong><span style="color:#f33b45;">二、在Ubuntu中安装VSCode</span></strong></p>

<pre class="has"><code>sudo dpkg -i xxx.deb</code></pre>

<p><span style="color:#f33b45;"><strong>三、安装VSCode所需依赖</strong></span></p>

<pre class="has"><code>sudo apt-get install -f</code></pre>

<p><span style="color:#f33b45;"><strong>四、启动VSCODE  安装相关插件</strong></span></p>

<p>启动的时候要注意  如果是root用户  启动时采用</p>

<pre class="has"><code>code --user-data-dir
</code></pre>

<p>如果是一般用户  直接输入code即可</p>

<p><strong>4.1 安装vscode-icons（图标美化）</strong></p>

<p>点击左侧最后一个按钮(Extensions)，在其右侧框中输入vscode-icons，点击install进行安装，安装完成之后会提示你重载(点击reload)，在右下角中点击active进行激活</p>

<p style="text-align:center;"><img alt="" class="has" src="https://img-blog.csdn.net/20180815162519356?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3l1bmdlODEy/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70"/></p>

<p>4.2 同理安装python插件</p>

<p>4.3 安装flake8(错误检查)和yapf(美化代码)插件</p>

<pre class="has"><code>sudo apt-get install python-pip
pip install flake8
pip install yapf </code></pre>

<p><span style="color:#f33b45;"><strong>五、配置设置</strong></span></p>

<p><strong>5.1 配置vscode的设置</strong></p>

<p>点击右下角工具图票--设置</p>

<p style="text-align:center;"><img alt="" class="has" src="https://img-blog.csdn.net/20180815163643538?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3l1bmdlODEy/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70"/></p>

<p>在弹出来的settings中右边写入以下内容   确保vscode能使用这些插件 </p>

<pre class="has"><code>{
    "workbench.iconTheme": "vscode-icons",
    "python.pythonPath": "/usr/bin/python3.5",
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "yapf",
    "files.insertFinalNewline": true
}</code></pre>

<p style="text-align:center;"><img alt="" class="has" src="https://img-blog.csdn.net/20180815163708906?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3l1bmdlODEy/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70"/></p>

<p><strong>5.2 配置工程</strong></p>

<p>ctrl+shift+B 在上方提示没有成功</p>

<p>点击others  生成tasks.json模版   这里我们需要按照我们自己的工程来进行设置</p>

<pre class="has"><code>{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "python_test1",
            "type": "shell",
            "command": "python",
            "args": ["${file}"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
        }
    ]
}</code></pre>

<p>下面介绍几个需要修改的地方</p>

<p> "label": "python_test1",       即文件名 工程名</p>

<p>"command": "python",</p>

<p>"args": ["${file}"],</p>

<p>配置相关的可以参考以下<a href="https://blog.csdn.net/u013205877/article/details/78883405" rel="nofollow">https://blog.csdn.net/u013205877/article/details/78883405</a></p>

<p><strong>5.3 再次运行ctrl+shift+B</strong></p>

<p>在下面的<strong>终端</strong>中 打印出相应的内容</p>            </div>
                </div>
"""
url = "https://blog.csdn.net/yunge812/article/details/81706301"
img_url = "https://img-blog.csdn.net/20180815162519356?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3l1bmdlODEy/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70"
html_doc = requests.get(url=img_url, headers=headers).content.decode()
url_content = requests.get(img_url+url)
print(url_content)
soup = BeautifulSoup(html,"html.parser")
imgs = soup.find_all("img")
x = 0
# for img_src in imgs:
#     print(img_src['src'])
#     url_content = requests.get(img_src['src']+url)
#     print(url_content)
#     break
    # urllib.urlretrieve(img_src['src'],"./img/%d.jpg" % (x))
    # img_temp = urllib.urlopen(img_src['src'])

    # temp_file = open("./img/%d.jpg" % (x), 'wb')
    # temp_file.write(img_temp)
    # temp_file.close()
    # x += 1
# print(soup.prettify())