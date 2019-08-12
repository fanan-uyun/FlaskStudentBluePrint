"""
gevent官方案例
"""
import gevent

def fun1():
    for i in range(5):
        print("I am fun 1 this is %s"%i)
        gevent.sleep(0)

def fun2():
    for i in range(5):
        print("I am fun 2 this is %s"%i)
        gevent.sleep(0)


# fun1()
# fun2()

# 交替执行
# t1 = gevent.spawn(fun1)
# t2 = gevent.spawn(fun2)
# gevent.joinall([t1,t2])

# 协程锁方式
from gevent.lock import Semaphore

# 实例化信号量
sem = Semaphore(1)

def fun3():
    for i in range(5):
        sem.acquire()
        print("I am fun 3 this is %s"%i)
        sem.release()

def fun4():
    for i in range(5):
        sem.acquire()
        print("I am fun 4 this is %s"%i)
        sem.release()


t3 = gevent.spawn(fun3)
t4 = gevent.spawn(fun4)
gevent.joinall([t3,t4])

