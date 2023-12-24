import requests
local_host = 'http://127.0.0.1:5000/'
# urls = ["generate/fill_worksheet", "generate/worksheet", "generate/rearrange_worksheet", "generate/vocab_worksheet"]
urls = ["generate/worksheet", "generate/rearrange_worksheet", "generate/vocab_worksheet"]

""" 
with open('index.html', 'w') as file:
    file.write(requests.get(local_host).content.decode('utf-8'))

for url in urls:
    with open(url.replace('/', '-') + '.html', 'w') as file:
        file.write(requests.get(local_host + url).content.decode('utf-8'))
 """
for level in ['1', '2', '3', '4', '5', '6']:
    for url in urls:
        with open(url.replace('/', '-') + '-' + level + '.html', 'w') as file:
            file.write(requests.get(local_host + url + '/' + level).content.decode('utf-8'))