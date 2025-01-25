import time
from tkinter import ACTIVE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import pymsteams
from ensurepip import version
from win32api import *
import os
import shutil
import pygetwindow
import pyautogui
import configparser
 
 
# setting before testing
config = configparser.ConfigParser()
config.read('ngm 인증서 갱신.ini', encoding='utf-8-sig')
Type = config['SETTING']['type']
Build = config['SETTING']['build']
Download = config['SETTING']['download']
bot_url = config['SETTING']['bot_url']
myTeamsMessage = pymsteams.connectorcard(bot_url, verify=False)
driver_path = Type + '.exe'
 
# collection of variables
ngm_install = "C:/Users/" + Download + "/Downloads/Install_NGM.exe"
ngm_folder = "C:/ProgramData/Nexon/NGM"
ngm_path = "C:/ProgramData/Nexon/NGM/NGM.exe"
repair_path = "C:/Users/" + Download + "/Downloads/NexonRepair.exe"
 
# check and delete NGM and program files
def deleteInstallFiles():
    if os.path.exists(ngm_install):
        os.remove(ngm_install)
    else:
        pass
    if os.path.exists(repair_path):
        os.remove(repair_path)
    else:
        pass
    if os.path.exists(ngm_folder):
        shutil.rmtree(ngm_folder)
    else:
        pass
 
# web setting
def setting_web(weburl):
    driver_path = Type + '.exe'
    if driver_path == 'chromedriver.exe':
        option = webdriver.ChromeOptions()
        option.add_argument('--user-data-dir=C:/Users/' + Download + '/AppData/Local/Google/Chrome/User Data')
        option.add_argument(r'--profile-directory=Profile 1')
        driver = webdriver.Chrome(driver_path, chrome_options=option)
    else:
        option = Options()
        driver = webdriver.Edge(driver_path, options=option)
     
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get(weburl)
     
    if weburl == "https://help.nexon.com/Download/ngm":
        driver.find_element(By.ID, 'downngm').click()
        time.sleep(5)
        driver.quit()
    elif weburl == "https://help.nexon.com/Download/Restore":
        driver.find_element(By.ID, 'downngm').click()
        driver.switch_to.window(driver.window_handles[1]) # 새로 열린 창을 current window로 전환, 0 기본 - 새창 순서에 따라 숫자 증가
        driver.get_window_position(driver.window_handles[1]) # [1]창에 포지션
        driver.find_element(By.CSS_SELECTOR, '#footer > a:nth-child(1) > img').click()
        time.sleep(3)
        driver.quit()
 
# find the program using window titles
def checkWinTitle(programName):
    for w in pygetwindow.getAllTitles():
        try:
            if programName.lower() in w.lower():
                return False
        except:
            pass
    return True
 
# run NGM
def runInstallFiles(file_path, wintTitle):
    os.startfile(file_path)
    time.sleep(2)
    alive = pygetwindow.getWindowsWithTitle(wintTitle)[0]
    alive.activate()
    pyautogui.press('enter')
    time.sleep(0.5)
 
# check dead or live
def checkWinAlive(programName):
    while(True):
        time.sleep(0.5)
        print(programName + ' 설치 중')
        pyautogui.press('enter')
        if checkWinTitle(programName):
            print(programName + ' 설치 완료')
            pyautogui.press('enter')
            break
 
# check ver of NGM
def get_version_number(ngm_path):
    file_info = GetFileVersionInfo(ngm_path, '\\')
    ms = file_info['FileVersionMS']
    ls = file_info['FileVersionLS']
    return [str(HIWORD(ms)), str(LOWORD(ms)),
            str(HIWORD(ls)), str(LOWORD(ls))]
 
# compare ver of NGM
def check_version(ngm_path, repair = ""):
    version = '.'.join(get_version_number(ngm_path))
    if(version != Build):
        myTeamsMessage.text(repair + "NGM 버전이 맞지 않습니다.")
        myTeamsMessage.send()
        return False
    else:
        return True
 
 
def main():
    # 1-0. 잔여 파일 정리
    deleteInstallFiles()
     
    # 1-1. nexon 고객센터 - ngm 설치 파일 다운로드
    setting_web("https://help.nexon.com/Download/ngm")
  
  
    # 1-2. ngm 설치파일 실행
    ngm_install = "C:/Users/" + Download + "/Downloads/Install_NGM.exe"
    runInstallFiles(ngm_install, 'Nexon Installer')
 
 
    # 1-3. ngm 설치 완료 및 종료 확인
    checkWinAlive('Nexon Installer')
  
  
    # 1-4. nmg 버전 확인
    if check_version(ngm_path) == False:
        return
    else:
        pass
  
  
    # 2-0. ngm 파일 삭제
    os.remove("C:/ProgramData/Nexon/NGM/NGM.exe")
    os.remove("C:/ProgramData/Nexon/NGM/NGM64.exe")
    os.remove("C:/ProgramData/Nexon/NGM/NGMDll.dll")
    os.remove("C:/ProgramData/Nexon/NGM/NGMDll64.dll")
    os.remove("C:/ProgramData/Nexon/NGM/NGMResource.dll")
    os.remove("C:/ProgramData/Nexon/NGM/torbjorn.dll")
  
  
    # 2-1. 에러복구 프로그램 다운
    setting_web('https://help.nexon.com/Download/Restore')
  
  
    # 2-2. 에러복구 프로그램 시작
    repair_path = "C:/Users/" + Download + "/Downloads/NexonRepair.exe"
    runInstallFiles(repair_path, '넥슨 에러복구 프로그램')
  
  
    # 2-3. 에러복구 프로그램 설치 완료 및 종료 확인
    checkWinAlive('넥슨 에러복구 프로그램')
 
 
    # 2-4. 복구된 ngm 버전 재확인
    if check_version(ngm_path, '복구한 ') == False:
        return
    else:
        pass
     
    time.sleep(5) # Repair log가 생기기 전에 너무 빨리 확인이 들어가는 것을 방지
  
  
    # 2-5. repair 상태 확인 # 팀즈 봇
    ngm_64folder = r"C:\ProgramData\Nexon\NGM\webview_x64"
    if os.path.exists(ngm_64folder):
        myTeamsMessage.text("NGM 폴더 에러 복구에 문제가 발생했습니다. (webview 폴더 존재)")
        myTeamsMessage.send()
        return
  
    ngm_common_1 = r"C:\ProgramData\Nexon\Common\nl1gr.tmp"
    if os.path.exists(ngm_common_1):
        myTeamsMessage.text("Common 폴더 에러 복구에 문제가 발생했습니다. (nl1gr 파일 존재)")
        myTeamsMessage.send()
        return
  
    ngm_common_2 = r"C:\ProgramData\Nexon\Common\NexonRepair.log"
    if os.path.exists(ngm_common_2):
        pass
    else:
        myTeamsMessage.text("Common 폴더 에러 복구에 문제가 발생했습니다. (Repair 로그 부재)")
        myTeamsMessage.send()
        return
  
  
    # 3-1. 다음을 위해 설치한 파일 삭제
    if os.path.exists(ngm_install):
        os.remove(ngm_install)
    else:
        pass
    if os.path.exists(repair_path):
        os.remove(repair_path)
    else:
        pass
 
 
    # 3-2. 갱신 완료 안내
    myTeamsMessage.text("NGM 인증 갱신 확인을 마쳤습니다. 테스트를 종료합니다.")
    myTeamsMessage.send()
 
 
if __name__ == "__main__":
    main()
