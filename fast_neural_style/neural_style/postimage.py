import requests
import time
import random

def postImage(path, houzhui):
    url = "https://www.autotracer.org/zh.html"
    proxy_list= ['175.44.108.8:9999','180.168.13.26:8000','36.248.129.61:9999','183.129.207.86:11206',
                 '218.73.135.108:9999','182.35.84.130:9999','1.197.10.198:9999','119.33.64.147:80','222.189.191.213:9999',
                 '182.35.87.155:9999','123.163.96.144:9999','222.189.190.185:9999','1.197.203.105:9999']

    lclpath = path + houzhui
    
    files={'userfile':('temp.jpg',open(lclpath,'rb'),'image/jpeg'),
           'outFormat':(None,'svg'),
           'colorCount':(None,'2')
    }
    
    response = requests.post(url, files=files, proxies={'http': random.choice(proxy_list)})

    start_index = response.text.find('var url =')
    end_index = response.text.rfind('makeRequest')
    urll = response.text[start_index + 11:end_index]
    urll = urll.split("'")[0]
    urll = "https://www.autotracer.org/" + urll
    print('Step1 Complete!')

    time.sleep(2)
    response2 = requests.get(urll)

    start_index2 = response2.text.find("<a href=")
    end_index2 = response2.text.find('.svg">')
    urlll = response2.text[start_index2+9:end_index2+4]
    urlll = "https://www.autotracer.org/" + urlll
    print('Step2 Complete!')

    time.sleep(2)
    response3 = requests.get(urlll)
    img = response3.content

    with open( path + 'tempout.svg','wb' ) as f:
        f.write(img)

    print("All Complete!")
