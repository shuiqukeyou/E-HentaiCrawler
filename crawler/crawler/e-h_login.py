import requests
#登录ehrantai，获取cookie，但似乎这个方式获取的cookie缺少字段


username = '帐号'
password = '密码'
loginurl = 'https://forums.e-hentai.org/index.php?act=Login&CODE=01'
logindata = {'returntype': 8, 'CookieDate': 1, 'b': 'd', 'bt': 'pone', 'UserName': username, 'PassWord': password,
             'ipb_login_submit': 'Login!'}

def get_cookie(username,password):
    loginurl = 'https://forums.e-hentai.org/index.php?act=Login&CODE=01'
    logindata = {'returntype': 8, 'CookieDate': 1, 'b': 'd', 'bt': 'pone', 'UserName': username, 'PassWord': password,
                 'ipb_login_submit': 'Login!'}
    seObj = requests.session()
    s = seObj.post(loginurl, data=logindata)
    return(s.cookies)
