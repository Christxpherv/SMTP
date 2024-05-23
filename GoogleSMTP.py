from socket import *
# establish a secure connection
import ssl
# for encoding email and password
import base64
# for sending email with attachments
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# start authentication
email = 'your email'
# for google you most likely need to generate an app password
password = 'dsto yzml sydt olug'
# recipient email
recipient = "recipient"

# Create a multipart message
msg = MIMEMultipart()
msg['From'] = 'email'
msg['To'] = 'recipient'
msg['Subject'] = 'subject'

# Attach the text part
text = MIMEText('\r\n I love computer networks!', 'plain')
msg.attach(text)

# Attach the image part
with open('cat.jpeg', 'rb') as img:
    image = MIMEImage(img.read())
    msg.attach(image)

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'
mailport = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, mailport))

recv = clientSocket.recv(1024).decode()
print(recv)

# if we did not receive a 220 reply from the server, print an error message
if recv[:3] != '220':
    print('220 reply not received from server.')
  
# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())

recv1 = clientSocket.recv(1024).decode()
print(recv1)

# if we did not receive a 250 reply from the server, print an error message
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send STARTTLS command and print server response
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
response = clientSocket.recv(1024).decode()
print(response)
if response[:3] != '220':
    print('220 reply not received from server.')

# Create a default context
context = ssl.create_default_context()

# Use the context to wrap the socket
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

# send login command
authCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
auth = clientSocket.recv(1024).decode()
print(auth)
if auth[:3] != '334':
    print('334 reply not received from server.')

# use base64 to encode email 
clientSocket.send(base64.b64encode(email.encode()) + '\r\n'.encode())
recvEmail = clientSocket.recv(1024).decode()
print(recvEmail)
if recvEmail[:3] != '334':
    print('334 reply not received from server.')

# use base64 to encode password
clientSocket.send(base64.b64encode(password.encode()) + '\r\n'.encode())
recvPassword = clientSocket.recv(1024).decode()
print(recvPassword)
if recvPassword[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFrom = f'MAIL FROM: <{email}>\r\n'
clientSocket.send(mailFrom.encode())

recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
RCPTto = f'RCPT TO: <{recipient}>\r\n'
clientSocket.send(RCPTto.encode())

recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
DATAcommand = 'DATA\r\n'
clientSocket.send(DATAcommand.encode())

recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')
    
# Send message data.
clientSocket.send(msg.as_string().encode())
clientSocket.send('\r\n.\r\n'.encode())

recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
QUITcommand = 'QUIT\r\n'
clientSocket.send(QUITcommand.encode())

recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '221':
    print('221 reply not received from server.')

clientSocket.close()