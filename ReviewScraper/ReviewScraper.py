import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

class reviewScraper:
    def __init__(self):
        pass
    
    # Parse
    def urlParser(url):
        try:
            reqData = requests.get(url)
            return BeautifulSoup(reqData.content, 'html.parser')
        except:
            return 'Please provide valid product url from Flipkart.com'
    
    def prodInformation(soup):
        try:
            prodImage = str(soup.find('div', {'class': '_2E1FGS'})).split('\"')[5]
            prodName = soup.find_all('span', {'class':'B_NuCI'})[0].text
            prodRating = soup.find('div', {'class':'_3LWZlK'}).text
            prodPrice = soup.find_all('div', {'class':'_30jeq3 _16Jk6d'})[0].text
            highlights = soup.find('div', {'class' : '_2cM9lP'})
            prodHighlights = '|'.join([e.text for e in highlights.find_all('li')])
            prodBox = soup.find('td', {'class' : 'URwL2w col col-9-12'}).li.text

            mydict = {"Image": prodImage,
                  "Name": prodName,
                  "Rating": prodRating,
                  "Price": prodPrice,
                  "Highlights": prodHighlights,
                  "In Box" : prodBox}

            return pd.DataFrame(mydict, index = [1,])        
        except Exception as e:
            return e
    
    def pageLink(soup, pageNum):
        pageLink = []
        review = soup.find_all('div',{'class':'col JOpGWq'})
        try:
            for i in range(1,pageNum + 1):
                link = 'https://www.flipkart.com' + review[0].find_all('a')[-1]['href'] + '&page={}'.format(i)
                pageLink.append(link)
            return pageLink
        except Exception as e:
            return e
        
    def productReview(pageLink):
        col = ['ReviewPage','Rating', 'Headline','Review','ReviewDate']
        userReviews = pd.DataFrame(columns = col)
        i = 0
        reviewPage = 1
        try:
            for page in pageLink:
                Link = requests.get(page)
                Html = BeautifulSoup(Link.content, 'html.parser')   

                # Review Parsing from each page
                for rev in Html.find_all('div',{'class': 'col _2wzgFH K0kLPL'}):
                    try:            
                        rating = rev.find_all('div',{'class' : '_3LWZlK _1BLPMq'})[0].text
                        headLine = rev.find_all('p',{'class' : '_2-N8zT'})[0].text
                        comments = rev.find('div', {'class' : 't-ZTKy'}).div.div.text
                        date = rev.find_all('p',{'class' : '_2sc7ZR'})[1].text
                        userReviews.loc[i] = [reviewPage,rating,headLine,comments,date]
                        i+=1
                    except:
                        pass

                # Stop If don't have Next button
                lenHtml = len(Html.find_all('a' , {'class' : '_1LKTO3'}))    
                if lenHtml == 1:
                    next_ = Html.find_all('a' , {'class' : '_1LKTO3'})[0].text
                else:
                    next_ = Html.find_all('a' , {'class' : '_1LKTO3'})[1].text  

                if next_ == 'Next':
                    reviewPage +=1
                else:
                    break  

            return userReviews
        except Exception as e:
            return e