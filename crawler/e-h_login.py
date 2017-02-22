import requests

# 登录ehentai，获取cookie，但似乎这个方式获取的cookie缺少访问EXhendtai的某些字段，用requests也没法追踪cookie的变化，最后直接获取登录后的cookie了事

# 请自备E绅士帐号
username = ''
password = ''
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
