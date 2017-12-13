import requests
from firebase import firebase
from bs4 import BeautifulSoup
from time import sleep
import html2text
import simplejson

class Main:

    def __init__(self):
        self.firebase = firebase.FirebaseApplication('https://firebaseio.com/', authentication=None)

    # def getAllRow(self):
    #     for key in self.r.scan_iter("*"):
    #         # delete the key
    #         print(key)


    def getArticleUrl(self):
        cats = ['animationworld', 'vfxworld']
        for i in range(len(cats)):
            theCat = cats[i]
            for x in range(0, 5):
                url = 'https://www.awn.com/'+theCat+'?page='+str(x)
                print('downloading: ' + url)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                articles = soup.find_all('article')
                for theArticle in articles:
                    readMore = theArticle.find('div', class_='read-more')
                    theLink = readMore.find('a', href=True)
                    self.crawContent(theLink['href'])
                    
    def crawContent(self, url):
        # print(link)
        response = requests.get('https://www.awn.com' + str(url))
        soup = BeautifulSoup(response.text, 'lxml')

        #
        # Get title
        #
        title = soup.find('h1', {'id': 'page-title'}).getText().lstrip()
        # print(title)

        article = soup.find('article')

        #
        # Get abstract
        #
        try:
            abstract = article.find('div', {'class': 'field-name-field-abstract'})\
                            .find('div', {'class': 'field-items'})\
                            .find('div', {'class': 'field-item'})\
                            .find('p').getText().lstrip()
        except:
            abstract = ''
            print 'Oops! abstract error'
            pass
        # print(abstract)

        #
        # Get submitted
        #
        submitted = article.find('footer', {'class': 'submitted'})
        # print(submitted)

        #
        # Get body
        #
        body = article.find('div', {'class': 'content'})\
                        .find('div', {'class': 'field-name-body'})
        # print(body.getText())

        #
        # Get tags
        #
        tags = article.find('div', {'class': 'content'})\
                        .find('div', {'class': 'field-name-field-tags'})\
                        .find('div', {'class': 'field-items'})\
                        .find_all('div', {'class': 'field-item'})
                        # .find('a')
        allTags = []
        for tag in tags:
            theTag = tag.find('a').getText().lstrip()
            allTags.append(theTag)
        # print(allTags)
        
        # print(simplejson.encoder.JSONEncoderForHTML().encode(str(submitted)))
        result = self.firebase.post('/', {\
                    'url':url,\
                    'title':title,\
                    'abstract':abstract,\
                    'submitted':str(submitted),\
                    'body':str(body),\
                    'allTags':allTags,\
                })
        print('done ' + str(url)) 

main = Main()
main.getArticleUrl()
# main.getAllRow()
