from bs4 import BeautifulSoup as bs
from requests import get
import argparse

parser = argparse.ArgumentParser(description='Rename all images and append a number to the end')
parser.add_argument('-p','--pages', type=int, help='the number of pages you wish to scrape')
args = parser.parse_args()

if __name__ == '__main__':

	def linklooper(link):
		review_page = 'https://pitchfork.com' + link
		return review_page

	def paeglooper(paegnum):
		page = 'https://pitchfork.com/reviews/albums/?page=' + str(paegnum)
		return page

	def argcheck(pg):
		if pg == None:
			return 1
		else:
			return pg

	review_dict = []
	score_list = []

	print("Gathering information...")
	for i in range(1, argcheck(args.pages) + 1):
		source = get(paeglooper(i)).content
		soup = bs(source, 'lxml-xml')

		reviews_html = soup.find_all("div", { "class" : "review" })

		for r in reviews_html:
			slug = r.a["href"]
			artist = r.ul.text
			title = r.h2.text

			a_review = {"slug": slug, "Artist" : artist, "Title" : title, "review" :''}
			review_dict.append(a_review)


		for i in review_dict:
			new_source = get(linklooper(i["slug"])).content
			review_soup = bs(new_source, 'lxml-xml')
			score_circle = review_soup.find_all("div", { "class" : "score-circle" })

			for x in score_circle:
				score = x.span.text
				
				i["review"] = score

		for i in review_dict:
			arteest = i["Artist"]
			album = i["Title"]
			revue = i["review"]

			print("Artist: {} |  Album: {} | Score: {}".format(arteest, album, revue))
