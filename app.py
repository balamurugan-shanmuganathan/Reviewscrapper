from flask import Flask, render_template, request, url_for, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods = ['GET','POST'])
def result():
    if request.method == 'POST':

        searchString = request.form['content'].replace(" ","")
        try:

            # Get Product URL
            flipkartUrl = 'https://www.flipkart.com/search?q=' + searchString
            reqData = requests.get(flipkartUrl)
            flipkartHtml = BeautifulSoup(reqData.content, 'html.parser')
            # flipkartLink = flipkartHtml.find_all('div', {'class': 'bhgxx2 col-12-12'})

            productLink = []
            baseLink = "https://www.flipkart.com"
            for i in flipkartHtml.findAll('a'):
                try:
                    if len(i.get('href')) > 100:
                        link = baseLink + i.get('href')
                    productLink.append(link)
                except:
                    'None'
            productLink = list(dict.fromkeys(productLink))  # Remove duplicate links

            
            results = []

            for link in productLink[0:10]:

                productPage = requests.get(link)
                product = BeautifulSoup(productPage.content, 'html.parser')

                # ProductImage
                try:
                    prodImage = str(product.find('div', {'class': '_2_AcLJ'})).split('(')[1].replace(')"></div>',
                                                                                                     '')
                except:
                    prodImage = ''

                # ProductName
                try:
                    name = product.find_all('span', {'class': '_35KyD6'})
                    prodName = name[0].text
                except:
                    prodName = ''

                # Ratings
                try:
                    rating = product.find('div', {'class': 'hGSR34'})
                    prodRatings = rating.get_text()
                except:
                    prodRatings = ''

                # Price
                try:
                    price = product.find('div', {'class': '_3auQ3N _1POkHg'})
                    prodPrice = price.get_text()
                except:
                    prodPrice = ''

                # Offer
                try:
                    offer = product.find_all('div', {'class': 'VGWI6T _1iCvwn'})
                    prodOffer = offer[0].text
                except:
                    prodOffer = ''

                # Offer Price
                try:
                    offerPrice = product.find('div', {'class': '_1vC4OE _3qQ9m1'})
                    prodOfferPrice = offerPrice.get_text()
                except:
                    prodOfferPrice = ''

                # Highlights
                try:
                    highlights = product.find('div', {'class': '_3WHvuP'})
                    prodHighlights = ' | '.join([e.text for e in highlights.find_all('li')])
                except:
                    prodHighlights = ''

                mydict = {"Product": searchString,
                          "Image": prodImage,
                          "Name": prodName,
                          "Rating": prodRatings,
                          "Price": prodPrice,
                          "Offer": prodOffer,
                          "OfferPrice": prodOfferPrice,
                          "Highlights": prodHighlights}
                results.append(mydict)                


            return render_template('result.html', results = results)
        except:
            return "Something Wrong"


if __name__ == '__main__':
    app.run(debug= True)