import argparse
import smtplib
from email.message import EmailMessage
import requests
import time
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}
TO_EMAIL = ""
EMAIL=""
PASSWORD=""
DELAY=10


def send(subject,message):
    # Replace the number with your own, or consider using an argument\dict for multiple people.

    auth = (EMAIL, PASSWORD)

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    # Send text message through SMS gateway of destination number
    print("Sending Message\nto: {}\nfrom: {}\nsubject: {}\nmessage: {}".format(TO_EMAIL, EMAIL, subject, message))
    result=server.send_message(msg, auth[0], TO_EMAIL)
    print("Message Sent\nReturned: {}".format(result))


def getInStockBB(gpu):
    link=gpu_list[gpu]
    page = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = soup.find(class_="heading-5 v-fw-regular").get_text()
    sold_out = soup.find(text="Sold Out")
    print("Checking: {}".format(name))
    if not sold_out:
        price=soup.find(class_="priceView-hero-price priceView-customer-price").find_all("span")[0].get_text()
        print("IN STOCK")
        send("IN STOCK {}".format(name),"Name: {}\nPrice: {}\nLink: {}".format(name,price,link))
    else:
        print("Sold Out")
gpu_list = {"fe":"https://www.bestbuy.com/site/nvidia-geforce-rtx-4090-24gb-gddr6x-graphics-card-titanium-and-black/6521430.p?skuId=6521430","msi_liquid":"https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-4090-suprim-liquid-x-24g-24gb-ddr6x-pci-express-4-0-graphics-card/6522334.p?skuId=6522334","msi_trio":"https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-4090-gaming-trio-24g-24gb-ddr6x-pci-express-4-0-graphics-card/6522371.p?skuId=6522371"}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--email', type=str,help='Email to send message from', required=True)
    parser.add_argument('--password', type=str,help='GMail passowrd (may need to setup app specific password)', required=True)
    parser.add_argument('--toEmail', type=str,help='Email to send message to')
    parser.add_argument('--delay', type=int,help='Delay for checking (in seconds)')


    args = parser.parse_args()

    if args.email:
        EMAIL=args.email
    if args.password:
        PASSWORD=args.password
    if args.toEmail:
        TO_EMAIL=args.toEmail
    if args.delay:
        DELAY = args.delay

    while True:
        for gpu in gpu_list:
            getInStockBB(gpu)
        print("Sleeping for {}s....".format(DELAY))
        time.sleep(DELAY)
