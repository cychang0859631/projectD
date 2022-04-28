from re import X
from flask import Flask,render_template,url_for,redirect,request
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn import metrics
from flask_mysqldb import MySQL
import joblib

import base64
from io import BytesIO

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



data_record=[]
test_data=[]
target = 0
col = 0
dep =""
career=""
ac=0
app=Flask(__name__)
model_ae = joblib.load('model_ae_dummy.pkl')
model_pa = joblib.load('model_PA.pkl')
model_sp = joblib.load('model_SP.pkl')
target_class = {'A': '學術導向', 'B': '本校進修', 'C': '就業導向', 'D': '它校進修'}


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'A15446546ab'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/student',methods=['POST','GET'])
def student():
	global target
	global col
	global dep
	global career
	global test_data
	global data_record
	global ac
	if request.method == "POST":
		test_data=[]
		data_record=[]
		details = request.form
		stid=details['stid']
		dep = details['dep']
		sex = float(details['sex'])
		if sex==1:
			sex_var='男'
			test_data.extend([1,0])
		else:
			sex_var='女'
			test_data.extend([0,1])
		ac = float(details['ac'])
		if ac==0:
			ac_var='考試入學'
		elif ac==1:
			ac_var='個人申請'
		elif ac==2:
			ac_var='繁星入學'
		col = float(details['col'])
		if col==6:
			col_var='電機學院'
			test_data.extend([0,0,0,0,0,0,1])
		elif col==3:
			col_var='生物科技學院'
			test_data.extend([0,0,0,1,0,0,0])
		elif col==5:
			col_var='資訊學院'
			test_data.extend([0,0,0,0,0,1,0])
		elif col==1:
			col_var='工學院'
			test_data.extend([0,1,0,0,0,0,0])
		elif col==2:
			col_var='理學院'
			test_data.extend([0,0,1,0,0,0,0])
		elif col==4:
			col_var='管理學院'
			test_data.extend([0,0,0,0,1,0,0])
		elif col==0:
			col_var='人文社會學院'
			test_data.extend([1,0,0,0,0,0,0])
		elif col==7:
			col_var='客家文化學院'
			test_data.extend([1,0,0,0,0,0,0])
		mathscore = int(details['mathscore'])
		test_data.append(mathscore)
		dep = details['dep']
		print(test_data)
		#模型list
		# list_test=[sex,col,mathscore]		
		# for i in list_test:
		# 	test_data.append(i)
		#紀錄list
		list_record=[stid,sex_var,ac_var,col_var,dep,mathscore]
		for i in list_record:
			data_record.append(i)
		# test_data=np.array(test_data)
		# print(test_data)
		'''
		X = np.array([sex,col,mathscore,cal_1,cal_2,ecr_1,noncal_credit_1,noncal_mean_1,ecr_2,cal_credit_2,cal_mean_2,noncal_credit_2,noncal_mean_2,ecr_3,cal_credit_3,cal_mean_3,noncal_credit_3,noncal_mean_3,ecr_4,cal_credit_4,cal_mean_4,noncal_credit_4,noncal_mean_4,gpa])
		X = X.reshape(1,-1)
		target = target_class[model_ae.predict(X)[0]]
		if target=="就業導向":
			career="就業"
		elif target=="學術導向":
			career="往學術領域發展"
		elif target=="本校進修":
			career="在交大進修碩士班"
		elif target=="它校進修":
			career="在其他學校進修"'''
		#return render_template('t3.html',data=sex_var,data1=col_var,data2=ac_var,data3=dep)
		return redirect(url_for('student1'))
	return render_template('student.html')

