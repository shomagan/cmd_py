import requests
import shutil
url = 'http://172.16.2.33/jpg/image.jpg'
user, password = '1', '1'
resp = requests.get(url, auth=(user, password))
counter=383
while(1):
    resp = requests.get(url, auth=(user, password), stream=True)
    if resp.status_code == 200:
        with open('jpg/ft'+str(counter)+'.jpg', 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)   

    counter+=1
    print(counter)

