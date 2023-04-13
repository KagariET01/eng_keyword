import PySimpleGUI as sg
import json
import pathlib
st_num=0	#開始單字編號
ed_num=0	#結束單字編號
err=0		#錯誤數量
cho=0		#選擇
file_keyword=None	#要背的單字庫路徑
file_save=None		#儲存錯誤單字及st和ed
file_keyword_type=0	#1:csv 2:json
list_eng=[]
list_ch=[]
list_err_eng=[]
list_err_ch=[]
ed_max=None

json_save_ex={"st":None,"ed":None,"keyword":[]}
keyword_ex={"eng":None,"ch":None}

def choose(tt="1:否"):
	cho=0
	print(tt,"0:退出",sep="")
	cho=int(input(">"))
	if(cho==0):
		print("確定要退出嗎？")
		print(tt,"0:確定退出",sep="")
		cho=int(input(">"))
		if(cho==0):
			print("See you next time.")
			exit()
	return cho




print("歡迎來到ET01的背單字應用程式")	
cho=choose("1:選擇要背的檔案\n")
if (cho==1):
	#選擇要背的檔案
	print("將跳出檔案選擇框，請在選擇完檔案之後按ok")
	file_keyword = sg.popup_get_file('選擇要背的檔案')
	while(file_keyword==None):
		print("你尚未選擇檔案，是否重選")
		cho=choose("1:重選檔案\n")
		file_keyword = sg.popup_get_file('選擇要背的檔案')
	print("確定要背這個檔案嗎？")
	print(file_keyword)
	cho=choose("1:確定\n2:重選\n")
	print("選擇檔案格式")
	file_keyword_type=choose("1:csv\n2:json\n")
	#選擇儲存路徑
	print("將跳出檔案選擇框，請在選擇完檔案之後按ok")
	file_save = sg.popup_get_folder('選擇儲存檔路徑')
	while(file_keyword==None):
		print("你尚未選擇檔案，是否重選")
		cho=choose("1:重選檔案")
		file_save = sg.popup_get_folder('選擇儲存檔路徑')
	print("確定要儲存在這嗎？")
	print(file_save)
	cho=choose("1:確定\n2:重選\n")
	print("輸入檔名(不用加.json)")
	file_save=file_save+"/"+input(">")+".json"
	pathlib.Path(file_save).touch()		#建立檔案
	print(file_save)
	#載入檔案	
	print("載入檔案中")
	fs=open(file_save,"w")		#儲存檔
	fs_j=json_save_ex			#儲存檔json
	fs_j_k=fs_j["keyword"]		#錯題檔的單字庫(json)
	fk=open(file_keyword,"r+")	#單字庫
	i=st_num
	ed_max=0
	if(file_keyword_type==1):#csv
		pass
	if(file_keyword_type==2):#json
		fk_j=json.load(fk)		#json單字庫檔案
		fk_j_k=fk_j["keyword"]	#單字庫json格式
		ed_max=len(fk_j_k)
		for i in range(0,ed_max,1):
			list_eng.append((fk_j_k[i])["eng"])
			list_ch.append((fk_j_k[i])["ch"])
	
	
	
	
	print("輸入起始單字編號(數字)")
	st_num=int(input(">"))-1
	fs_j["st"]=st_num
	fs_j["ed"]=0
	ed_num=0
	print("輸入結束單字編號(數字)，最大",ed_max)
	ed_num=int(input(">"))-1
	while(ed_num>ed_max):
		print("數字過於強大，導致系統無法接受")
		ed_num=int(input(">"))-1
	
	print(list_eng)#debug
	print(list_ch)#debug
	
	
	
	print("選擇模式")
	cho=choose("1:輸入單字\n2:選擇中文\n3:背單字\n")
	if(cho==1):
		for i in range(st_num,ed_num+1,1):
			pass
	
	if(cho==2):
		for i in range(st_num,ed_num+1,1):
			pass
	
	if(cho==3):
		for i in range(st_num,ed_num+1,1):
			pass  
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
