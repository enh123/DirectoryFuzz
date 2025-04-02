本项目的精华为top5000目录字典和超大js文件字典

当测试空白页面时扫出来'/script/'目录时可以使用超大js目录文件进行扫描

top5000目录字典是我用github上的各种目录字典(几乎包含了所有的优质字典)用服务器扫了上万个网站，总共耗时2个月左右，经过筛选之后最终提取出来出现频率最高的5000个目录和文件。

最后推荐一款目录扫描工具https://github.com/epi052/feroxbuster

我试过非常多的目录扫描工具包括御剑的全部版本，ffuf，dirsearch，dirmap，7kbscan等等很多工具都试过，几乎都有各种各样的问题，要么就是扫描速度太慢，要么就是不支持批量扫描,要么就是批量导入的时候会出问题，要么就是多线程的时候程序会卡住，但最终找到一款工具很好用的工具'feroxbuster'，该工具有windows版本，下载对应版本https://github.com/epi052/feroxbuster/releases/tag/v2.10.4   

使用如下命令即可实现批量扫描

type url.txt | feroxbuster.exe --stdin --auto-tune -k -A  --dont-extract-links --no-state --no-recursion -o result.txt -t 20 -C 404 -w top5000.txt


2025/4/2 上传0.2版本

1.  对所有字典进行精简化，用一些规则去除了不常见的路径
2.  新增top15w.txt 和 top3w.txt 这两个是综合github上的字典进行合并提取出来的出现频率最高的路径(不是像top5000.txt一样扫出来的)。 新增swagger_api.txt ,这个是用swagger-hack2.0.py扫了大概700个swagger.json页面得到的所有路径没有添加别的。






