#-*-coding: utf-8-*-
import os
import sys
import RPi.GPIO as GPIO
import socket
import threading

# 통신 정보 설정
IP = ''
PORT = 35000
SIZE = 1024
ADDR = (IP, PORT)
msg = ''

signup = []
idname = ""
pwd = ""
catName = ""
age = ""
catKind = ""

enableStepAuto = 0
Step1 = 0
Step2 = 3

tempAuto = "on"
tempState = "on"
temp1 = "31"
temp2 = "낮은온도"

weight = "1-2-3-4-5-6-7"
calAutoState = "on"
cal = "고열량"
feed = "자동"
feednum = "0"

playcount = "3-2-1-1-3-2-1"
snack = "주기"

health = "2-3-1-3-3-2-2"
healthStep = "위험"
healthState = "병원 방문이 필요합니다."

def server():
	global idname, pwd, catName, age, catKind
	global enableStepAuto, Step1, Step2
	global tempAuto, tempState, temp1, temp2
	global weight, cal, feed, feednum, calAutoState
	global playcount, snack
	global health, healthStep, healthState

	print("thread start")

	# 서버 소켓 설정
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind(ADDR)  # 주소 바인딩
		server_socket.listen(3)  # 클라이언트의 요청을 받을 준비
		client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
		print("connected")

	# 무한루프 진입
	while (True):
		msg = client_socket.recv(1024).decode()
		if msg!="" :
			print("[{}] massage : {}".format(client_addr, msg))

			if(msg[:5]=="회원가입,"):
				signup = msg.split(",",5)
				print("회원가입 : ",signup)
				idname = signup[1]
				pwd = signup[2]
				catName = signup[3]
				age = signup[4]
				catKind = signup[5]
			elif(msg=="로그인,"+idname+","+pwd): ### 로그인 성공할 id, pwd 처리 필요
				client_socket.sendall("로그인,성공\r\n".encode())
				print("message back to client : 로그인,성공")
			elif(msg[:2]=="계단"):
				if(msg=="계단"):
					if(enableStepAuto==0):
						client_socket.sendall("계단,{},{}\r\n".format(Step1,Step2).encode())
						print("message back to client : 계단,{},{}".format(Step1,Step2))
					else:
						client_socket.sendall("계단,{},{},auto\r\n".format(Step1,Step2).encode())
						print("message back to client : 계단,{},{},auto".format(Step1,Step2))
				elif(msg[0:3]=="계단,"):
					if(msg=="계단,auto"):
						enableStepAuto = 1
					else:
						enableStepAuto = 0

					if(enableStepAuto==0):
						Step1 = msg[3]
						Step2 = msg[5]
						client_socket.sendall("계단,{},{}\r\n".format(Step1,Step2).encode())
						print("message back to client : 계단,{},{}".format(Step1,Step2))
					else:
						client_socket.sendall("계단,{},{},auto\r\n".format(Step1,Step2).encode())
						print("message back to client : 계단,{},{},auto".format(Step1,Step2))
			elif(msg[:2]=="온도"):
				if(msg=="온도,on"):
					tempAuto = "off"
					tempState = "ON"
				elif(msg=="온도,off"):
					tempAuto = "off"
					tempState = "OFF"
				elif(msg=="온도,auto"):
					tempAuto = "on"
				if(tempAuto=="off"):
					client_socket.sendall("온도,{},{},{}\r\n".format(temp1,temp2,tempState).encode())
					print("message back to client : 온도,{},{}".format(temp1,temp2))
					print("tempState : {}".format(tempState))
				else:
					client_socket.sendall("온도,{},{},auto/{}\r\n".format(temp1,temp2,tempState).encode())
					print("message back to client : 온도,{},{}".format(temp1,temp2))
					print("tempState : auto/{}".format(tempState))
			elif(msg[:2]=="체중"):
				if(msg=="체중"):
					if(calAutoState=="off"):
						client_socket.sendall("체중,{},{},{},{}\r\n".format(weight,cal,feed,feednum).encode())
						print("message back to client : 체중,{},{},{},{}".format(weight,cal,feed,feednum))
					else:
						client_socket.sendall("체중,{},auto,{},{},{}\r\n".format(weight,cal,feed,feednum).encode())
						print("message back to client : 체중,{},auto,{},{},{}".format(weight,cal,feed,feednum))
				elif(msg=="체중,저열량"):
					calAutoState="off"
					cal = "저열량"
					client_socket.sendall("체중,{}\r\n".format(cal).encode())
					print("message back to client : 체중,{}".format(cal))
				elif(msg=="체중,고열량"):
					calAutoState="off"
					cal = "고열량"
					client_socket.sendall("체중,{}\r\n".format(cal).encode())
					print("message back to client : 체중,{}".format(cal))
				elif(msg=="체중,auto"):
					calAutoState="on"
					client_socket.sendall("체중,auto,{}\r\n".format(cal).encode())
					print("message back to client : 체중,auto,{}".format(cal))
				elif(msg=="체중,수동"):
					feed = "수동"
					client_socket.sendall("체중,{},{}\r\n".format(feed,feednum).encode())
					print("message back to client : 체중,{},{}".format(feed,feednum))
				elif(msg=="체중,자동"):
					feed = "자동"
					client_socket.sendall("체중,{},{}\r\n".format(feed,feednum).encode())
					print("message back to client : 체중,{},{}".format(feed,feednum))
				elif(msg[3]>="0" or msg[3]<="3"):
					feed = "수동"
					feednum = msg[3]
					client_socket.sendall("체중,수동,{}\r\n".format(feednum).encode())
					print("message back to client : 체중,수동,{}".format(feednum))
			elif(msg[:2]=="운동"):
				if(msg=="운동"):
					client_socket.sendall("운동,{},{}\r\n".format(playcount,snack).encode())
					print("message back to client : 운동,{},{}".format(playcount,snack))
				elif(msg=="운동,주기"):
					snack = "주기"
					client_socket.sendall("운동,{}\r\n".format(snack).encode())
					print("message back to client : 운동,{}".format(snack))
				elif(msg=="운동,안주기"):
					snack = "안주기"
					client_socket.sendall("운동,{}\r\n".format(snack).encode())
					print("message back to client : 운동,{}".format(snack))
				elif(msg=="운동,auto"):
					snack = "auto/"+snack
					client_socket.sendall("운동,{}\r\n".format(snack).encode())
					print("message back to client : 운동,{}".format(snack))
			elif(msg=="건강"):
				client_socket.sendall("건강,{},{},{}\r\n".format(health,healthStep,healthState).encode())
				print("message back to client : 건강,{},{},{}".format(health,healthStep,healthState))
			elif(msg[:2]=="정보"):
				if(msg=="정보"):
					client_socket.sendall("정보,{},{},{}\r\n".format(catName,age,catKind).encode())
					print("message back to client : 정보,{},{},{}".format(catName,age,catKind))
				elif(msg=="정보,cancel"):
					pass
				else:
					signup = msg.split(",",3)
					print("정보 변경 : ",signup)
					catName = signup[1]
					age = signup[2]
					catKind = signup[3]
					client_socket.sendall("정보,{},{},{}\r\n".format(catName,age,catKind).encode())
					print("message back to client : 정보,{},{},{}".format(catName,age,catKind))
	client_socket.close()  # 클라이언트 소켓 종료

t=threading.Thread(target=server, daemon=True)
t.start()

# main
while True:
	try:
		pass
	except KeyboardInterrupt:
		# Ctrl + C
		GPIO.cleanup()
		sys.exit()
	except:
		print("problem!!")