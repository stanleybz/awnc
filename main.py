import requests
import redis
from firebase import firebase
from bs4 import BeautifulSoup
from time import sleep


class Main:

    def __init__(self):
        # self.getArticleUrl()
        self.connectRedis()
        self.firebase = firebase.FirebaseApplication('https://firebaseio.com/', authentication=None)

    def getAllRow(self):
        for key in self.r.scan_iter("*"):
            # delete the key
            print(key)


    def getArticleUrl(self):
        cats = ['home', 'news', 'blog', 'animationworld', 'vfxworld']
        for i in range(len(cats)):
            theCat = cats[i]
            for x in range(0, 1):
                url = 'https://www.awn.com/'+theCat+'?page='+str(x)
                print('downloading: ' + url)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                articles = soup.find_all('article')
                for theArticle in articles:
                    readMore = theArticle.find('div', class_='read-more')
                    theLink = readMore.find('a', href=True)
                    if self.r.get(theLink['href']) is None:
                        # Save if not exists
                        self.r.set(theLink['href'], 0)

    def crawContent(self, url):
        # print(link)
        response = requests.get('https://awn.com')
        print(response)
        return
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
        abstract = article.find('div', {'class': 'field-name-field-abstract'})\
                        .find('div', {'class': 'field-items'})\
                        .find('div', {'class': 'field-item'})\
                        .find('p').getText().lstrip()
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
        # print(body)

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
        #
        # result = self.firebase.post('/' + url, {\
        #             'title':title,\
        #             'abstract':abstract,\
        #             'submitted':submitted,\
        #             'body':body,\
        #             'allTags':allTags,\
        #         })

main = Main()
# main.getArticleUrl()
# main.getAllRow()
main.crawContent('https://www.awn.com/news/neill-blomkamp-uses-unity-2017-unleash-short-adam-mirror')
