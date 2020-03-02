import os
from selenium import webdriver
import datetime
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

class peopleInfo(object):
    def __init__(self,infoList):
        self.name = infoList[0]
        self.phone = infoList[1] 
        self.id = infoList[2]
        self.region = infoList[3]
        self.street = infoList[4]
        self.area = infoList[5]

        if infoList[6] =='邮政':
            self.url = "http://kzyynew.qingdao.gov.cn:81/dist/index.html#/preOrder"
        else:
            self.url = "http://kzyynew.qingdao.gov.cn:81/dist/index.html#/SFOrder"

def main():
    txtFile = open("./information.txt", "r",encoding='UTF-8')
    txtList = txtFile.readlines()
    txtList = [x.strip('\n') for x in txtList if x.strip('\n')!='']

    infoList = []
    if len(txtList)%7 == 0:
        for i in range(int(len(txtList)/7)):
            infoList.append(peopleInfo(txtList[i*7:(i+1)*7]))
    else:
        print('information.txt文件信息格式有误，请检查！')
        return 0

    #每天10:00开始
    dateToday = datetime.date.today().strftime("%Y-%m-%d")
    openTime =dateToday +" 10:00:00"

    #10点以后预约时间变到第二天
    if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')>(dateToday +" 10:00:00"):
        openTime = (datetime.date.today()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")+" 10:00:00"
    
    # 创建浏览器对象
    chromeOptions = Options()
    # 关闭Chrome上部提示语 "Chrome正在受到自动软件的控制"
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation'])
    # 允许浏览器重定向，Framebusting requires same-origin or a user gesture
    chromeOptions.add_argument("disable-web-security")
    driver = webdriver.Chrome(os.path.join("./chromeDriver", "chromedriver.exe"),
                            chrome_options=chromeOptions)
    # 窗口最大化显示
    driver.maximize_window()

    while datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') < openTime:
        localTime = datetime.datetime.strptime(openTime, "%Y-%m-%d %H:%M:%S")
        print('预约未开始，离开始还有',(localTime-datetime.datetime.now()) )

    print('*'*20,'预约开始','*'*20)
    for i, info in enumerate(infoList):
        print('*'*20,'第%d次预约'%(i+1),'*'*20)
        failFindNum = 0
        if i == 0:
            driver.get(info.url)
            time.sleep(0.5)
        else:
            js = 'window.open("'+info.url+'");'
            driver.execute_script(js)
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            time.sleep(0.5)
        while True:
            try: 
                driver.find_element_by_class_name('vux-check-icon').click()

                inputText = driver.find_elements_by_class_name('weui-input')
                inputText[0].send_keys(info.name)
                inputText[1].send_keys(info.phone)
                inputText[2].send_keys(info.id)

                selectRegion = driver.find_elements_by_class_name('weui-select')
                region = selectRegion[0]
                Select(region).select_by_visible_text(info.region)
                street = selectRegion[1]
                Select(street).select_by_visible_text(info.street)
                driver.find_element_by_class_name('weui-textarea').send_keys(info.area)
                break

            except Exception:
                if failFindNum<5:
                    print('第%d次失败，正在进行第%d次查询'%(failFindNum,failFindNum+1))
                    failFindNum += 1
                    time.sleep(0.5)
                else :
                    print(info.url,'服务器超时，或其他原因！')
                    break
                
if __name__ == '__main__':
    main()
    print('按任意键结束...')
    os.system('pause>>nul')