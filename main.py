# 介紹 :
# main是使用者操作介面
# 呼叫crawler，crawler可以
#       搜尋想要的職業
#       新增或刪減爬蟲的資料
#       設定爬蟲的資料數量
# 再由get_url爬取個職業的URL
# crawl_detail會去抓取crawler指定的資料
import crawler
crawler = crawler.Crawler()

print("歡迎使用簡易104爬蟲程式!!")
print()

while True:
    crawler.print_current_status()
    print()
    crawler.print_operation_list()
    print()
    print("請輸入代碼 : ", end="")
    crawler.operation(input())

