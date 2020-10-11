from bs4 import BeautifulSoup
import requests
import json
import time

#Set up URL construction
base_url = 'https://www.snopes.com'
archive_extension = '/fact-check/rating/{}'
page_extension = '/page/{}/'

#list of pre-archived ratings
#ratings = ['scam', 'true', 'mostly-true', 'mixture', 'mostly-false', 'false', 'outdated', 'miscaptioned', 'correct-attribution', 'misattributed', 'legend']
ratings = [ 'mixture', 'mostly-false', 'false', 'outdated', 'miscaptioned', 'correct-attribution', 'misattributed', 'legend']

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
        soup = BeautifulSoup(url_content.content.decode('utf-8', 'ignore'), 'html.parser')
        #check status code
        if url_content.status_code != 200:
            print('Error on {}, status code of {}'.format(url, url_content.status_code))
            page_valid = False
            break

        #Check if we can validly scrape page
        if page_valid:
            #extract list of articles on page
            print('_____' + url + '_____')
            article_list = soup.findAll('main', {'class':'base-main'})[0].findAll('article')

            for article in article_list:
                time.sleep(.5)
                output_dictionary = {}

                article_url = article.findAll('a', href = True)[0]['href']
                output_dictionary['url'] = str(article_url)

                article_rating = rating
                output_dictionary['evaluation'] = str(rating)

                title = article.findAll('h5', {'class':'title'})[0].contents[0]
                output_dictionary['title'] = str(title)

                try:
                    subtitle = article.findAll('p',{'class':'subtitle'})[0].contents[0]
                    output_dictionary['subtitle'] = str(subtitle)
                except:
                    output_dictionary['subtitle']=""


                current_article_contents = BeautifulSoup(requests.get(article_url).content.decode('utf-8', 'ignore'), 'html.parser')
                print(article_url)

                try:
                    author = current_article_contents.findAll('a', {'class':'author'})[0].contents[0]
                    output_dictionary['author'] = str(author)
                except:
                    output_dictionary['author']=''

                try:
                    claim = current_article_contents.findAll('div', {'class':'claim'})[0].findAll('p')[0].contents[0]
                    output_dictionary['statement'] = str(claim)
                except:
                    output_dictionary['statement'] = ''

                try:
                    post_author = ''
                    output_dictionary['post_author'] = post_author
                except:
                    output_dictionary['post_author'] = ''

                try:
                    date_posted = current_article_contents.findAll('span',{'class':'date date-published'})[0].contents[0]
                    output_dictionary['date_posted'] = str(date_posted)
                except:
                    output_dictionary['date_posted'] = ''
                output_list.append(output_dictionary)

        page = page + 1
    output_string = json.dumps(output_list, ensure_ascii = True, indent = 4)

    replacement_dictionary = {
        '\\u2018':"'",
        '\\u2019':"'",
        '\\u2014':'-'
    }


    for uni in replacement_dictionary:
        output_string = output_string.replace(uni, replacement_dictionary[uni])
    #write out json string
    with open('{}-stories.json'.format(rating),'w') as fp:
        fp.write(output_string)
