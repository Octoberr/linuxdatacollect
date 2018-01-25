# coding:utf-8
"""
公用方法：
不同时间格式转换
去重等方法
creat by swm
20180108
"""
import datetime
import os
# 当前文件夹的绝对路径
fileDir = os.path.dirname(os.path.realpath(__file__))
print(fileDir)


class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError("score must be an integer!")
        if value < 0 or value > 100:
            raise ValueError("score must between 0~100")
        self._score = value

def getallthefilename(directorypath):
    allfilenames = []
    for root, dirs, files in os.walk(directorypath):
        for filename in files:
            # print(filename)
            allfilenames.append(filename)
    # 修改文件名
    # os.rename(filename, newfilename)
    return allfilenames


# 测试定时任务
def aspdo():
    print("i have a schedule", datetime.datetime.now())


# unixtime to 北京时间
def unixtimeToBjTime(nowUnixtime):
    bjtime = datetime.datetime.fromtimestamp(nowUnixtime)
    # 时间相加(例子为加10分钟)
    getonthncartime = bjtime + datetime.timedelta(minutes=10)
    return bjtime


# 获取列表中一个元素重复的次数和位置
def getAllIndices(element, alist):
    """
    Find the index of an element in a list. The element can appear multiple times.
    input:  alist - a list
            element - objective element
    output: index of the element in the list
    """
    result = []
    offset = -1
    while True:
        try:
            offset = alist.index(element, offset + 1)
        except ValueError:
            return result
        result.append(offset)


if __name__ == '__main__':
    s = Student()
    s.score = 30
    print s.score
    s.score = 9000
    # print(getallthefilename(fileDir))