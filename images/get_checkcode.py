import requests
times = 3
url = input("checkcode url:")
for i in range(0, times) :
    r = requests.get(url)
    with open(str(i)+".gif", "wb") as f :
        f.write(r.content)
print("success")