@app.route('/student1',methods=['POST','GET'])
def student1():
	global test_data
	global data_record
	cur = mysql.connection.cursor()
	query_string = "SELECT * FROM test.calculus_class where course_dep = %s"
	cur.execute(query_string, (dep,))
	#cur.execute("SELECT * FROM test.calculus_class where course_dep = (%s)",("土木工程學系"))
	fetchdata = cur.fetchall()
	cur.close()
	if request.method == "POST":
		print('heool')
		details = request.form
		cal_1 = int(details['cal_1'])
		cal_2 = int(details['cal_2'])
		cal_credit_2 = int(details['cal_credit_2'])
		cal_mean_2 = float(details['cal_mean_2'])
		cal_credit_3 = int(details['cal_credit_3'])
		cal_mean_3 = float(details['cal_mean_3'])
		cal_credit_4 = int(details['cal_credit_4'])
		cal_mean_4 = float(details['cal_mean_4'])
		if ac==0:
			if cal_1 == 0:
				cal_1_m = 58
			else:
				cal_1_m= cal_1
			if cal_2 == 0:
				cal_2_m = 60
			else:
				cal_2_m= cal_2
			if cal_credit_2 == 0:
				cal_credit_2_m = 12
				cal_mean_2_m = 74.66
			else:
				cal_credit_2_m = cal_credit_2
				cal_mean_2_m = cal_mean_2
			if cal_credit_3 == 0:
				cal_credit_3_m = 8
				cal_mean_3_m = 76.86
			else:
				cal_credit_3_m = cal_credit_3
				cal_mean_3_m = cal_mean_3
			if cal_credit_4 == 0:
				cal_credit_4_m = 5
				cal_mean_4_m = 73.74
			else:
				cal_credit_4_m = cal_credit_4
				cal_mean_4_m = cal_mean_4
		elif ac==1:
			if cal_1 == 0:
				cal_1_m = 59
			else:
				cal_1_m= cal_1
			if cal_2 == 0:
				cal_2_m = 59
			else:
				cal_2_m= cal_2
			if cal_credit_2 == 0:
				cal_credit_2_m = 10
				cal_mean_2_m = 75.59
			else:
				cal_credit_2_m = cal_credit_2
				cal_mean_2_m = cal_mean_2
			if cal_credit_3 == 0:
				cal_credit_3_m = 7
				cal_mean_3_m = 79.09
			else:
				cal_credit_3_m = cal_credit_3
				cal_mean_3_m = cal_mean_3
			if cal_credit_4 == 0:
				cal_credit_4_m = 4
				cal_mean_4_m = 75.20
			else:
				cal_credit_4_m = cal_credit_4
				cal_mean_4_m = cal_mean_4
		elif ac==2:
			if cal_1 == 0:
				cal_1_m = 56
			else:
				cal_1_m= cal_1
			if cal_2 == 0:
				cal_2_m = 59
			else:
				cal_2_m= cal_2
			if cal_credit_2 == 0:
				cal_credit_2_m = 9
				cal_mean_2_m = 78.33
			else:
				cal_credit_2_m = cal_credit_2
				cal_mean_2_m = cal_mean_2
			if cal_credit_3 == 0:
				cal_credit_3_m = 7
				cal_mean_3_m = 80.04
			else:
				cal_credit_3_m = cal_credit_3
				cal_mean_3_m = cal_mean_3
			if cal_credit_4 == 0:
				cal_credit_4_m = 4
				cal_mean_4_m = 79.29
			else:
				cal_credit_4_m = cal_credit_4
				cal_mean_4_m = cal_mean_4
		list_test=[cal_1_m,cal_2_m,cal_credit_2_m,cal_mean_2_m,cal_credit_3_m,cal_mean_3_m,cal_credit_4_m,cal_mean_4_m]
		list_record=[cal_1,cal_2,cal_credit_2,cal_mean_2,cal_credit_3,cal_mean_3,cal_credit_4,cal_mean_4]
		for i in list_test:
			test_data.append(i)
		print(test_data)
		for i in list_record:
			data_record.append(i)
		print(data_record)
		return redirect(url_for('student2'))
		#return render_template('student2.html')
	return render_template('student1.html',data=fetchdata)

