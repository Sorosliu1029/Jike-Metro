
# coding: utf-8

# In[8]:


import qrcode
import requests
import time


# In[2]:


jike_url_fmt = 'jike://page.jk/web?url=https%3A%2F%2Fruguoapp.com%2Faccount%2Fscan%3Fuuid%3D{uuid}&displayHeader=false&displayFooter=false'


# In[49]:


qr = qrcode.QRCode(
    version=8,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=2,
)


# In[50]:


resp = requests.get('https://app.jike.ruguoapp.com/sessions.create')
qr.add_data(jike_url_fmt.format(**resp.json()))
qr.make()

img = qr.make_image(fill_color="white", back_color="black")


# In[51]:


img


# In[52]:


uuid = resp.json()
res = requests.get('https://app.jike.ruguoapp.com/sessions.wait_for_login', params=uuid)
result = res.json()
if result.get('logged_in') == True:
    print(res.cookies)
    res = requests.get('https://app.jike.ruguoapp.com/sessions.wait_for_confirmation', params=uuid)
    token = res.json()
    if token.get('confirmed') == True:
        print(token)
        print(res.cookies)


# In[56]:


t = token['token']
payload = {
    'limit': 20,
    'loadMoreKey': 'null'
}
headers = {
    'Origin': 'http://web.okjike.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Referer': 'http://web.okjike.com/collection',
    'x-jike-app-auth-jwt': t,
    'Content-Length': '31',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'App-Version': '4.1.0',
    'DNT': '1',
    'platform': 'web',
}
cookies = {
    'auth-token': t
}
resp = requests.post('https://app.jike.ruguoapp.com/1.0/users/collections/list',
                    json=payload,
                    headers=headers,
                    cookies=cookies)
print(resp.text)

