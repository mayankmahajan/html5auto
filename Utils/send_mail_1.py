# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Added
from email.mime.image import MIMEImage


# Define these once; use them twice!
def sendResults(filePath):
    strFrom = 'mayank.mahajan@guavus.com'
    strTo = 'mayank.mahajan@guavus.com,Saikat.Prabhakar@guavus.com'
    smtp_server = "smtp-relay.guavus.com"

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Test Results'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText('<b>Find <i>Results</i></b>:<br><img src="cid:image1"><br><br>ui-automation', 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('result_graph.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # Send the email (this example assumes SMTP authentication is required)

    import smtplib
    server = smtplib.SMTP(smtp_server,port=25)
    # server.starttls()
    server.sendmail(strFrom, strTo, msgRoot.as_string())
    server.quit()


# from pyvirtualdisplay import Display
from selenium import webdriver

# display = Display(size=(800, 600))
# display.start()

driver = webdriver.Firefox()
driver.get("http://localhost:3333/index2.html")
import time
time.sleep(4)
filenamePath = "result_graph.png"
driver.save_screenshot(filenamePath)
sendResults(filenamePath)
driver.quit()
# display.stop()