from bs4 import BeautifulSoup
from email_notification import email_notification
import datetime
import os
import requests
from settings import settings


# checking which books I allready have
try:
    with open("booklist.txt") as f:
        books = [book.strip("\n") for book in f.readlines()]
except FileNotFoundError:
    with open("booklist.txt", "w") as f:
        f.write()
    books = []

try:
    url = "https://www.packtpub.com/packt/offers/free-learning"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")

    # title
    title = soup.find("div", attrs={"class":"dotd-title"}).text.strip("\t\n")

    # Summary
    summary_div = soup.find("div", attrs={"class":"dotd-main-book-summary"})
    divs = summary_div.find_all("div")
    summary = []
    for i, div in enumerate(divs):
        if i < 2:
            pass
        elif i == 2:
            summary.append(divs[2].text.strip("\n\t"))
        else:
            if not 'class="dotd-main-book-form cf"' in str(div):
                summary.append(divs[i].text.strip("\n\t"))
    summary = "\n".join(summary)

    # image
    img = soup.find("img", attrs={"class" : "bookimage"})["src"].strip("/")

    # print([title])
    # print([summary])
    # print([img])
    # print([url])

except KeyError:
    # ToDo -- Specify possible errors
    email_notification(settings, "packtbub.com | An error occurs...", f"<b>Please visit {url} manually and fix me...</b>")
    exit()


if title in books:

    subject = f"packtpub.com | {title} | You allready have this book!"

    text = """<h2>{title}</h2>
    <p>Please visit {url}!</p>
    <img src={img}/>
    <p>{summary}</p>""".format(title=title, url=url, img=img, summary=summary.replace("\n", "</p><p>"))

    email_notification(settings, subject, text)

else:

    books.append(title)

    subject = f"packtpub.com | {title} | ✭ This book is new! ✭"

    text = """<div style="margin-bottom: 10px; padding: 10px; background: Yellow; color: Red;">
    <strong>I added this book to your booklist. Please download this book immediately.</strong>
    </div>

    <h2>{title}</h2>
    <p>Please visit {url}!</p>

    img src="{img}" title="" />
    
    <p>{summary}</p>""".format(title=title, url=url, img=img, summary=summary.replace("\n", "</p><p>"))

    email_notification(settings, subject, text)


# Updating booklist
books.sort(key=str.lower)
with open("booklist.txt", "w") as f:
    for book in books:
        f.write(book + "\n")
