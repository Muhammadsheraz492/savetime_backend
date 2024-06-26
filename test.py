import smtplib

sender_email = "qasim5ali99@gmail.com"
rec_email = "qasim5ali99@gmail.com"
password = "flxl nhkp mndw eafr"
message = "Hey, this was sent using python"

# Set up the SMTP server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()  # Start TLS encryption
server.login(sender_email, password)  # Login to the email server
print("Login Success")

# Send the email
server.sendmail(sender_email, rec_email, message)
print("Email has been sent to", rec_email)

# Close the connection to the SMTP server
server.quit()