@app.route('/student2',methods=['POST','GET'])
def student2():
	global test_data
	global target
	global career
	global data_record
	if request.method == "POST":
		details = request.form
		noncal_credit_1 = int(details['noncal_credit_1'])
		noncal_mean_1 = float(details['noncal_mean_1'])
		noncal_credit_2 = int(details['noncal_credit_2'])
		noncal_mean_2 = float(details['noncal_mean_2'])
		noncal_credit_3 = int(details['noncal_credit_3'])
		noncal_mean_3 = float(details['noncal_mean_3'])
		noncal_credit_4 = int(details['noncal_credit_4'])
		noncal_mean_4 = float(details['noncal_mean_4'])
		ecr_1 = float(details['ecr_1'])
		ecr_2 = float(details['ecr_2'])
		ecr_3 = float(details['ecr_3'])
		ecr_4 = float(details['ecr_4'])
		gpa = float(details['gpa'])
		list_test=[noncal_credit_1,noncal_mean_1,noncal_credit_2,noncal_mean_2,noncal_credit_3,noncal_mean_3,noncal_credit_4,noncal_mean_4,ecr_1,ecr_2,ecr_3,ecr_4,gpa]		
		for i in list_test:
			test_data.append(i)
			data_record.append(i)
		print(test_data)
		print(data_record)
		X = np.array(test_data)
		'''
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO data_record(stid, sex, ac, col, dep, mathscore, cal_1, cal_2, cal_credit_2, cal_mean_2, cal_credit_3, cal_mean_3, cal_credit_4, cal_mean_4, noncal_credit_1, noncal_mean_1, noncal_credit_2, noncal_mean_2, noncal_credit_3, noncal_mean_3, noncal_credit_4, noncal_mean_4, ecr_1, ecr_2, ecr_3, ecr_4, gpa, news_career_1, news_other_1, news_career_2, news_other_2, news_career_3, news_other_3, pre_target, agree, real_target, other_career, choose_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)", (X[0], X[1], X[2], X[3], X[4], X[5], X[6], X[7], X[8], X[9], X[10], X[11], X[12], X[13], X[14], X[15], X[16], X[17], X[18], X[19], X[20], X[21], X[22], X[23], X[24], X[25], X[26], X[27], X[28], X[29], X[30], X[31], X[32], X[33], X[34], X[35], X[36], X[37]))
		mysql.connection.commit()
		cur.close()'''
		X = X.reshape(1,-1)
		if ac==0:
			target = target_class[model_ae.predict(X)[0]]
		elif ac==1:
			target = target_class[model_pa.predict(X)[0]]
		elif ac==2:
			target = target_class[model_sp.predict(X)[0]]
		#target = target_class[model_ae.predict(X)[0]]
		print(target)
		if target=="就業導向":
			career="就業"
		elif target=="學術導向":
			career="往學術領域發展"
		elif target=="本校進修":
			career="在交大進修碩士班"
		elif target=="它校進修":
			career="在其他學校進修"
		return redirect(url_for('news1'))
	return render_template('student2.html')

@app.route('/news1',methods=['POST','GET'])
def news1():
	global data_record
	if request.method == "POST":
		details = request.form
		news_career_1=details['news_career_1']
		news_other_1=details['news_other_1']
		data_record.append(news_career_1)
		data_record.append(news_other_1)
		return redirect(url_for('news2'))
	return render_template('news_job.html')

@app.route('/news2',methods=['POST','GET'])
def news2():
	global data_record
	if request.method == "POST":
		details = request.form
		news_career_2=details['news_career_2']
		news_other_2=details['news_other_2']
		data_record.append(news_career_2)
		data_record.append(news_other_2)
		return redirect(url_for('news3'))
	return render_template('news_graduate.html')

@app.route('/news3',methods=['POST','GET'])
def news3():
	global data_record
	if request.method == "POST":
		details = request.form
		news_career_3=details['news_career_3']
		news_other_3=details['news_other_3']
		data_record.append(news_career_3)
		data_record.append(news_other_3)
		return redirect(url_for('confirm'))
	return render_template('news_graduate_other.html')


