from bs4 import BeautifulSoup
import html_downloader
import re
class HtmlParser(object):
	"""HTML解析器"""
	def parse(self,html_cont):
		"""解析器"""
		if html_cont is None:
			return
		soup = BeautifulSoup(html_cont, "html5lib")
		new_data = self.get_new_data(soup)
		next_url = self.get_next_url(soup)
		return next_url,new_data

	def get_next_url(self,soup):
		"""获取下一个要解析的URL"""
		# <a href="http://bbs.ghtt.net/forum-93-2.html" class="nxt">下一页</a>
		next_page_node = soup.find('a',class_="nxt")
		next_page_url = next_page_node['href']
		return next_page_url

	def get_new_data(self,soup):
		"""获取所需要的信息"""
		res_data = []
		# <a href="http://bbs.ghtt.net/thread-2046718-1-1.html" style="font-weight: bold;color: #EE1B2E;" onclick="atarget(this)" class="s xst">关于禁止发布买卖公共考研座位的通知</a>
		nodes = soup.find_all('a',class_="s xst")
		for node in nodes:
			data = {}

			title = node.get_text()							# 标题
			data['title'] = title

			child_url = node['href']
			data['url'] = child_url							# 对应的URL

			data['time'] = self.get_child_data(child_url)								# 进入帖子并获取信息
			res_data.append(data)

		return res_data

	def get_child_data(self,url):
		"""获取子网页信息"""
		try:
			downloader = html_downloader.HtmlDownloader()
			cont = downloader.download(url)
			child_soup = BeautifulSoup(cont, "html5lib")
			# <em id="authorposton2753">发表于 2003-2-19 17:21:09</em><span title="2017-10-5 17:05:56">3&nbsp;小时前</span>
			time_node = child_soup.find('em', id=re.compile("authorposton")).find('span')
			if  time_node != None:
				time = time_node['title']
			else:
				time_node = child_soup.find('em', id=re.compile("authorposton"))
				time = time_node.get_text()
				time = time[time.find(' ')+1:]
			return time
		except:
			print("error")
			return None
