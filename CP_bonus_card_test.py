from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymsteams
from datetime import datetime
 
ID = "Nexon ID"
PW = "Nexon PW"
myTeamsMessage = pymsteams.connectorcard("teams connector url")
 
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])
 
 
browser = webdriver.Chrome(options=option)
browser.implicitly_wait(5)
browser.maximize_window()
browser.get("https://test-creators.nexon.com/kr/campaign")
 
 
# login
browser.find_element(By.XPATH, '//*[@id="root"]/header/div/div/button').click()
browser.find_element(By.ID, 'txtNexonID').send_keys(ID)
browser.find_element(By.ID, 'txtPWD').send_keys(PW)
browser.find_element(By.XPATH, '//*[@id="nexonLogin"]/fieldset/div[4]/button').click()
time.sleep(2)
 
# find bonus cards
def find():
    try:
        browser.find_element(By.XPATH, value="//div[@role='button']")
        return True
    except:
        pass
 
print("Let's start.")
     
def main():
    try:
        x = 0
        while x < 10:
            if find():
                browser.find_element(By.XPATH, value="//div[@role='button']").click()
                x += 1
                time.sleep(2)
                browser.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div[6]/button").click()
                print("I find + %s cards" % (x))
                browser.refresh()
            else:
                print("There are no cards.")
                browser.refresh()
                time.sleep(0.5)
                 
        today = datetime.now().strftime("%Y-%m-%d")     
        myTeamsMessage.text(today+ "\n" + ID + " has recieved all bonus reward from cards. Check it please.")
        myTeamsMessage.send()
 
 
    except:
        myTeamsMessage.text("The program has stopped.")
        myTeamsMessage.send()
         
 
 
if __name__ == "__main__":
    main()
