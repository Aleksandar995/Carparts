import requests

def makerequests(sku):
    base_url = "https://api.usautoparts.io/v1/pages?domain=carparts.com&uri=/bumper-cover/replacement/9363-1&absearch=u&blog=0&bot=0&getTools=0"
    before = base_url[0:base_url.rindex('replacement/') + 12]
    after = base_url[base_url.rindex('&absearch'):]
    f1.write(before + sku + after + '\n')


apis = {'apikey': 'atpvGyxKcznNy'}
r = requests.get('https://api.usautoparts.io/v1/pages?domain=carparts.com&&itemperpage=9470&uri=/bumper-cover&absearch=u&blog=0&bot=0&getTools=0',
                 headers=apis)


f = open("skus.txt", "a")
f1 = open("requests.txt", "a")
r_json = r.json()

items = r_json['data']['products']['items']
i = 0
for item in items:
#     f.write(item['sku'] + '\n')
    makerequests(item['sku'])
    i = i + 1


print(i)
