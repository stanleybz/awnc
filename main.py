import requests
import urllib2
from firebase import firebase
from bs4 import BeautifulSoup
from time import sleep

class Main:

    def __init__(self):
        self.firebase = firebase.FirebaseApplication('https://firebaseio.com/', authentication=None)

    def getArticleUrl(self):
        cats = ['home', 'news', 'blogs', 'animationworld', 'vfxworld']
        for i in range(len(cats)):
            theCat = cats[i]
            for x in range(0, 5):
                url = 'https://www.awn.com/'+theCat+'?page='+str(x)
                print('downloading: ' + url)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                articles = soup.find_all('article')
                for theArticle in articles:
                    try:
                        readMore = theArticle.find('div', class_='read-more')
                        thumb = theArticle.find('img')['src']
                        theLink = readMore.find('a', href=True)['href']
                        slug = theLink.split('/')[len(theLink.split('/'))-1]

                        filehandle = urllib2.urlopen(thumb)
                        with open('img/' + slug + '.jpeg','wb') as output:
                          output.write(filehandle.read())

                        self.crawContent(theLink, slug, thumb, theCat, cats[i])
                    except Exception as e:
                        print(e)

    def crawContent(self, url, slug, thumb, mainTag, showAt):
        # print(link)
        response = requests.get('https://www.awn.com' + str(url))
        soup = BeautifulSoup(response.text, 'lxml')

        #
        # Get title
        #
        author = soup.find('a', class_='username').getText().lstrip()
        # print(author)

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
        date = submitted.getText().lstrip().split('|')[1].lower().split('in')[0]
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

        result = self.firebase.post('/', {\
                    'url':url,\
                    'title':title,\
                    'abstract':abstract,\
                    'submitted':str(submitted),\
                    'body':str(body),\
                    'allTags':allTags,\
                    'thumb':thumb,\
                    'mainTag':mainTag,\
                    'author':author,\
                    'date':date,\
                    'slug':slug,\
                    'showAt':showAt\
                })
        print('done ' + str(url))

    def getFromFirebase(self):
        result = self.firebase.get('/', None)



main = Main()
main.getArticleUrl()
# main.getFromFirebase()
