import smtplib
import logging
from email.mime.text import MIMEText
from requests import get


ipfile = "PATH_xxx/FILE.xxx" # File and its full path, which you need to check and write your IP on.
ip_site = "https://api.ipify.org"
email_sender = "xxx@xxx.xxx"  # Whatever you want as long it is in the format user@domain.
email_receiver = "xxx@xxx.xxx"  # Must be a valid email address.
smtp_server = "xxx.xxx.xxx"  # The SMTP server you want to authenticate at. You must already have valid credentials.
smtp_port = "587"  # The port you want to use. Port 25 is insecure and deactivated on most severs anyway.
smtp_user = "xxx"  # Your username for the SMTP server.
smtp_password = "xxx"  # Your password for the SMTP server.


def get_ip(ip_api):
    ipnow = get(ip_api).text
    logging.debug(f"IP read from API {ipnow}")
    return ipnow

def notify(current_ip: str, smtp_settings: dict):   # Sends an email with the present IP as body of the message.
    msg = MIMEText(current_ip)
    msg['Subject'] = 'xxx' # Subject of the email you'll receive.
    msg['From'] = smtp_settings['sender']
    msg['To'] = smtp_settings['receiver']

    s = smtplib.SMTP(smtp_settings['server'], smtp_settings['port'])
    s.starttls()
    s.login(smtp_settings['user'], smtp_settings['password'])
    s.sendmail(smtp_settings['sender'],smtp_settings['receiver'], msg.as_string())
    s.quit()
    logging.debug("notify - Notification has been sent.")

def read_ip(f_name):
    iplog = open(f_name, 'r')
    ipsofar = iplog.read()
    iplog.close()
    logging.debug("IP read from file")
    return ipsofar

def store_ip(curr_ip):
    ipnew = open(ipfile, 'w+')
    ipnew.write(format(curr_ip))
    ipnew.close()
    logging.debug("store_ip - iplog has been overwritten.")


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s", level=logging.DEBUG)

# Compares last IP with the present one. If the IP changed, the ipfile is updated and notify() is invoked.
    smtp_sets = {
        'sender': email_sender,
        'receiver': email_receiver,
        'server': smtp_server,
        'port': smtp_port,
        'user': smtp_user,
        'password': smtp_password
        }
    ipsofar = None
    ipnow = None
    try:
        ipnow = get_ip(ip_site)
        logging.info(f"IP detected {ipnow}")
        ipsofar = read_ip(ipfile)
        logging.info(f"IP read from file {ipsofar}")
    except FileNotFoundError as pippo:
        logging.debug("Log file not found... creating new one.")
        store_ip('first run')
    except HTTPError as excpt:
        logging.error(f"Can't connect to {ip_site}")

    try:
        if ipnow is not None and ipnow != ipsofar:
            logging.info("IP change detected ")
            notify(ipnow, smtp_sets)
            store_ip(ipnow)
        else:
            logging.info("No IP changes detected")
    except smtplib.SMTPException as excpt:
        logging.error("ERROR: Email could not be sent! " + str(excpt))
    except OSError as excpt:
        logging.error("ERROR: File could not be overwritten! " + str(excpt))
    except Exception as excpt:
        logging.error(f"Unhandled exception {excpt}")
        sys.exit(-1)
        
        
