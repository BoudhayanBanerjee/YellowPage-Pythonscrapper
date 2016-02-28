import requests
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

#------------------ function to Send Email -----------------------#

def send_email(item,place,shop):

    # Here goes all the details about email #
    from_email = "boudhayanbanerjee@gmail.com"
    to_email = "bbanerji@iastate.edu"
    server = smtplib.SMTP('smtp.gmail.com',587)

    # Create message container - the correct MIME type is multipart/alternative.
    message = MIMEMultipart('alternative')
    message['from'] = from_email
    message['to'] = to_email
    message['subject'] = "Message from BYAN LLC support team"

    # Create the body of the message (a plain-text and an HTML version).
    message_text = "Hello!\nHow are you?\nHere is our suggestion for "+item+" in "+place+".\n\n Thanks,\nBYAN LLC Support Team"

    message_html = """\
    <html>
      <head></head>
      <body>
        <p>Hey!<br><br>
           How are you?<br>
           Here is our suggestion for """+item+""" in """+place+"""
        .<br><br>"""+shop+"""<br><br>
        Thanks,<br>BYAN LLC Support Team</p>
      </body>
    </html>
    """
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(message_text, 'plain')
    part2 = MIMEText(message_html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    message.attach(part1)
    message.attach(part2)


    try:
        server.starttls()
    except:
        print("Problem while starting mail server\n")

    try:
        server.login(from_email,"lqougbpjrqghrmeq")
    except:
        print("Problem while login\n")

    try:
        server.sendmail(from_email,to_email,message.as_string())
        print("Email sent successfully")
    except:
        print("Could not send email.Please try again\n")


#------------- script for webscrapper ---------#

def ypscrapper(search_item,search_location):

    search = "http://www.yellowpages.com/search?search_terms="+str(search_item)+'&geo_location_terms='+str(search_location)


    r = requests.get(search)
    soup = BeautifulSoup(r.content,"html.parser")

    data = soup.find_all("div",{"class": "info"})

    filename = str(search_location).upper()+"_"+str(search_item).upper()+".csv"
    file = open(filename,'w')
    file.write("Business Name" + "," + "Street" + "," + "Locality" + "," + "Region" + "," + "Postal Code" + "," + "Phone"+'\n')

    randNum = random.randrange(1,len(data))
    count = 0


    for item in data:

        try:
           businessName = (item.contents[0].find_all("a",{"class": "business-name"})[0].text)
        except:
            businessName = ""

        try:
            street = (item.contents[1].find_all("span",{"class": "street-address"})[0].text)

        except:
            street = ""
        try:
            locality = (item.contents[1].find_all("span",{"class": "locality"})[0].text.replace(",",""))

        except:
            locality = ""
        try:
            region = (item.contents[1].find_all("span",{"itemprop": "addressRegion"})[0].text)
        except:
            region =""
        try:
            zip = (item.contents[1].find_all("span",{"itemprop": "postalCode"})[0].text)
        except:
            zip = ""

        try:
            phone = (item.contents[1].find_all("div",{"itemprop": "telephone"})[0].text)
        except:
            phone = "Not Available"

        line = businessName + "," + street + "," + locality + "," + region + "," + zip + "," + phone+'\n'

        file.write(line)

        count +=1

        if (count == randNum):

            send_email(str(search_item).upper(),str(search_location).upper(),businessName.upper()+"," + locality + " phone : " + phone)

            '''
            print("+-----------------------------------------------------------+")
            print("Order from ",businessName.upper() + "," + locality + " phone : " + phone)
            print("+-----------------------------------------------------------+")
            '''

    file.close()

def main():
    print("Please enter what you like to order :")
    search_item = input()
    print("Please enter your location :")
    search_location = input()
    ypscrapper(search_item,search_location)

main()