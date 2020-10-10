from bs4 import BeautifulSoup
import requests
import json

#Set up URL construction
base_url = 'https://www.snopes.com'
archive_extension = '/fact-check/rating/{}'
page_extension = '/page/{}/'

#list of pre-archived ratings
ratings = ['true', 'mostly-true', 'mixture', 'mostly-false', 'false', 'outdated', 'miscaptioned', 'correct-attribution', 'misattributed', 'scam', 'legend']


#iterate through each rating
for rating in ratings:
    print('Starting {} label...'.format(rating))

    #reset control flow every iteration
    page = 1
    page_valid = True
    output_list = []


    #ensure current page is valid
    while page_valid:
        #construct URL
        url = base_url + archive_extension.format(rating) + page_extension.format(str(page))
        #Grab URL contents
        url_content = requests.get(url)
        soup = BeautifulSoup(url_content.content, 'html.parser')
        #check status code
        if url_content.status_code != 200:
            print('Error on {}, status code of {}'.format(url, url_content.status_code))
            page_valid = False
            break

        #Check if we can validly scrape page
        if page_valid:
            #extract list of articles on page
            print(url)
            article_list = soup.findAll('div', {'class':'theme-content'})[0].findAll('article', {'class':'media-wrapper'})

            for article in article_list:
                output_dictionary = {}

                article_url = article.findAll('a', href = True)[0]['href']
                output_dictionary['url'] = str(article_url)

                article_rating = rating
                output_dictionary['rating'] = str(rating)

                title = article.findAll('h5', {'class':'title'})[0].contents
                output_dictionary['title'] = str(title)

                try:
                    subtitle = article.findAll('p',{'class':'subtitle'})[0].contents
                    output_dictionary['subtitle'] = str(subtitle)
                except:
                    output_dictionary['subtitle']=""
                output_list.append(output_dictionary)

        page = page + 1
    output_string = json.dumps(output_list)

    #write out json string
    with open('{}-stories.json'.format(rating),'w') as fp:
        fp.write(output_string)
