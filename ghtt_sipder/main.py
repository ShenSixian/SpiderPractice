import html_downloader,html_parser,html_outputer

class SpiderMain(object):
	"""爬虫总调度程序"""
	def __init__(self):
		self.downloader = html_downloader.HtmlDownloader()
		self.parser = html_parser.HtmlParser()
		self.outputer = html_outputer.HtmlOutputer()

	def craw(self, root_url,page):
		p = 1
		while p <= page:
			url = root_url + "-%d.html" %p
			if url is None:
				return 
			try:
				html_cont = self.downloader.download(url)
				next_url,new_data = self.parser.parse(html_cont)
				self.outputer.add_new_data(new_data)	
			except:
				p = p + 1
				print("craw failed")
		self.outputer.output_to_excel()
		self.outputer.output_to_mysql()


if __name__ == '__main__':
	url = "http://bbs.ghtt.net/forum-93"
	page = 5
	objs_pider = SpiderMain()
	objs_pider.craw(url,page)