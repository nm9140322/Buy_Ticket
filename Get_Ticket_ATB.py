# python 搶票機器人 side project
# selenium：pip install selenium
# Ticket Plus 遠大售票系統-原子少年演唱會

from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# 登入帳密輸入
def login(driver):
    # 若已登入就略過
    try:
        # 帳號密碼的登入
        account = driver.find_element("xpath", '//*[@class="input-tel__input"]') # 輸入帳號資料的位置-程式碼的XPath (檢查-複製)
        account.clear()
        account.send_keys('售票網個人帳號') # 帳號資料
        # print('輸入帳號', datetime.now())

        password = driver.find_element("xpath", '//*[@autocomplete="new-password"]') # 輸入密碼資料的位置
        password.clear()
        password.send_keys('售票網個人密碼') # 密碼資料
        # print('輸入密碼', datetime.now())

        driver.find_element("xpath", '//*[@id="app"]/div[3]/div/div[1]/div/div[2]/div[1]/form/button/span').click() # 點選提交按鈕
        # print('登入成功', datetime.now())

    except:
        pass

# 活動開放購買
def Buy_allow(driver):
    # 尚未開放就重新迴圈，開放了就結束迴圈繼跑後面流程
    # 購買場次網址：OK
    while True:
        buy_url = '//*[@id="buyTicket"]/div[2]/div[1]/div[2]/div/button/span'
        buy_start = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, buy_url)))
        # print('活動狀況：', buy_start.text)
        
        if buy_start.text == '立即購票':          
            buy_start.click()
            # print('點選立即購買', datetime.now())
            # 登入
            login(driver)
            break
        else:
            print('現在尚未開放喔！', datetime.now())
            time.sleep(1) # 一秒後再試
            pass 

# 票種票數位置選取，後續流程如果重整都會從這裡開始
def Pick_Ticketclass(driver):
    # 網址前綴：
    process = '//*[@id="app"]/div[1]/div/div/main/div/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/'
    
    # 原子少年票種（票價）區：OK
    area_3280 = 'div[1]/div/div/div/div[1]/' 
    area_2880 = 'div[2]/div/div/div/div/'
    area_2280 = 'div[3]/div/div/div/div[1]/'
    area_1880 = 'div[4]/div/div/div/div[1]/'
    area_1480 = 'div[5]/div/div/div/div[1]/'
    area_1080 = 'div[6]/div/div/div/div/'
    ticket_types = [area_3280, area_2880, area_2280, area_1880, area_1480, area_1080]

    # 原子少年選擇票數區：OK
    pick_num = 'div/div/div[2]/div[3]/div/button[2]/span'

    # 剩餘標籤：OK
    soldout = 'button/div[1]/div[1]/small'
    
    # 先跑高價票，順利就結束迴圈往後面跑，沒了就改試低價票
    for ticketchoese in ticket_types:
        ticket_class_url = str(process + ticketchoese + 'button')
        ticket_pick = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ticket_class_url)))

        # 如果賣完了會有「剩餘」的small class
        try:
            ticket_soldout = str(process + ticketchoese + soldout)
            ticket_pick_soldout = driver.find_element(By.XPATH, ticket_soldout)
            ticket_pick_soldout_text = ticket_pick_soldout.text

            left_num = ['剩餘：0', '剩餘：1', '剩餘：2', '剩餘：3', '剩餘：4']
            # 字串剩餘數不足就跳下一個票種
            if ticket_pick_soldout_text in left_num:
                print('票沒了搶下一種～', datetime.now())
                continue
            # 剩餘量>4就照跑
            else:
                pass
        except:
            # 票數充足就不會有小標籤直接pass
            pass

        # 點擊票種
        driver.execute_script("arguments[0].click();", ticket_pick)
        # print('點選票種：', ticketchoese, datetime.now())

        ticket_class_num_url = str(process + ticketchoese + pick_num)
        ticket_num = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ticket_class_num_url)))
        
        try:
            # 點選張數(5張)
            driver.execute_script("arguments[0].click();", ticket_num)
            driver.execute_script("arguments[0].click();", ticket_num)
            driver.execute_script("arguments[0].click();", ticket_num)
            driver.execute_script("arguments[0].click();", ticket_num)
            driver.execute_script("arguments[0].click();", ticket_num)
            # print('點選票數', datetime.now())
            break
        
        except:
            print('選票數出錯囉！')
            continue

def seat_next(driver):
    # 連位：OK
    seat_url = '//*[@id="app"]/div[1]/div/div/main/div/div/div[4]/div/div/div[1]/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div'
    seat = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, seat_url)))
    driver.execute_script("arguments[0].click();", seat)
    # print('連位', datetime.now())

    # 下一步：OK
    nextstep1_url = '//*[@id="app"]/div[1]/div/div/main/div/div/div[4]/div/div/div[3]/div/div[2]/button/span'
    nextstep1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, nextstep1_url))).click()
    # print('下一步1', datetime.now())

