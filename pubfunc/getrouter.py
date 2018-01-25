"""
正则表达式匹配路由器用户名和密码
by swm 2018/01/05
"""
import re
import datetime


# 时间转换str datetime to datetime
def str2datetime(strdate):
    dt = datetime.datetime.strptime(strdate, "%Y-%m-%d %H:%M:%S")
    return dt


def getrouter(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    # 匹配dhcp的host
    re_host = re.compile(r'host:\s([\d.]+[\d.]+[\d.]+[\d])')
    # 匹配用户名
    re_usr = re.compile(r'login:\s(\w+)')
    # 匹配密码
    re_pwd = re.compile(r'password:\s(\S+)')
    # 匹配成功的时间
    re_time =re.compile(r'\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2}')
    host = re_host.findall(data)
    usr = re_usr.findall(data)
    pwd = re_pwd.findall(data)
    time = re_time.findall(data)
    # 转换为datetime格式
    starttime = str2datetime(time[0])
    endtime = str2datetime(time[1])
    print(data)
    print(host)
    print(usr)
    print(pwd)
    print(time)
    print(starttime, type(starttime))
    print(endtime, type(endtime))


if __name__ == '__main__':
    filepath = 'router.txt'
    getrouter(filepath)