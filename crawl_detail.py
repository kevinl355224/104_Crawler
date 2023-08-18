import requests

def crawl_detail(url, column_decide) ->list : 
    referer = url
    
    url2 = "https://www.104.com.tw/job/ajax/content/" +url.split("/")[-1]


    headers = {
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 
        "Referer":referer
        }
    req = requests.get(url=url2, headers=headers)

    data = req.json()

    data_list = [
        ["1", "更新日期", "2023/06/23", 'data["data"]["header"]["appearDate"]'], 
        ["2", "職務名稱", "會計", 'data["data"]["header"]["jobName"]'], 
        ["3", "薪資範圍", "30000~40000", 'data["data"]["jobDetail"]["salary"]'], 
        ["4", "最低薪資", "30000", 'crawl_salary_min(data)'], 
        ["5", "最高薪資", "40000", 'crawl_salary_max(data)'], 
        ["6", "工作區域", "大安區", 'data["data"]["jobDetail"]["addressRegion"]'], 
        ["7", "詳細地址", "基隆路xx巷xx弄", 'data["data"]["jobDetail"]["addressDetail"]'], 
        ["8", "公司名稱", "範例有限公司", 'data["data"]["header"]["custName"]'], 
        ["9", "工作性質", "全職", 'crawl_work_type(data)'], 
        ["10", "上班時段", "日班09:00~17:00", 'data["data"]["jobDetail"]["workPeriod"]'], 
        ["11", "休假制度", "周休二日", 'data["data"]["jobDetail"]["vacationPolicy"]'], 
        ["12", "網址", "https://xx", 'referer']
    ]

    ##### 有機會再增加#####
    # 不拘就不顯示
    # condition_list = ["工作經驗", "學歷要求", "科系要求", "擅長工具", "工作技能", "具備證照"]
    # data_dict["條件要求"] = data["data"]["condition"]


    # 要可以遇到爬不了的資料回傳error不會crash
    crawl_data_list = []
    for n in column_decide:
        for m in data_list:
            if n == m[0]:
                try:
                    crawl_data_list.append(eval(m[3]))
                except:
                    crawl_data_list.append("Error")

    return crawl_data_list


def crawl_work_type(data):
    work_type = data["data"]["jobDetail"]["workType"]
    if work_type == []:
        return "全職"
    else :
        return ",".join(work_type)


def crawl_salary_min(data):
    salary_min = data["data"]["jobDetail"]["salaryMin"]
    if data["data"]["jobDetail"]["salary"] == "待遇面議":
        return data["data"]["jobDetail"]["salary"]
    elif salary_min == 9999999 or salary_min == 0 :
        return ""
    else:
        return salary_min

def crawl_salary_max(data):
    salary_max = data["data"]["jobDetail"]["salaryMax"]
    if data["data"]["jobDetail"]["salary"] == "待遇面議":
        return data["data"]["jobDetail"]["salary"]
    elif salary_max == 9999999 or salary_max == 0 :
        return ""
    else:
        return salary_max
    
