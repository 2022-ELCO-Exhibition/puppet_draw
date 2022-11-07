import serial
import time
import cv2
import numpy as np
import torch

# 모델 로드
global model_num
model_num = 0

global start
start = False
global key
key = -1

# 인형에 대한 Yolo model을 Load
model_1 = torch.hub.load('yolov5', 'custom',path='weights/pink_best.pt', source='local')
# 찾은 객체의 신뢰도가 0.65이상이면 찾은 객체를 표시
model_1.conf = 0.65
# 한번에 찾을 객체의 Maximun수 (어차피 인형은 1개이므로 1개의 객체만 찾음)
model_1.max_det = 1


# 일정 delay동안 이미지를 띄움
def delay_with_img(delay):
    global key
    now = past = time.time()*1000.0
    while  (now- past < delay):
        ret, img = cap.read()
        # img, info = findDolls(img)
        cv2.imshow("Image", img)
        now = time.time()*1000.0
        # print(now - past)
        key = cv2.waitKey(33)
        if key == 27:  # ESC
            break

# 아두이노에서 "END"신호를 받기 전까지 대기
# 대기하면서 이미지를 화면에 띄운다.
def serial_return_delay():
    while True:

        ret, img = cap.read()
        img, info = findDolls(img)
        cv2.imshow("Image", img)

        key = cv2.waitKey(33)
        if key == 27:  # ESC
            break
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'

        if py_serial.readable():
            response = py_serial.readline()

        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)

        SIG = response[:len(response) - 2].decode()
        if SIG == "END":
            delay_with_img(500)
            break



# 학습한 yolo model을 통해서 객체(인형)을 찾고 표시
# 찾은 인형의 좌표값을 return한다.
def findDolls(img):
    name = " "
    # 모델의 종류를 결정 한다.
    # global model_num
    # 키보드 입력을 통해서 결정
    if model_num == 0:
        results = model_1(img)
        name = "PINK"
        bgr = (0, 0, 255)
    # elif model_num == 1:
    #     results = model_2(img)
    #     name = "RABBIT"
    #     bgr = (0, 255, 0)
    # elif model_num == 2:
    #     results = model_3(img)
    #     bgr = (0, 0, 255)
    #     name = "MARIN"

    labels, cord = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()
    n = len(labels)
    # print(labels)

    x_shape, y_shape = img.shape[1], img.shape[0]

    center = [0, 0]
    Area = 0
    for i in range(n):
        row = cord[i]
        if row[4] >= 0.2:
            x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
            center = [int((x1 + x2) / 2), int((y1 + y2) / 2)]
            Area = (x2 - x1) * (y2 - y1)
            cv2.circle(img, center, 2, (100, 100, 100), 2)
            cv2.rectangle(img, (x1, y1), (x2, y2), bgr, 2)

            cv2.putText(img, name
                        + ': ' + str(x1) + ', ' + str(x2) + ', ' + str(y1) + ', ' + str(y2),
                        (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

    cv2.putText(img, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 3)
    return img, [center, Area]


# 찾은 인형의 중심좌표를 아두이노에 전달하여 인형을 뽑고 다시 되돌아오는 작업
def py2Uno(x,y):
    commend_x = x
    py_serial.write(str(commend_x).encode())
    serial_return_delay()
    delay_with_img(500)

    commend_yy = y
    py_serial.write(str(commend_yy).encode())
    serial_return_delay()
    delay_with_img(400)

    commend = 1
    py_serial.write(str(commend).encode())
    serial_return_delay()
    delay_with_img(300)

    commend_z = -30700
    py_serial.write(str(commend_z).encode())
    serial_return_delay()
    delay_with_img(200)

    commend = 0
    py_serial.write(str(commend).encode())
    serial_return_delay()
    delay_with_img(500)

    commend_z = 30700
    py_serial.write(str(commend_z).encode())
    serial_return_delay()
    delay_with_img(500)

    commend_x = -x
    py_serial.write(str(commend_x).encode())
    serial_return_delay()
    delay_with_img(500)

    commend_yy = -y
    py_serial.write(str(commend_yy).encode())
    serial_return_delay()
    delay_with_img(500)

    commend = 1
    py_serial.write(str(commend).encode())
    serial_return_delay()
    delay_with_img(500)

    commend = 0
    py_serial.write(str(commend).encode())
    serial_return_delay()
    delay_with_img(500)

    ## x축은 2000만큼만 움직임
    ## y축은 2700만큼
    ## Z축은 -가 내리는 거임
    ## 1은 집게 벌리기 0은 집게 작기

    # if py_serial.readable():
    #     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    #     # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    #     response = py_serial.readline()
    #     # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    #     print(response[:len(response) - 1].decode())

# 연결된 휴대폰으로 이미지를 촬영
cap = cv2.VideoCapture(1)
# 아두이노와 Serial통신을 하기위한 작업
py_serial = serial.Serial(port='COM20', baudrate=115200,timeout=0.03)

while True:

    ret, img = cap.read()
    img, info = findDolls(img)
    cv2.imshow("Image", img)
    print("Center", info[0][0],info[0][1])

    if info[0][0]==0 and info[0][1]==0:
        print("NO DOLL")
        x=y=0
    else:
        x= (info[0][0]-173)*7.9766  + 10000
        y= (info[0][1]-360)*(-9.644)    +20000

        if x<0: x=0
        elif x>= 12050: x = 12040
        if y<0: y=0
        elif y>22700: y=22700
        print(int(x) , int(y))

    if start == True:
        commend_y = -22700
        py_serial.write(str(commend_y).encode())
        serial_return_delay()
        delay_with_img(200)
        py2Uno(x,y)

    start = False

    key_1 = cv2.waitKey(33)
    if key == 27 or key_1 == 27:  # ESC
        break

    # elif key_1 == 48:
    #     model_num = 0

    #  Enter키를 누르면 작동
    elif key==13 or key_1 == 13:
        start=True
        commend_y = 22700
        py_serial.write(str(commend_y).encode())
        serial_return_delay()
        delay_with_img(100)
        key = -1









