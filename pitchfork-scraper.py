from bs4 import BeautifulSoup as bs
from requests import get
import argparse

parser = argparse.ArgumentParser(description='Rename all images and append a number to the end')
parser.add_argument('-p','--pages', type=int, help='the number of pages you wish to scrape')
parser.add_argument('--csv', action='store_true', help='the number of pages you wish to scrape')
args = parser.parse_args()


if __name__ == '__main__':
	
	def linklooper(link):
		review_page = 'https://pitchfork.com' + link
		return review_page

	def paeglooper(paegnum):
		page = 'https://pitchfork.com/reviews/albums/?page=' + str(paegnum)
		return page

	def page_argcheck(pg):
		if pg == None:
			return 1
		else:
			return pg


	def csv_argcheck(csvarg):
		if csvarg == None:
			
			for i in review_dict:
				arteest = i["Artist"]
				album = i["Title"]
				revue = i["review"]

				result = "Artist: {} |  Album: {} | Score: {}".format(arteest, album, revue)
				print(result)
		else:		
			csvdir = "reviews.csv"
			csv = open(csvdir, "w")
			csv.write('artist, album, score\n')
			
			print('Creating the CSV')
			
			for i in review_dict:
				arteest = i["Artist"]
				album = i["Title"]
				revue = i["review"]
				row = "{},{},{}\n".format(arteest, album, revue)
				csv.write(row)

	review_dict = []
	score_list = []

	print("Gathering information...")
	for i in range(1, page_argcheck(args.pages) + 1):
		source = get(paeglooper(i)).content
		soup = bs(source, 'lxml-xml')

		reviews_html = soup.find_all("div", { "class" : "review" })

		for r in reviews_html:
			slug = r.a["href"]
			artist = r.ul.text
			title = r.h2.text

			a_review = {"slug": slug, "Artist" : artist, "Title" : title, "review" :''}
			review_dict.append(a_review)

		print("Gathering scores")
		for i in review_dict:
			new_source = get(linklooper(i["slug"])).content
			review_soup = bs(new_source, 'lxml-xml')
			score_circle = review_soup.find_all("div", { "class" : "score-circle" })

			for x in score_circle:
				
				score = x.span.text
				print("Score gathered")
				i["review"] = score
		print("")		

csv_argcheck(args.csv)

print("Scraping complete.")
