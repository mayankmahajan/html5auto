import pycurl
curl = pycurl.Curl()

# Turn on cookies
curl.setopt(pycurl.COOKIEFILE, "cookie_test.txt")

# Login
curl.setopt(pycurl.URL, "http://192.168.113.44/login")
curl.setopt(pycurl.POST, 1)
curl.setopt(pycurl.HTTPPOST, [('username', 'manager'), ('password', 'm'),('submit','Login')])
curl.perform()