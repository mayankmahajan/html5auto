import httplib,urllib

params = urllib.urlencode({'username' : "manager", 'password':"m", 'submit' : "Login"})
headers = {
    "Content-type" : "application/x-www-form-urlencoded",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Host" : "192.168.113.44",
    "Referer" : "http://192.168.113.44/login"
}
conn = httplib.HTTPConnection("192.168.113.44",80)
conn.request("POST", "login", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()
