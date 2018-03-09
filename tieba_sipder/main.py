import html_downloader,html_parser,html_outputer

class SpiderMain(object):
	"""爬虫总调度程序"""
	def __init__(self):
		self.downloader = html_downloader.HtmlDownloader()
		self.parser = html_parser.HtmlParser()
		self.outputer = html_outputer.HtmlOutputer()

	def craw(self, root_url,page):
		url = root_url
		p = 0
		while p < page:
			if url is None:
				return 
			print("...waiting...")
			try:
				html_cont = self.downloader.download(url)
				next_url,new_data = self.parser.parse(html_cont)
				self.outputer.add_new_data(new_data)
				url = next_url
				p = p + 1
			except:
				print ("craw failed.Page %d") %page
				break
		# self.outputer.output_to_excel()
		self.outputer.output_to_mysql()


if __name__ == '__main__':
	url = "http://tieba.baidu.com/f?kw=python&ie=utf-8&pn=0"
	page = 30
	objs_pider = SpiderMain()
	objs_pider.craw(url,page)