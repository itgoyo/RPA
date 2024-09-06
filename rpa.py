import pyautogui
import time
import xlrd
import pyperclip

# 定义鼠标事件
def mouseClick(clickTimes, lOrR, img, reTry):
    if reTry == 1:
        location = pyautogui.locateOnScreen(img, confidence=0.9)
        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center, duration=0.1)
            pyautogui.click(clicks=clickTimes, interval=0.05, button=lOrR)
        else:
            print("未找到匹配图片")
    elif reTry == -1:
        while True:
            location = pyautogui.locateOnScreen(img, confidence=0.9)
            if location:
                center = pyautogui.center(location)
                pyautogui.moveTo(center, duration=0.1)
                pyautogui.click(clicks=clickTimes, interval=0.05, button=lOrR)
            time.sleep(0.1)
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
            location = pyautogui.locateOnScreen(img, confidence=0.9)
            if location:
                center = pyautogui.center(location)
                pyautogui.moveTo(center, duration=0.1)
                pyautogui.click(clicks=clickTimes, interval=0.05, button=lOrR)
                print("重复")
                i += 1
            time.sleep(0.1)

# 数据检查
def dataCheck(sheet1):
    checkCmd = True
    if sheet1.nrows < 2:
        print("没数据啊哥")
        return False
    
    for i in range(1, sheet1.nrows):
        cmdType = sheet1.row(i)[0]
        if cmdType.ctype != 2 or cmdType.value not in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]:
            print(f'第{i+1}行,第1列数据有毛病')
            checkCmd = False
        
        cmdValue = sheet1.row(i)[1]
        if cmdType.value in [1.0, 2.0, 3.0] and cmdValue.ctype != 1:
            print(f'第{i+1}行,第2列数据有毛病')
            checkCmd = False
        elif cmdType.value == 4.0 and cmdValue.ctype == 0:
            print(f'第{i+1}行,第2列数据有毛病')
            checkCmd = False
        elif cmdType.value in [5.0, 6.0] and cmdValue.ctype != 2:
            print(f'第{i+1}行,第2列数据有毛病')
            checkCmd = False
    
    return checkCmd

# 任务
def mainWork(sheet1):
    for i in range(1, sheet1.nrows):
        cmdType = sheet1.row(i)[0].value
        cmdValue = sheet1.row(i)[1].value
        
        if cmdType == 1.0:
            reTry = int(sheet1.row(i)[2].value) if sheet1.row(i)[2].ctype == 2 else 1
            mouseClick(1, "left", cmdValue, reTry)
            print(f"单击左键 {cmdValue}")
        elif cmdType == 2.0:
            reTry = int(sheet1.row(i)[2].value) if sheet1.row(i)[2].ctype == 2 else 1
            mouseClick(2, "left", cmdValue, reTry)
            print(f"双击左键 {cmdValue}")
        elif cmdType == 3.0:
            reTry = int(sheet1.row(i)[2].value) if sheet1.row(i)[2].ctype == 2 else 1
            mouseClick(1, "right", cmdValue, reTry)
            print(f"右键 {cmdValue}")
        elif cmdType == 4.0:
            pyperclip.copy(cmdValue)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            print(f"输入: {cmdValue}")
        elif cmdType == 5.0:
            time.sleep(cmdValue)
            print(f"等待 {cmdValue} 秒")
        elif cmdType == 6.0:
            pyautogui.scroll(int(cmdValue))
            print(f"滚轮滑动 {int(cmdValue)} 距离")

if __name__ == '__main__':
    file = 'cmd.xls'
    wb = xlrd.open_workbook(filename=file)
    sheet1 = wb.sheet_by_index(0)
    print('欢迎使用不高兴就喝水牌RPA~')
    
    if dataCheck(sheet1):
        key = input('选择功能: 1.做一次 2.循环到死 \n')
        if key == '1':
            mainWork(sheet1)
        elif key == '2':
            while True:
                mainWork(sheet1)
                time.sleep(0.1)
                print("等待0.1秒")
    else:
        print('输入有误或者已经退出!')
