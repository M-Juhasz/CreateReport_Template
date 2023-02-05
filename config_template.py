# Fill in your configuration details and rename this file to config.py. createreport.py imports config.py.

# pdfkit needs the location of wkhtmltopdf
wkhtmltopdf_path = "C://your//path//to//wkhtmltopdf(.exe)"

# connection and login data for smtplib
port = 465  # SSL!
smtp_server = "your.smtp.server"
sender_email = "yourmail@smtp.server"
password = "yourPW"

# mail recipients - seperate with comma
to = "some1@somemail.com,some2@somemail.com,..."
cc = "some1@somemail.com,some2@somemail.com,..."
bcc = "some1@somemail.com,some2@somemail.com,..."

# mail body - if no html body needed, set to ""
body_plain = """Hi there,

This message is sent from Python.
For source, see https://github.com/M-Juhasz/PandasTraining.

Best regards,
my script"""
body_html = """<html>
  <body>
    <p>Hi there,<br>
       <b>Testing</b> my script.<br>
       <a href="https://github.com/M-Juhasz/PandasTraining">This</a> 
       is what sent this mail.<br><br>
       Best,<br>
       my script
    </p>
  </body>
</html>
"""