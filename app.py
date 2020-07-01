from flask import Flask, render_template, request
from ReviewScraper.ReviewScraper import reviewScraper
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    img1 = os.path.join('static','flipkartImg', 'Image1.jpg')
    return render_template('index.html',img1 = img1)

@app.route('/about')
def about():
    img2 = os.path.join('static','flipkartImg', 'Image2.jpg')
    return render_template('about.html', img2 = img2)

@app.route('/Reviews', methods = ['GET','POST'])
def reviews():
    if request.method == 'POST':
        try:
            url = request.form['url']
            pages = int(request.form['page'])        
            soup = reviewScraper.urlParser(url)
            prodInfo = reviewScraper.prodInformation(soup)
            pageLink = reviewScraper.pageLink(soup, pages)
            reviews = reviewScraper.productReview(pageLink)
            review_len  = '{} Reviews are scraped from {} pages'.format(reviews.shape[0],pages)
            return render_template('reviews.html', prodInfo = prodInfo ,reviews = reviews, prodImg = prodInfo['Image'].values, review_len = review_len)
        except:
            return 'Can not parse this link. Please try another link or refer About Page'
if __name__ == '__main__':
    app.run(debug = True)
