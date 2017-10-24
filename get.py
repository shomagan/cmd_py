import urllib.request
counter = 0
while(1):
  http_get = urllib.request.urlopen("http://172.16.1.3").read()
  counter+=1
  print(counter)