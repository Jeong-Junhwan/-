#시작하기전에 캡쳐도구로 학수번호-분반을 캡쳐해서 같은폴더에 1.PNG 2.PNG 이렇게 저장
#각 세부 수치는
#pyautogui.displayMousePosition()
#로 각자 계산
import pyautogui
from PIL import ImageGrab
import time
import keyboard
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

locations = []
#파일 개수만큼 돌리기
#OS로 파일개수 세면 편한데 귀찮음 잡고자 하는 과목수에 따라 수정 요망
for i in range(1,6):
    temp = pyautogui.locateOnScreen(str(i)+'.PNG')
    locations.append((pyautogui.center(temp)[0],pyautogui.center(temp)[1]))


def available_space(location):
    img = ImageGrab.grab((1183,location[1]-8,1230,location[1]+8)) #인원 제한부분 스크린샷 따오기
    img.save('temp.jpg')
    image = cv2.imread('temp.jpg')
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #--psm 6으로 숫자로 인식하도록
    try:
        text = pytesseract.image_to_string(gray, lang=None, config= '--psm 6')
        #text가 45/45 꼴이므로 eval로 계산하면 정원이 차면 1, 꽉 안차면 0~1 사이의 값이 나옴
        return eval(text.strip())
    except:
        return 1

def mouse_click(location):
    x = 355
    y = location[1]
    pyautogui.click(x,y) #신청 좌표 클릭
    time.sleep(0.6)
    pyautogui.press('enter', presses=2, interval=0.4) #클릭 후 혹시모르니 1초 간격으로 엔터 두번

def refresh_page():
    pyautogui.click(408,134) #수강신청 탭 좌표
    time.sleep(0.5) #페이지 로딩 시간 여유롭게

#f4키가 눌리면 프로그램 종료
while(keyboard.is_pressed('f4') == False):
    refresh_page()
    for location in locations:
        result = available_space(location)

        #1보다 작으면, 즉 빈자리가 있으면 해당 과목 신청 클릭
        if result < 1:
            mouse_click(location)
