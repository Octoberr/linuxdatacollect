# coding:utf-8
# 函数注册
registry = []


def register(decorated):
  registry.append(decorated)
  return decorated

