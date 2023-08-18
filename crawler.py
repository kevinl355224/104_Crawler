import datetime 
import pandas as pd
import xlsxwriter

from get_url import get_url
from crawl_detail import crawl_detail

class Crawler():
    def __init__(self) -> None:

        self.current_column = ["1", "2", "3", "6", "7", "8", "9", "10", "11", "12"]
        self.keyword = "None"
        self.data_num = "0"

        self.operation_list = [
            ["1", "新增項目", "self.add_column()"], 
            ["2", "刪除項目", "self.drop_column()"], 
            ["3", "輸入/更改 查詢關鍵字", "self.input_keyword()"], 
            ["4", "輸入/更改 搜尋數量", "self.input_data_num()"], 
            ["5", "輸出Excel", "self.export_excel()"], 
            ["6", "關閉程式", "self.break_out()"]
        ]

        self.data_list = [
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


    def print_operation_list(self):
        print("操作選單 :")
        for n in self.operation_list:
            print("  "+n[0]+"."+n[1])
    
    def operation(self, num):   
        for n in self.operation_list:
            if num == n[0]:
                eval(n[2])
                return
        print("[ 代碼錯誤,請重新輸入 ]")

    def print_current_status(self):
        print("----------- 目前欄位 ----------------------------------------------------------------------")
        print("  ", end="")
        for n in self.current_column:
            for m in self.data_list:                  
                if n == m[0]:
                    print(f"{m[0]}.{m[1]} | ", end="")
        print()
        print("  關鍵字: "+self.keyword)
        print("  搜尋數量: "+self.data_num)
        print("-------------------------------------------------------------------------------------------")
    
    def print_column(self):
        print("可添加項目 :")
        for n in self.data_list:
            if n[0] in self.current_column:
                continue
            # print("  "+n[0]+"."+n[1]+" : "+n[2])
            print(f"  {n[0]:2}.{n[1]:4} : {n[2]:10}")

    def add_column(self):
        self.print_current_status()
        self.print_column()
        print()
        print("請輸入項目代號 : ( 0 : 退出 )")
        a=1
        while a==1:
            input_ = input()
            if input_=="0":
                return
            elif input_ in self.current_column:
                print("代碼重複,請重新輸入 :")
            elif any( n[0]==input_ for n in self.data_list):
                self.current_column.append(input_)
                print("[ 添加成功 ]")
                a=0
            else:
                self.error()

        
    def drop_column(self):
        self.print_current_status()
        print("請輸入刪除項目代號 : ( 0 : 退出 )")
        a=1
        while a==1:
            input_ = input()
            if input_=="0":
                return
            elif input_ in self.current_column:
                self.current_column.remove(input_)
                print("[ 刪除成功 ]")
                a=0
            else:
                self.error()

    def input_keyword(self):
        print("請輸入關鍵字 : ", end="")
        self.keyword = input()
        print("[ 關鍵字設定成功 ]")

    def input_data_num(self):
        print("請輸入查詢數量 : ", end="")
        while True:
            input_ = input()
            if input_.isdigit():
                self.data_num = input_
                print("[ 數量設定成功 ]")
                return
            else:
                print("請輸入正確數字 : ", end="")

    def export_excel(self):
        if self.keyword == "None":
            print("[ 請輸入關鍵字 ]")
            self.input_keyword()
        if self.data_num == "0":
            print("[ 請輸入查詢數量 ]")
            self.input_data_num()

        url_list = get_url(keyword=self.keyword, number=self.data_num)
        column = []
        for n in self.current_column:
            for m in self.data_list:
                if n == m[0]:
                    column.append(m[1])  

        df = pd.DataFrame(columns=column)
        time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        excel_name = f"104_{self.keyword}_查詢結果_{time}.xlsx"

        writer = pd.ExcelWriter(excel_name, engine='xlsxwriter')

        for url in url_list:
            df.loc[len(df)] = crawl_detail(url=url, column_decide=self.current_column)

        df.to_excel(writer, sheet_name="Sheet1", index=False)
 
        #center對齊
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        start_row = 1
        end_row = start_row + len(df)
        start_col = 0
        end_col = start_col + len(df.columns) - 1

        centered_format = workbook.add_format({'align': 'center'})

        worksheet.set_column(start_col,  end_col,  cell_format=centered_format)
        for row in range(start_row,  end_row):
            worksheet.set_row(row,  cell_format=centered_format)

        #設定欄位寬度
        for column in df:
            column_width = max(df[column].map(len).max(), len(column))
            column_idx = df.columns.get_loc(column)
            if column_width < 22:
                column_width = 22
            worksheet.set_column(column_idx, column_idx, column_width)
        writer.close()



        print("[ 檔案輸出成功 ]")
        self.break_out()

    def break_out(self):
        print("感謝您的使用,期待下次再見 >皿< ")
        exit()

    def error(self):
        print("代碼錯誤,請重新輸入 : ( 0 : 退出 )")

    
