import time
import httpx

user_login_url = "https://webapi.account.mihoyo.com/Api/login_by_mobilecaptcha"
bbs_login_url = "https://api-takumi.mihoyo.com/account/auth/api/webLoginByMobile"

header = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "DNT": "1",
    "Origin": "https://user.mihoyo.com",
    "Referer": "https://user.mihoyo.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/103.0.5060.134 Safari/537.36",
    "x-rpc-client_type": "4"
}


def cookie_to_str(_cookie) -> str:
    cookies = ""
    for i in _cookie:
        cookies = f'{cookies}; {i}={_cookie.get(i)}'
    return cookies[2:]


def bbs_login():
    _header = header
    _header["Origin"] = "https://bbs.mihoyo.com"
    _header["Referer"] = "https://bbs.mihoyo.com/"
    print("请打开: https://bbs.mihoyo.com/ys/ 申请手机号登入验证码")
    req = httpx.post(url=bbs_login_url,
                     json={"is_bh2": False,
                           "mobile": str(mobile),
                           "captcha": str(int(input("请输入验证码: "))),
                           "action_type": "login",
                           "token_type": 6},
                     headers=_header)
    result = req.json()
    if result['retcode'] != 0:
        print(f'登入失败，返回状态码:{result["retcode"]}，错误信息:{result["message"]}')
        return ""
    return cookie_to_str(req.cookies)


def user_login():
    print("请打开: https://user.mihoyo.com/ 申请手机号登入验证码")
    req = httpx.post(url=user_login_url,
                     data={"mobile": mobile,
                           "mobile_captcha": int(input("请输入验证码: ")),
                           "source": "user.mihoyo.com",
                           "t": int(time.time() * 1000)},
                     headers=header)
    result = req.json()
    if result['code'] != 200:
        print(f'登入失败，返回状态码:{result["code"]}，错误信息:{result["data"]["msg"]}')
        return ""
    return cookie_to_str(req.cookies)


if __name__ == '__main__':
    print("米游社Cookie获取器:\n\t1.游戏签到Cookie\n\t2.米游币获取Cookie\n\t3.全部获取")
    print('tips: 一般单独获取米游币Cookie用不到')
    login_type = int(input("请输入获取的类型: "))
    mobile = int(input("请输入手机号: "))
    cookie = ""
    if login_type == 1:
        cookie = bbs_login()
    elif login_type == 2:
        cookie = user_login()
    elif login_type == 3:
        bbs = bbs_login()
        user = user_login()
        cookie = f'{bbs}; {user}'
    else:
        print("输入错误!")
        exit(0)
    print("Cookie为：")
    print(cookie)
