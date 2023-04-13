import PySimpleGUI as sg
import json
#失敗品


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
ofs=None
have_file=0
list_eng=[]
list_ch=[]
list_err_eng=[]
list_err_ch=[]
ed_max=None

json_save_ex={"st":None,"now":None,"ed":None,"o_file":None,"keyword":[]}
keyword_ex={"eng":None,"ch":None}
wrong_json_list=[]
now=0
ofs_j=None
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
	while(True):
		print("將跳出檔案選擇框，請在選擇完檔案之後按ok")
		file_keyword = sg.popup_get_file('選擇要背的檔案',file_types = (('all_support',".csv .json"),('csv',".csv"),('json',".json"),('ALL Files', '*.*'),))
		extension=""
		if(file_keyword==None or file_keyword==""):
			print("你尚未選擇檔案，是否重選")
			cho=choose("1:重選檔案\n")
			if(cho==1):
				continue
			elif(cho==0):
				exit()
			else:
				print("fuck you幹麻亂填阿幹幹幹fuck you")
				exit()
		print("確定要背這個檔案嗎？")
		print(file_keyword)
		cho=choose("1:確定\n2:重選\n")
		if(cho==2):
			continue
		elif(cho==1):
			break
	root, extension = os.path.splitext(file_keyword)
	if (extension==".csv"):
		file_keyword_type=1
	elif(extension==".json"):
		file_keyword_type=2
	#選擇儲存路徑
	while(True):
		print("將跳出檔案選擇框，請在選擇完檔案之後按ok")
		file_save = sg.popup_get_folder('選擇儲存檔路徑')
		while(file_save==None or file_save==""):
			print("你尚未選擇檔案，是否重選")
			cho=choose("1:重選檔案")
			file_save = sg.popup_get_folder('選擇儲存檔路徑')
		print("輸入檔名(不用加.json)")
		file_save=file_save+"/"+input(">")+".json"
		print("確定要儲存在這嗎？")
		print(file_save)
		cho=choose("1:確定\n2:重選\n")
		if(cho==2):
			continue
		try:
			ofs=open(file_save,"r+",newline="")
		except:
			pathlib.Path(file_save).touch#建立檔案
			break
		#判別紀錄   
		try:
			print(ofs,type(ofs))#debug
			ofs_r=str(ofs.read())
			print(ofs_r,type(ofs_r))#debug
			ofs_j=json.loads(ofs_r)
			if(str(ofs_j["o_file"])==str(file_keyword)):
				print("偵測到你先前的紀錄，要開啟紀錄嗎？")
				cho=choose("1:開啟紀錄\n2:不開紀錄")
				if(cho==1):
					now=ofs_j["now"]
					st_num=ofs_j["st"]
					ed_num=ofs_j["ed"]
					have_file=1
					break
		except:
			print("未偵測到檔案紀錄")
			pass
		print("偵測到現有檔案，是否複寫？")
		cho=choose("1:複寫\n2:不複寫\n")
		if(cho==2):
			continue
		elif(cho==1):
			break
	#載入檔案
	print("載入檔案中")
	fs=open(file_save,"w")		#儲存檔
	if(have_file):
		fs_j=ofs_j
		fs.write(str(fs_j))
		fs.close
	else:
		fs_j=json_save_ex.copy()			#儲存檔json
		fs_j["o_file"]=file_keyword
	fs_j_k=fs_j["keyword"]		#錯題檔的單字庫(json)
	fk=open(file_keyword,"r+",newline="")	#單字庫
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
	
	
	
	if(not(have_file)):
		check=0
		while(check!=1):
			st_num=choose(("輸入起始單字編號(數字)，最大"+str(ed_max)+"或者"))-1
			while(st_num>ed_max or st_num<0):
				print("數字超出範圍，導致系統無法接受")
				st_num=choose(("輸入起始單字編號(數字)，最大"+str(ed_max)+"或者"))-1
			fs_j["st"]=st_num
			ed_num=0
			ed_num=choose(("輸入結束單字編號(數字)，最大"+str(ed_max)+"或者"))-1
			while(ed_num>ed_max or ed_num<0):
				print("數字過於強大，導致系統無法接受")
			fs_j["ed"]=ed_num
			print("確定要背",st_num+1,"到",ed_num+1,"嗎？",sep="")	
			check=choose("1:確定\n2:重選\n")
		
	
	print("選擇模式")
	cho=choose("1:拼單字\n2:選中文\n3:背單字\n")
	if(cho==1):#拼單字
		wrong_json_list=[]
		if(have_file):
			i=now
		else:
			i=st_num
		while(i<=ed_num):
			fs_j["now"]=i
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
			fs=open(file_save,"w")
			fs.write(str(fs_j))
			fs.close
			i=i+1
		print("成績單")
		print("模式：拼單字")
		print("開始單字編號",st_num+1)
		print("結束單字編號",st_num+1)
		print("錯題數",err)
	elif(cho==2):#選中文
		if(have_file):
			i=now
		else:
			i=st_num
		while(i<=ed_num):
			fs_j["now"]=i
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
			fs=open(file_save,"w")
			fs.write(str(fs_j))
			fs.close
			i=i+1
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
