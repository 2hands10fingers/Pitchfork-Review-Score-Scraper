from bs4 import BeautifulSoup as bs
from requests import get
from re import findall
from json import load, loads, dump

source = get('http://pitchfork.com/reviews/albums/').content
soup = bs(source, 'lxml-xml')

'''optional way to grab information 
if you want to sort through things'''

# js_source = soup.find_all("script")[8].text
# parsed_js = findall('^\{\".*\}', js_source[11:])

# with open('object.json', 'w') as file:
# 	parser = loads(parsed_js[0])
# 	dump(parser, file, indent=2, sort_keys=True)

# with open('object.json', 'r+') as jsonfile:
# 	data = load(jsonfile)

review_dict = []
score_list = []

print("Gathering information...")
reviews_html = soup.find_all("div", { "class" : "review" })

for r in reviews_html:
	slug = r.a["href"]
	artist = r.ul.text
	title = r.h2.text

	a_review = {"slug": slug, "Artist" : artist, "Title" : title, "review" :''}
	review_dict.append(a_review)


def linklooper(link):
	review_page = 'https://pitchfork.com' + link
	# print(review_page)
	return review_page

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
