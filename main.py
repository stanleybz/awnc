import requests
import redis
from bs4 import BeautifulSoup

class Main:

    redisHost = 
    redisPort = 
    redisPassword = 

    def __init__(self):
        # self.getArticleUrl()
        self.connectRedis()

    def connectRedis(self):
        self.r = redis.StrictRedis(\
            host = self.redisHost,\
            port = self.redisPort,\
            db = 0,\
            password = self.redisPassword\
        )

    def getAllRow(self):
        for key in self.r.scan_iter("*"):
            # delete the key
            print(key)


    def getArticleUrl(self):
        cats = ['home', 'news', 'blog', 'animationworld', 'vfxworld']
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
                    self.r.set(theLink['href'], 0)


main = Main()
# main.getArticleUrl()
main.getAllRow()