#確認職涯方向-------------------------------------------------------------
@app.route('/confirm',methods=['POST','GET'])
def confirm():
	global data_record
	if request.method == "POST":
		con=request.form.get('career')
		ot=request.form.get('othercareer')
		other_car=request.form.get('other_car')
		reason=request.form.get('reason')
		data_record.append(target)
		data_record.append(con)
		data_record.append(ot)
		data_record.append(other_car)
		data_record.append(reason)
		print(data_record)
		X=data_record
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO data_record(stid, sex, ac, col, dep, mathscore, cal_1, cal_2, cal_credit_2, cal_mean_2, cal_credit_3, cal_mean_3, cal_credit_4, cal_mean_4, noncal_credit_1, noncal_mean_1, noncal_credit_2, noncal_mean_2, noncal_credit_3, noncal_mean_3, noncal_credit_4, noncal_mean_4, ecr_1, ecr_2, ecr_3, ecr_4, gpa, news_career_1, news_other_1, news_career_2, news_other_2, news_career_3, news_other_3, pre_target, agree, real_target, other_career, choose_reson) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)", (X[0], X[1], X[2], X[3], X[4], X[5], X[6], X[7], X[8], X[9], X[10], X[11], X[12], X[13], X[14], X[15], X[16], X[17], X[18], X[19], X[20], X[21], X[22], X[23], X[24], X[25], X[26], X[27], X[28], X[29], X[30], X[31], X[32], X[33], X[34], X[35], X[36], X[37]))
		mysql.connection.commit()
		cur.close()
		if target=='就業導向':
			if con=='y':
				return redirect(url_for('e1'))
			elif con=='n':
				if ot =='original':
					return redirect(url_for('ao1'))
				elif ot =="other_school":
					return redirect(url_for('aot1'))
				elif ot =="original_PhD":
					return redirect(url_for('aop1'))
				elif ot =="other":
					return redirect(url_for('advisory'))
		elif target=='學術導向':
			if con=='y':
				return redirect(url_for('aop1'))
			elif con=='n':
				if ot =='original':
					return redirect(url_for('ao1'))
				elif ot =="other_school":
					return redirect(url_for('aot1'))
				elif ot =="employment":
					return redirect(url_for('e1'))
				elif ot =="other":
					return redirect(url_for('advisory'))
		elif target=='本校進修':
			if con=='y':
				return redirect(url_for('ao1'))
			elif con=='n':
				if ot =="original_PhD":
					return redirect(url_for('aop1'))
				elif ot =="other_school":
					return redirect(url_for('aot1'))
				elif ot =="employment":
					return redirect(url_for('e1'))
				elif ot =="other":
					return redirect(url_for('advisory'))
		elif target=='它校進修':
			if con=='y':
				return redirect(url_for('ao1'))
			elif con=='n':
				if ot =="original_PhD":
					return redirect(url_for('aop1'))
				if ot =='original':
					return redirect(url_for('ao1'))
				elif ot =="employment":
					return redirect(url_for('e1'))
				elif ot =="other":
					return redirect(url_for('advisory'))
	return render_template('confirm.html',data=target,career=career)
#--------------------------------------------------------------------------

#就業---------------------------------------------------------------
@app.route('/employment')
def e1():
	return render_template('就業導向/guide.html')

@app.route('/employment/job_intro')
def e2():
	job_type=[]
	job_count=[]
	job_salary=[]
	cur = mysql.connection.cursor()
	cur.execute("SELECT dep,job_type,count(job_type) as 個數,avg(job_salary) as 平均薪水 FROM test.dep_salary where dep='電機工程學系' group by dep,job_type HAVING count(job_type) > 1")
	fetchdata = cur.fetchall()
	cur.close()
	print(len(fetchdata))
	for i in range(len(fetchdata)):
		job_type.append(fetchdata[i][1])
		job_count.append(fetchdata[i][2])
		job_salary.append(fetchdata[i][3])
	print(job_type)
	print(job_count)
	plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
	#畫圖--------------------------------------------------------
	# sizes = [15, 30, 45, 10]
	# labels = ['5555555', 'Hogs6666', 'Dogs66666', 'Logs66666']
	# plt.xticks(rotation=45, ha='right')
	plt.rcParams["figure.figsize"] = (8, 6)
	plt.subplot(211)
	plt.pie(job_count,labels=job_type)
	plt.tight_layout()
	plt.legend()
	plt.subplot(212)
	plt.xticks(rotation=45, ha='right')
	plt.bar(job_type,job_salary)
	plt.tight_layout()
	# plt.show()
	#轉二進制
	buffer = BytesIO()
	plt.savefig(buffer)
	plot_data =buffer.getvalue()
	imb=base64.b64encode(plot_data)
	ims = imb.decode()
	imd = "data:image/png;base64," + ims
	return render_template("就業導向/job_col_intro copy.html",image=imd)

