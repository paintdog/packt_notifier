#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import logging
import os
import time

import requests

from email_notification import email_notification
from settings import settings

# LOGGING -------------------------------------------------------------------
filename = "logfile.log"
handler = logging.FileHandler(filename, "a")
frm = logging.Formatter("%(asctime)s [%(levelname)-8s] [%(funcName)-20s] [%(lineno)-4s] %(message)s", 
                          "%d.%m.%Y %H:%M:%S") 
handler.setFormatter(frm)
logger = logging.getLogger() 
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
# ---------------------------------------------------------------------------

URL            = "https://www.packtpub.com/packt/offers/free-learning"
URL_PRODUCT_ID = "https://services.packtpub.com/free-learning-v1/offers?dateFrom={}T00:00:00.000Z&dateTo={}T00:00:00.000Z"
URL_SUMMARY    = "https://static.packt-cdn.com/products/{}/summary"
URL_AUTHOR     = "https://static.packt-cdn.com/authors/{}"
URL_COVER      = "https://static.packt-cdn.com/products/{}/cover/smaller"

def get_product_id(URL_PRODUCT_ID):
    ''' get the product id for todays free ebook '''
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    web = requests.get(URL_PRODUCT_ID.format(today, tomorrow))
    data = web.json()
    product_id = data["data"][0]["productId"]
    return product_id

def get_summary_data(product_id, URL_SUMMARY):
    ''' get the summary data for a product id '''
    web = requests.get(URL_SUMMARY.format(product_id))
    summary_data = web.json()
    return summary_data

def get_cover_url(product_id, URL_COVER):
    ''' get the url to the cover of a product '''
    return URL_COVER.format(product_id)

def get_authors(author_ids, URL_AUTHOR):
    ''' get the information about the authors '''
    author_text = []    
    for author_id in author_ids:
        web = requests.get(URL_AUTHOR.format(author_id))
        author_text.append(web.json()["description"])    
    return "".join(author_text)

def update_books(books):
        books.sort(key=str.lower)
        with open("booklist.txt", "w") as f:
            for book in books:
                f.write(book + "\n")

def main():
    # checking which books I allready have
    try:
        with open("booklist.txt") as f:
            books = [book.strip("\n") for book in f.readlines()]
    except FileNotFoundError:
        with open("booklist.txt", "w") as f:
            f.write()
        books = []

    try:
        
        product_id = get_product_id(URL_PRODUCT_ID)
        summary_data = get_summary_data(product_id, URL_SUMMARY)
        title = summary_data["title"]
        image_url = get_cover_url(product_id, URL_COVER)
        summary_text = summary_data["about"]
        authors = get_authors(summary_data["authors"], URL_AUTHOR)     

        logging.info("## url:     {}".format(URL))
        logging.info("## ID:      {}".format(product_id))
        logging.info("## title:   {}".format(title))
        logging.info("## summary: {}...".format(summary_text[:40]))
        logging.info("## img_url: {}".format(image_url))                         

    except KeyError:
        email_notification(settings, "packtbub.com | An error occured...", f"<b>Please visit {url} manually and fix me...</b>")
        exit()

    if title in books:
        subject = f"packtpub.com | {title} | You allready have this book!"
        text = """<h2>{title}</h2>
        <p>Please visit {url}!</p>
        <img src='{img}' width='200px'></img>
        <p>Heute: [b]{title}[/b]<br><br>{url}</p>
        <p>{summary}</p>""".format(title=title, url=URL, img=image_url, summary=summary_text)
        email_notification(settings, subject, text)

    elif title == "" or title is None:
        # ToDo -- Specify possible errors
        email_notification(settings, "packtbub.com | An error occured...", f"<b>Please visit {url} manually and fix me...</b>")
        exit()
        
    else:
        books.append(title)
        subject = f"packtpub.com | {title} | ✭ This book is new! ✭"
        text = """<div style="margin-bottom: 10px; padding: 10px; background: Yellow; color: Red;">
        <strong>I added this book to your booklist. Please download this book immediately.</strong>
        </div>
        <h2>{title}</h2>
        <p>Please visit {url}!</p>
        <img src='{img}' width='200px'></img>
        <p>Heute: [b]{title}[/b]<br><br>{url}</p>
        <p>{summary}</p>""".format(title=title, url=URL, img=image_url, summary=summary_text)
        email_notification(settings, subject, text)

    # Updating booklist
    update_books(books)

    
if __name__ == "__main__":

    logging.info("job started.")
    done_flag = False
    error_counter = 0
    
    while True:
        try:
            main()
            done_flag = True
        except:
            logging.exception("Ein Fehler ist aufgetreten.")

            from skynet import Report
            report = Report()
            report.set_title("packt_notifier")
            report.set_summary('Please check the logs, an error occured.<br>Please visit <a href="https://www.packtpub.com/packt/offers/free-learning">https://www.packtpub.com/packt/offers/free-learning</a>.')
            report.save()
            break
                
        if done_flag:
            print("DONE")
            break

    logging.info("job closed.\n\n")
