import smtplib
from email.mime.text import MIMEText
from requests import get

ipnow = get("https://api.ipify.org").text
ipfile = "FULL PATH OF THE TEXT FILE" # You need such file to check and write your IP on.

def notify():   # Sends an email with the present IP as body of the message.
    server = "YOUR CHOSEN SMTP SERVER"  # The SMTP server you want to authenticate at. You must already have valid credentials.
    port = "587"  # The port you want to use. Port 25 is insecure and deactivated on most severs anyway.
    user = "YOUR USERNAME"  # Your username for the SMTP server.
    password = "YOUR PASSWORD"  # Your password for the SMTP server.
    msg = MIMEText(ipnow)
    sender = 'SENDER@EMAIL.COM'  # Whatever you want as long it is in the format user@domain.
    receiver = 'RECEIVER@EMAIL.COM'  # Must be a valid email address.
    msg['Subject'] = 'YOUR SUBJECT'
    msg['From'] = sender
    msg['To'] = receiver

    s = smtplib.SMTP(server, port)
    s.starttls()
    s.login(user, password)
    s.sendmail(sender, [receiver], msg.as_string())
    s.quit()

def checkip():  # Compares last IP with the present one. If the IP changed, the ipfile is updated and notify() is invoked.    
    iplog = open(ipfile, 'r')
    ipsofar = iplog.read()
    iplog.close()
    if ipnow != ipsofar:
        ipnew = open(ipfile, 'w')
        ipnew.write(format(ipnow))
        ipnew.close()
        notify()
    else:
        print("No change detected.")

checkip()
