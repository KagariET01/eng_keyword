import PySimpleGUI as sg
import json
import pathlib
import csv
from gtts import gTTS 
import os 
import random
from playsound import playsound
st_num=0	#開始單字編號
ed_num=0	#結束單字編號
err=0		#錯誤數量
cho=0		#選擇
file_keyword=None	#要背的單字庫路徑
file_save=None		#儲存錯誤單字及st和ed
file_keyword_type=0	#1:csv 2:json
list_eng=[]
list_ch=[]
ed_max=-1

json_save_ex={"st":None,"ed":None,"keyword":[]}
keyword_ex={"eng":None,"ch":None}
wrong_json_list=[]
def choose(tt="1:否",tttype="int"):
	okey=0
	while(not(okey)):
		cho=0
		print(tt,"0:退出",sep="")
		cho=(input(">"))
		if(cho=="0"):
			print("確定要退出嗎？")
			print(tt,"0:確定退出",sep="")
			cho=int(input(">"))
			if(cho==0):
				print("See you next time.")
				exit()
		if(tttype=="int"):
			try:
				return int(cho)
			except:
				print("請輸入整數")
		elif(tttype=="text"):
			return cho
def f_soundplay(text="error",lang="en",slow=False):
	myobj=gTTS(text=text,lang=lang,slow=slow)
	myobj.save("./output.mp3")
	playsound("output.mp3")
	os.remove("./output.mp3")



print("歡迎來到ET01的背單字應用程式")	
cho=choose("1:選擇要背的檔案\n")
if (cho==1):
	#選擇要背的檔案
	print("將跳出檔案選擇框，請在選擇完檔案之後按ok")
	file_keyword = sg.popup_get_file('選擇要背的檔案',file_types = (('all_support',".csv .json"),('csv',".csv"),('json',".json"),('ALL Files', '*.*'),))
	extension=""
	while(file_keyword==None):
		print("你尚未選擇檔案，是否重選")
		cho=choose("1:重選檔案\n")
		file_keyword = sg.popup_get_file('選擇要背的檔案')
	print("確定要背這個檔案嗎？")
	print(file_keyword)
	cho=choose("1:確定\n2:重選\n")
	root, extension = os.path.splitext(file_keyword)
	if (extension==".csv"):
		file_keyword_type=1
	elif(extension==".json"):
		file_keyword_type=2
	#選擇儲存路徑
	print("將跳出檔案選擇框，請在選擇完檔案之後按ok")
	file_save = sg.popup_get_folder('選擇儲存檔路徑')
	while(file_save==None):
		print("你尚未選擇檔案，是否重選")
		cho=choose("1:重選檔案")
		file_save = sg.popup_get_folder('選擇儲存檔路徑')
	print("輸入檔名(不用加.json)")
	file_save=file_save+"/"+input(">")+".json"
	
	print("確定要儲存在這嗎？")
	print(file_save)
	cho=choose("1:確定\n2:重選\n")
	#載入檔案	
	print("載入檔案中")
	pathlib.Path(file_save).touch()		#建立檔案
	fs=open(file_save,"w")		#儲存檔
	fs.close()
	fs_j=json_save_ex			#儲存檔json
	fs_j_k=fs_j["keyword"]		#錯題檔的單字庫(json)
	fk=open(file_keyword,"r+",newline="")	#單字庫
	i=st_num
	ed_max=0
	if(file_keyword_type==1):#csv
		fk_c=csv.reader(fk, delimiter=',')
		for i in fk_c:
			ed_max=ed_max+1
			list_eng.append(i[0])
			list_ch.append(i[1])
	if(file_keyword_type==2):#json
		fk_j=json.load(fk)		#json單字庫檔案
		fk_j_k=fk_j["keyword"]	#單字庫json格式
		ed_max=len(fk_j_k)
		for i in range(0,ed_max,1):
			list_eng.append((fk_j_k[i])["eng"])
			list_ch.append((fk_j_k[i])["ch"])
	
	
	
	check=0
	while(check!=1):
		print("輸入起始單字編號(數字)")
		st_num=int(input(">"))-1
		fs_j["st"]=st_num
		fs_j["ed"]=0
		ed_num=0
		print("輸入結束單字編號(數字)，最大",ed_max)
		ed_num=int(input(">"))-1
		while(ed_num>ed_max-1):
			print("數字過於強大，導致系統無法接受")
			ed_num=int(input(">"))-1
		print("確定要背",st_num+1,"到",ed_num+1,"嗎？",sep="")	
		check=choose("1:確定\n2:重選\n")
	
	
	print("選擇模式")
	cho=choose("1:拼單字\n2:選中文\n3:背單字\n")
	if(cho==1):
		wrong_json_list=[]
		for i in range(st_num,ed_num+1,1):#拼單字
			now_eng=list_eng[i]
			now_ch=list_ch[i]
			ttext=now_ch+"，或者1:發音、"
			cho=1
			err_j=keyword_ex
			while(cho==1):
				cho=choose(ttext,"text")
				if(cho==1):
					f_soundplay(text=now_eng,lang="en",slow=False)
			if(cho==now_eng):
				print("O")
			else:
				print("X答案是"+now_eng)
				err_j={}
				err_j["eng"]=now_eng
				err_j["ch"]=now_ch
				fs_j_k.append(err_j)
				fs_j["keyword"]=fs_j_k
				err=err+1
			fs_j["ed"]=i
			fs=open(file_save,"w")
			fs.write(str(fs_j))
			fs.close
		print("成績單")
		print("模式：拼單字")
		print("開始單字編號",st_num+1)
		print("結束單字編號",st_num+1)
		print("錯題數",err)
	elif(cho==2):
		for i in range(st_num,ed_num+1,1):#選中文
			now_eng=list_eng[i]
			now_ch=list_ch[i]
			now_ch_list=["","","",""]
			for j in range(0,4,1):
				random_num=i
				while(random_num==i):
					random_num=random.randint(0,ed_max-1)
					now_ch_list[j]=list_ch[random_num]
			ans=int(random.randint(0,3))
			now_ch_list[ans]=now_ch
			cho=5
			while(cho==5):
				out="1:"+now_ch_list[0]+"\n2"+now_ch_list[1]+"\n3"+now_ch_list[2]+"\n4"+now_ch_list[3]+"\n或者5:念出單字\n"
				print(now_eng)
				cho=choose(out)
				if(cho==5):
					f_soundplay(text=now_eng,lang="en",slow=False)
				elif(cho==ans+1):
					print("O")
				else:
					print("X答案是",now_ch)
					err_j={}
					err_j["eng"]=now_eng
					err_j["ch"]=now_ch
					fs_j_k.append(err_j)
					fs_j["keyword"]=fs_j_k
					err=err+1
			fs_j["ed"]=i
			fs=open(file_save,"w")
			fs.write(str(fs_j))
			fs.close
		print("成績單")
		print("模式：選中文")
		print("開始單字編號",st_num+1)
		print("結束單字編號",st_num+1)
		print("錯題數",err)
	elif(cho==3):#背單字
		i=st_num
		while(True):
			now_eng=list_eng[i]
			now_ch=list_ch[i]
			print(now_ch,now_eng)
			while(True):
				cho=choose("1:上一個\n2:播放\n3:下一個\n")
				if (cho==1):
					if(i<=st_num):
						i=st_num
					else:
						i=i-1
						break
				if(cho==2):
					f_soundplay(text=now_eng,lang="en",slow=False)
				if(cho==3):
					if(i>=ed_num):
						i=ed_num
					else:
						i=i+1
						break
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
