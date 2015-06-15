#!/usr/bin/env python

#sends an email whenever there is a new psych study with times available

import urllib2
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#checks if the internet is available and active
def internet_connected():
    try:
        response=urllib2.urlopen('http://www.google.com',timeout=1) #an IP-addresse for google.com
        return True
    except urllib2.URLError as err: pass
    return False


# send mail from gmail address
def send_email(message):
    #sender = '[theSender]@gmail.com'
    #receivers  = '[theReceiver(s)]@gmail.com'

    # content of the message
    msg = MIMEMultipart()
    msg['Subject'] = 'New studies available!'
    msg['From'] = sender
    msg['To'] = receivers 
    content = MIMEText(message, 'plain')
    msg.attach(content)
    composed = msg.as_string()
      
    # set necessary credentials  
    username = sender  
    #password = '[yourPassword]'
      
    # send mail
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    server.sendmail(sender, receivers, composed)  
    server.quit()


def get_prev_studies():
    in_file = open("current_open_psych_studies.txt", 'r')
    lines = in_file.readlines()
    studies = {}
    for line in lines:
        study = line.split(',')[0]
        lab = line.split(',')[1].replace("\n", '')

        studies[study] = lab

    in_file.close()
    return studies


def check_reservax_site(lab):
    site_url = "http://www.reservax.com/" + lab
    page = urllib2.urlopen(site_url)
    soup = BeautifulSoup(page)

    font_tags = soup.find_all("b")
    for font_tag in font_tags:
        text = font_tag.get_text()
        #print text
        if "Open Slots!" in text:
            study_tag = font_tag.previous_sibling.previous_sibling
            study_name = study_tag.text
            study_href = study_tag.get('href')
            study_url = site_url + "/" + study_href

            if "Eye Tracking and Social Ju" in study_name: #they cancelled on me
                send_email(study_name + ": " + study_url)

            if study_name not in studies.keys():
                print "email sent!"
                send_email(study_name + ": " + study_url)

            studies[study_name] = lab


if internet_connected():
    studies = get_prev_studies()

    out_file = open("current_open_psych_studies.txt", 'w')
    for study_name, lab in sorted(studies.items(), key=lambda x: (x[1],x[0])): #will end up with duplicates, but may cut down on inadvertently wiping the file
        out_file.write(study_name + ',' + lab + '\n')

    check_reservax_site("ubcviscog")
    check_reservax_site("barlab")
    check_reservax_site("hciatubc")

    for study_name, lab in sorted(studies.items(), key=lambda x: (x[1],x[0])): #write out the studies in sorted order (by lab then study name)
        out_file.write(study_name + ',' + lab + '\n')



