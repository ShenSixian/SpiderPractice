import pymysql
class HtmlOutputer(object):
	"""docstring for HtmlOutputer"""
	def __init__(self):
		self.datas = []

	def add_new_data(self,datas):
		"""添加新的信息"""
		for data in datas:
			self.datas.append(data)
	"""	
	def output_to_excel(self):
		# 将数据输出至EXCEL表中
		fout = open('output.xls','w')
		fout.write("ID\tTITLE\tTIME\tURL\n")
		id = 1
		for data in self.datas:
			try:
				fout.write(str(id) + "\t")
				fout.write(data['title'] + "\t")
				fout.write(data['first_time'] + "\t")
				fout.write(data['url'] + "\n")
			except:					# 易出现编码问题，无法输入，进行报错
				fout.write("\n")
				print("error!")
			id = id + 1
		fout.close()
	"""

	def output_to_mysql(self):
		"""将数据导入数据库"""
		db = pymysql.connect("localhost","root","root1234","mytest", charset="utf8")
		cursor = db.cursor()
		cursor.execute("DROP TABLE IF EXISTS SpiderTest")
		# 使用预处理语句创建表
		sql = """CREATE TABLE SpiderTest (
				ID  INT NOT NULL,
				TITLE  VARCHAR(100),
				CREATION_TIME VARCHAR(20),
				LAST_REPLY_TIME VARCHAR(20),
				PASSAGE VARCHAR(3000),
				URL VARCHAR(250) )"""
		cursor.execute(sql)
		id = 1
		for data in self.datas:
			try:
				cursor.execute('insert into SpiderTest values("%d", "%s","%s","%s","%s","%s")' % (id, data['title'], data['first_time'], data['last_time'], data['passage'],data['url']))
				db.commit()
			except:
				db.rollback()			
			id = id + 1
		db.close()