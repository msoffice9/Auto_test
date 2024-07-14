from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymsteams
from datetime import datetime
 
ID = "넥슨 계정 아이디"
PW = "넥슨 계정 비밀번호"
myTeamsMessage = pymsteams.connectorcard("팀즈 커넥터 url")
 
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])
 
 
browser = webdriver.Chrome(options=option)
browser.implicitly_wait(5)
browser.maximize_window()
browser.get("https://test-creators.nexon.com/kr/campaign")
 
 
#로그인
browser.find_element(By.XPATH, '//*[@id="root"]/header/div/div/button').click()
browser.find_element(By.ID, 'txtNexonID').send_keys(ID)
browser.find_element(By.ID, 'txtPWD').send_keys(PW)
browser.find_element(By.XPATH, '//*[@id="nexonLogin"]/fieldset/div[4]/button').click()
time.sleep(2)
 
# 보너스 카드 찾기
def find():
    try:
        browser.find_element(By.XPATH, value="//div[@role='button']")
        return True
    except:
        pass
 
print("시작합니다.")
     
def main():
    try:
        x = 0
        while x < 10:
            if find():
                browser.find_element(By.XPATH, value="//div[@role='button']").click()
                x += 1
                time.sleep(2)
                browser.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div[6]/button").click()
                print("카드 보상 + %s개 수령" % (x))
                browser.refresh()
            else:
                print("보너스 카드가 없습니다.")
                browser.refresh()
                time.sleep(0.5)
                 
        today = datetime.now().strftime("%Y-%m-%d")     
        myTeamsMessage.text(today+ "\n" + ID + " 계정 보너스 카드 보상 완료를 확인하세요.")
        myTeamsMessage.send()
 
 
    except:
        myTeamsMessage.text("프로그램이 멈췄습니다.")
        myTeamsMessage.send()
         
 
 
if __name__ == "__main__":
    main()