# 剩餘購買流程，如果重新整理都會回到上一頁 
def Buy_Process(driver):

    # 跳轉確認位置下一步：OK
    nextstep2_url = '//*[@id="app"]/div[1]/div/div/main/div/div/div[5]/div/div/div[4]/div/div[2]/button/span'
    nextstep2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, nextstep2_url)))
    driver.execute_script("arguments[0].click();", nextstep2)
    # print('確認位置下一步2', datetime.now())

    # 跳轉勾選同意：OK
    agree_url = '//*[@id="app"]/div[1]/div/div/main/div/div/div/div[5]/div/div/div[2]/div/div/div/div/div'
    agree = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, agree_url)))
    driver.execute_script("arguments[0].click();", agree)
    # print('點選同意', datetime.now())

    # 同意後下一步：OK
    nextstep3_url = '//*[@id="app"]/div[1]/div/div/main/div/div/div/div[5]/div/div/div[3]/button/span'
    nextstep3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, nextstep3_url)))
    driver.execute_script("arguments[0].click();", nextstep3)
    # print('同意下一步3', datetime.now())

    # 跳轉
    # 點選取票方式-ibon：OK
    get_ticket_url = '//*[@id="getWay"]/div[2]/div/div/div[1]/div/div[1]/div/div'
    get_ticket = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, get_ticket_url)))
    driver.execute_script("arguments[0].click();", get_ticket)
    # print('取票方式-ibon', datetime.now())

    # 點選付款方式-ATM虛擬帳號：OK
    ATM_pay_url = '//*[@id="payWay"]/div[2]/div/div/div[1]/div/div[2]/div/div'
    ATM_pay = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ATM_pay_url)))
    driver.execute_script("arguments[0].click();", ATM_pay)
    # print('付款方式-ATM', datetime.now())

    # 點選前往付款-跳轉完成訂單：OK
    nextstep4_url = '//*[@id="app"]/div[1]/div/div/main/div/div/div[2]/div[5]/div/div/div[3]/button/span'
    nextstep4 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, nextstep4_url)))
    driver.execute_script("arguments[0].click();", nextstep4)
    print('完成付款', datetime.now())

    # 跳轉訂單資訊-查看訂單明細
    try:
        order_url = '//*[@id="app"]/div[1]/div/div/main/div/div/div/div[8]/button/span'
        order = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, order_url)))
        driver.execute_script("arguments[0].click();", order)
        print('完成訂單', datetime.now())
    except:
        print('訂單明細出了點小問題PASS', datetime.now())
        pass

    # 視窗截圖
    try:
        driver.get_screenshot_as_file('./ordersucceed.png')
        print('截圖訂單頁', datetime.now())
    except:
        print('截圖訂單出了點小問題PASS', datetime.now())
        pass

# 出問題就重新整理
def Page_Refresh(driver):
    driver.refresh()
    
    # 接受警告框
    try:
        driver.switch_to.alert.accept()
        print('確認警告框')

    except:
        print('沒有警告框')
        pass

    print('重新整理', datetime.now())



# 完整搶票全流程
def Buy_Ticket():
    # 提前開啟無痕瀏覽器
    print('開始搶票任務：', datetime.now())
    
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15" # 假的 headers 資訊
    options = Options()
    options.add_argument("--incognito")  # 使用無痕模式
    options.add_argument('--user-agent=%s' % user_agent) # 送出模擬瀏覽器的 headers 資訊  (反爬蟲)
    service = Service("./chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options) # 開啟模擬瀏覽器
    # 清空 window.navigator的 webdriver 屬性 (反爬蟲)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                            "source": """
                                Object.defineProperty(navigator, 'webdriver', {
                                get: () => undefined
                                })
                            """
                            })
    # print('開啟瀏覽器', datetime.now())

    # 開啟網頁：
    activity_url = 'https://ticketplus.com.tw/activity/a38b1a8b18a311b9a91a852025d0f8fa?openExternalBrowser=1'
    driver.get(activity_url) 
    # print('開啟網頁', datetime.now())

    # 先點選會員登入
    login_url = '//*[@id="appBar"]/div/div/div/button/span'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, login_url))).click() 
    # print('會員登入', datetime.now())
    login(driver)

    print('開始實際搶票流程：', datetime.now())

    # 執行搶票流程，直到成功搶到或是排程強制結束任務為止
    while True:
        try:
            try:
                Buy_allow(driver)
            except:
                print('已開放購買')
                pass

            # 重新整理的話會從這裡開始，如果是前一個步驟程式有錯才導致直接跑到這，那就直接結束迴圈
            try:
                Pick_Ticketclass(driver)
            except:
                print('選票流程有不明錯誤GG')
                driver.quit()
                break
            
            # 如果都沒票了，就沒辦法選位置直接結束搶票迴圈
            try:
                seat_next(driver)
            except:
                print('全部都被搶光啦哭喔！')
                driver.quit()
                break
            
            try:
                Buy_Process(driver)
            except:
                print('選位後的流程有不明錯誤GG')
                driver.quit()
                break    

            # 流程跑完關閉瀏覽器並結束搶票迴圈
            time.sleep(5) # 關閉前至少等5秒，避免訂單生成時間太長而失敗
            driver.quit()

            print('完成搶票去收信付款：', datetime.now())
            break
        
        except:
            # 流程跑到後面才沒票，就重整頁面
            Page_Refresh(driver)


# 搶票排程：
from apscheduler.schedulers.background import BlockingScheduler
import tzlocal # 時區差異會再時間排程上產生一些問題，所以import當地時間可以避免一些麻煩
sched = BlockingScheduler(timezone=str(tzlocal.get_localzone()))

sched.add_job(Buy_Ticket, 'date', run_date=datetime(2022, 7, 24, 13, 58, 0)) # 年 月 日 時 分 秒，13:58開始
sched.start()