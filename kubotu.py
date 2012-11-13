import sys 
import socket 
import string 
from pysqlite2 import dbapi2 as sqlite

HOST='irc.ubuntu.com' #The server we want to connect to 
PORT=8001 #The connection port which is usually 6667 
NICK='pybotu' #The bot's nickname 
IDENT='PhinnFortsBot'
REALNAME='PhinnFort' 
OWNER='PhinnFort' #The bot owner's nick 
CHANNEL='#kubuntu' #The default channel for the bot 
readbuffer='' #Here we store all the messages from server 

##initialize connection
print 'connecting...'
s=socket.socket( ) #Create the socket 
s.connect((HOST, PORT)) #Connect to server 
print 'opening db...'
dbcon = sqlite.connect("ubuntu.db")

def parsemsg(msg):
	global s
	if msg.find(CHANNEL):
		message = msg[1:].split(':',1)[1] #rip out the message
		if message[0]=='!': #treat all messages starting with '!' as search keyword 
			print 'replying...'
			query = message[1:]
			reply = searchDB(query)
			s.send('PRIVMSG ' + CHANNEL + ' :' + reply + '\n')

def searchDB(query):
	global dbcon
	global OWNER
	if (query.rstrip() == 'owner'):
		return 'The operator of this bot is Martin Sandsmark, aka PhinnFort. He can be reached at martin dot sandsmark at gmail.com.'
	cur = dbcon.cursor()
	cur.execute('SELECT value FROM facts WHERE name = ?', (query.rstrip(),))
	result = cur.fetchone()
	if (result == None):
		return 'Term not found.'
	else:
		return result[0][7:]


try:
	while 1:
		line=s.recv(500) #recieve server messages 
		print line #server message is output 
		if line.find('Found your hostname') != -1: 
			print 'sending authentication...'
			s.send('NICK '+NICK+'\n') #Send the nick to server 
			s.send('USER '+IDENT+' '+HOST+' tripleseven :'+REALNAME+'\n') #Identify to server 
		if line.find('End of /MOTD command') != -1: 
			print 'joining channel...'
			s.send('JOIN '+CHANNEL+'\n') #Join a channel
		if line.find('PRIVMSG') != -1: #Call a parsing function 
			print 'parsing message...'
			parsemsg(line)
		if(line[0]=='PING'): #If server pings then pong 
			print 'ponging...'
			s.send('PONG ' + line[1] + '\n')

except KeyboardInterrupt:
		print 'keyboard interrupted: dying silently...'
		s.send('QUIT')
		s.close()

def check_apache():
	try:

