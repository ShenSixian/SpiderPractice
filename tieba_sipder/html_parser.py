from bs4 import BeautifulSoup
import re
import html_downloader
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
		# <a href="//tieba.baidu.com/f?kw=python&amp;ie=utf-8&amp;pn=100" class="next pagination-item ">下一页&gt;</a>
		next_page_node = soup.find('a',class_="next pagination-item ")
		next_page_url = "http:" + next_page_node['href']
		return next_page_url

	def get_new_data(self,soup):
		"""获取所需要的信息"""
		res_data = []
		# <div class="t_con cleafix">
		# <div class="col2_right j_threadlist_li_right ">
		nodes = soup.find_all('div', class_="t_con cleafix")
		for node in nodes:
			data = {}

			# <span class="pull-right is_show_create_time" title="创建时间">9-12</span>
			create_time_node = node.find('span', class_ = "pull-right is_show_create_time")
			first_time = create_time_node.get_text()				   			# 创建时间
			data['first_time'] = first_time.strip()

			# <span class="threadlist_reply_date pull_right j_reply_data" title="最后回复时间"> 20:50 </span>
			last_time_node = node.find('span', class_ = "threadlist_reply_date pull_right j_reply_data")
			last_time = last_time_node.get_text()								# 最后回复时间
			data['last_time'] = last_time.strip()

			# <a href="/p/5318946119" title="...." target="_blank" class="j_th_tit ">
			title_node = node.find('a', class_="j_th_tit")
			data['title'] = title_node['title']									# 贴吧标题

			child_url = "http://tieba.baidu.com" + title_node['href']			# 对应的URL
			data['url'] = child_url 

			data['passage'] = self.get_child_data(child_url)					# 进入帖子并获取信息

			res_data.append(data)

		return res_data

	def get_child_data(self,url):
		"""获取子网页信息,即返回每一个帖子的一楼的内容"""
		try:
			downloader = html_downloader.HtmlDownloader()
			cont = downloader.download(url)
			child_soup = BeautifulSoup(cont, "html5lib")

		# <div id="post_content_112435851329" class="d_post_content j_d_post_content  clearfix">
			passage_node = child_soup.find('div',id = re.compile("post_content_"))		#获取第一条帖子内容
			passage = passage_node.get_text()
			return passage
		except:
			print ("child_page_craw failed")
			return None











