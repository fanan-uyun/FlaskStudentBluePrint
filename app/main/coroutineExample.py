"""
协程回顾
"""

# 生成器
def hello():
    for i in (1,3,5):
        key = yield i
        print(key)
        print("hello world")

# h = hello()
# print("+++++++++++++++++++++++++++++++++++++++++++++++")
# print(next(h))
# print("+++++++++++++++++++++++++++++++++++++++++++++++")
# print(next(h))
# print("+++++++++++++++++++++++++++++++++++++++++++++++")
# print(next(h))
# print("+++++++++++++++++++++++++++++++++++++++++++++++")

# print("+++++++++++++++++++++++++++++++++++++++++++++++")
# print(next(h))
# print("+++++++++++++++++++++++++++++++++++++++++++++++")
# print(h.send(10))
# print("+++++++++++++++++++++++++++++++++++++++++++++++")
# print(h.send(20))


# 实际工作中，协程至少需要两个函数
def getContent():
    """
    获取内容的方法
    """
    while True:
        url = yield  "I have content"
        print("get content from url : %s"%url)

def getUrl(g):
    url_list = ["url1","url2","url3","url4","url5"]
    for i in url_list:
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        g.send(i)
        print("+++++++++++++++++++++++++++++++++++++++++++++++")

if __name__ == "__main__":
    g = getContent()
    print(next(g))
    getUrl(g)
