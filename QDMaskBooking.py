import os
from selenium import webdriver
import datetime
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

def main():
    txtFile = open("./information.txt", "r",encoding='UTF-8')
    txtList = txtFile.readlines()
    infoList = []
    txtList = [x.strip('\n') for x in txtList if x.strip('\n')!='']

    if len(txtList)%6 == 0:
        for i in range(int(len(txtList)/6)):
            infoList.append(txtList[i*6:(i+1)*6])
    else:
        print('information.txt文件信息格式有误，请检查！')
        return 0

    #默认是邮政，每天9:30开始
    dateToday = datetime.date.today().strftime("%Y-%m-%d")
    url = "http://kzyynew.qingdao.gov.cn:81/dist/index.html#/preOrder"
    openTime =dateToday +" 09:30:00"

    #顺丰每天10：00开始
    if  (dateToday +" 09:30:00")<datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')<(dateToday +" 10:00:00"):
        url = "http://kzyynew.qingdao.gov.cn:81/dist/index.html#/SFOrder"
        openTime = dateToday +" 10:00:00"
    elif datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')>(dateToday +" 10:00:00"):
        openTime = (datetime.date.today()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")+" 09:30:00"
  
    for info in infoList:
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

        while True:
            try:
                if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') > openTime:
                    driver.get(url)
                    print('*'*30)
                    print('预约开始')
                    print('*'*30)
                    time.sleep(0.5)
                    if driver.find_element_by_class_name('vux-check-icon'):

                        driver.find_element_by_class_name('vux-check-icon').click()

                        inputText = driver.find_elements_by_class_name('weui-input')
                        inputText[0].send_keys(info[0])
                        inputText[1].send_keys(info[1])
                        inputText[2].send_keys(info[2])

                        selectRegion = driver.find_elements_by_class_name('weui-select')
                        region = selectRegion[0]
                        Select(region).select_by_visible_text(info[3])
                        street = selectRegion[1]
                        Select(street).select_by_visible_text(info[4])

                        driver.find_element_by_class_name('weui-textarea').send_keys(info[5])
                        break
                else:
                    localTime = datetime.datetime.strptime(openTime, "%Y-%m-%d %H:%M:%S")
                    print('预约未开始，离开始还有',(localTime-datetime.datetime.now()) )

            except Exception:
                time.sleep(0.5)

if __name__ == '__main__':
    main()
    print('按任意键结束...')
    os.system('pause>>nul')