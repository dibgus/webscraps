import pdfcrowd
#Initially, I wanted to save things as a pdf, but decided that using something
#with an api that cost money was kind of worthless
url = "https://www.webassign.net/login.html"
try:
    client = pdfcrowd.Client("_ignoreme", "cec86c8baaf06622b256adea0b73f635") #todo create api key
    newpdf = client.convertURI('http://www.google.com')

except pdfcrowd.Error, err:
    print("Failed to fetch PDF: {}".format(err))