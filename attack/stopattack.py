# coding:utf-8

"""
结束死循环式的攻击
反正就是结束攻击
"""
import redis


class SHUTDOWN:

    def attackover(self):
        r = redis.Redis(host="localhost", port=6379)
        r.hset('attack', 'statu', 0)
        return


if __name__ == '__main__':
    shuwdown = SHUTDOWN()
    shuwdown.attackover()
