import requests

def get_url(keyword,number):
    number = int(number)
    page = 0
    url_list = []
    while True:
        try :
            url_search_page = "https://www.104.com.tw/jobs/search/list?ro=0&kwop=7&keyword="+keyword+"&page="+str(page)
            headers = {
                "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
                "Referer":"https://www.104.com.tw/jobs/search/?keyword=%E6%9C%83%E8%A8%88&order=1&jobsource=2018indexpoc&ro=0"          
                }

            req = requests.get(url=url_search_page,headers=headers)
            data = req.json()
            for n in data["data"]["list"]:
                # 不加入廣告內容
                if "hotjob" in n["link"]["job"]:
                    pass
                else:
                    url_list.append("https:" + n["link"]["job"])
            page+=1

            if len(url_list)>= number:
                return url_list[0:number]

        except:
            print("Sometings wrong")
            break