@app.route('/employment/job_intro2')
def e2_2():
	job_type=[]
	job_count=[]
	job_salary=[]
	cur = mysql.connection.cursor()
	cur.execute("SELECT dep,job_type,count(job_type) as 個數,avg(job_salary) as 平均薪水 FROM test.dep_salary where dep='電機工程學系' group by dep,job_type HAVING count(job_type) > 1")
	fetchdata = cur.fetchall()
	cur.close()
	print(len(fetchdata))
	for i in range(len(fetchdata)):
		job_type.append(fetchdata[i][1])
		job_count.append(fetchdata[i][2])
		job_salary.append(fetchdata[i][3])
	print(job_type)
	print(job_count)
	plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
	#畫圖--------------------------------------------------------
	'''
	plt.pie(job_count,labels=job_type)
	plt.tight_layout()
	plt.legend(loc=0)
	#轉二進制
	buffer = BytesIO()
	plt.savefig(buffer)
	plot_data =buffer.getvalue()
	imb=base64.b64encode(plot_data)
	ims = imb.decode()
	imd = "data:image/png;base64," + ims
	'''
	imd=draw_pie(job_count,job_type)
	imd1=draw_bar(job_type,job_salary)
	'''
	plt.clf()
	
	
	plt.bar(job_type,job_salary)
	plt.tight_layout()
	buffer1 = BytesIO()
	plt.savefig(buffer1)
	plot_data1 =buffer1.getvalue()
	imb1=base64.b64encode(plot_data1)
	ims1 = imb1.decode()
	imd1 = "data:image/png;base64," + ims1
	'''
	return render_template("就業導向/job_col_intro copy.html",image=imd,image1=imd1)

def draw_pie(count,label):
	plt.clf()
	plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
	plt.pie(count,labels=label)
	plt.tight_layout()
	plt.legend(loc=0)
	#轉二進制
	buffer = BytesIO()
	plt.savefig(buffer)
	plot_data =buffer.getvalue()
	imb=base64.b64encode(plot_data)
	ims = imb.decode()
	imd = "data:image/png;base64," + ims
	return imd

def draw_bar(label,num):
	plt.clf()
	plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
	plt.xticks(rotation=45, ha='right')
	plt.bar(label,num)
	for index, value in enumerate(num):
		plt.text(index,value, int(value),fontsize=15, ha='center')
	plt.tight_layout()
	#轉二進制
	buffer = BytesIO()
	plt.savefig(buffer)
	plot_data =buffer.getvalue()
	imb=base64.b64encode(plot_data)
	ims = imb.decode()
	imd = "data:image/png;base64," + ims
	return imd


@app.route('/employment/job_interview1')
def e3_1():
	return render_template('就業導向/job_interview copy.html')

@app.route('/employment/job_interview2')
def e3_2():
	return render_template('就業導向/job_interview2.html')

@app.route('/employment/job_interview3')
def e3_3():
	return render_template('就業導向/job_interview3.html')

@app.route('/employment/job_find')
def e4():
	return render_template('就業導向/job_other copy.html')

@app.route('/employment/job_class')
def e5():
	return render_template('就業導向/recommend copy 2.html')
#-----------------------------------------------------------------------------

#原校進修---------------------------------------------------------------------
@app.route('/advance_original')
def ao1():
	return render_template('原校進修導向/guide.html')

@app.route('/advance_original/graduate_intro')
def ao2():
	return render_template('原校進修導向/graduate_ee.html')

@app.route('/advance_original/graduate_recom')
def ao3():
	return render_template('原校進修導向/graduate_recom.html')

@app.route('/advance_original/graduate_channel')
def ao4():
	return render_template('原校進修導向/graduate_channel.html')

@app.route('/advance_original/graduate_class')
def ao5():
	return render_template('原校進修導向/recommend copy 2.html')
#---------------------------------------------------------------------

#他校進修---------------------------------------------------------------------
@app.route('/advance_other')
def aot1():
	return render_template('他校進修導向/guide.html')

@app.route('/advance_other/graduate_intro')
def aot2():
	return render_template('他校進修導向/graduate_ee.html')

@app.route('/advance_other/graduate_recom')
def aot3():
	return render_template('他校進修導向/graduate_recom.html')

@app.route('/advance_other/graduate_channel')
def aot4():
	return render_template('他校進修導向/graduate_channel.html')

@app.route('/advance_other/graduate_channel_abroad')
def aot5():
	return render_template('他校進修導向/advance_abroad.html')

@app.route('/advance_other/graduate_class')
def aot6():
	return render_template('他校進修導向/recommend copy 2.html')
#---------------------------------------------------------------------

#學術導向---------------------------------------------------------------------
@app.route('/advance_PhD')
def aop1():
	return render_template('學術導向/guide.html')

@app.route('/advance_PhD/graduate_intro')
def aop2():
	return render_template('學術導向/graduate_ee.html')

@app.route('/advance_PhD/graduate_recom')
def aop3():
	return render_template('學術導向/graduate_recom.html')

@app.route('/advance_PhD/graduate_channel1')
def aop4_1():
	return render_template('學術導向/graduate_channel.html')

@app.route('/advance_PhD/graduate_channel2')
def aop4_2():
	return render_template('學術導向/graduate_channel1.html')

@app.route('/advance_PhD/graduate_class')
def aop5():
	return render_template('學術導向/recommend copy 2.html')
#---------------------------------------------------------------------

#職涯諮詢----------------------------------------------------------
@app.route('/advisory')
def advisory():
	return render_template('advisory.html')
#-----------------------------------------------------------------
'''
insert資料庫
@app.route('/ass')
def ass():
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO myusers(firstname, lastname) VALUES (%s, %s)", ("八蛋", "王"))
	mysql.connection.commit()
	cur.close()
	return render_template('t3.html')
'''
@app.route('/job')
def job():
	cur = mysql.connection.cursor()
	cur.execute("SELECT job_class FROM test.job GROUP BY job_class;")
	#cur.execute("SELECT * FROM test.job where job_col = '電機學院'")
	fetchdata = cur.fetchall()
	cur.execute("SELECT * FROM test.job")
	fetchdata1 = cur.fetchall()
	cur.close()
	'''
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM test.job where job_class = '專案管理'")
	fetchdata = cur.fetchall()
	cur.execute("SELECT * FROM test.job where job_class = '軟體工程'")
	fetchdata1 = cur.fetchall()
	cur.execute("SELECT * FROM test.job where job_class = '半導體元件'")
	fetchdata2 = cur.fetchall()
	mysql.connection.commit()
	cur.close()'''
	return render_template('job.html', subtitle = fetchdata, data = fetchdata1)


@app.route('/test',methods=['POST','GET'])
def test():
	if request.method == "POST":
		details = request.form
		data = details['id']
		data1 = details['timee']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO timee(id, timee) VALUES (%s, %s)", (data, data1))
		mysql.connection.commit()
		cur.close()
		return render_template('tt.html',data=data,data1=data1)
	return render_template('tt.html')

#-----畫圖
# @app.route("/pp", methods=["GET"])
# def pp():
# 	job_type=[]
# 	job_count=[]
# 	cur = mysql.connection.cursor()
# 	cur.execute("SELECT dep,job_type,avg(job_salary) as 平均薪水 FROM test.dep_salary where dep='電機工程學系' group by dep,job_type")
# 	fetchdata = cur.fetchall()
# 	cur.close()
# 	print(len(fetchdata))
# 	for i in range(len(fetchdata)):
# 		job_type.append(fetchdata[i][1])
# 		job_count.append(fetchdata[i][2])
# 	print(job_type)
# 	print(job_count)
# 	plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
# 	sizes = [15, 30, 45, 10]
# 	labels = ['5555555', 'Hogs6666', 'Dogs66666', 'Logs66666']
# 	plt.xticks(rotation=45, ha='right')
# 	plt.tight_layout()
# 	plt.bar(job_type,job_count)
# 	plt.tight_layout()
# 	# plt.show()
# 	buffer = BytesIO()
# 	plt.savefig(buffer)
# 	plot_data =buffer.getvalue()
# 	imb=base64.b64encode(plot_data)
# 	ims = imb.decode()
# 	imd = "data:image/png;base64," + ims
# 	return render_template("image.html",image=imd)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='9000',debug=True)
