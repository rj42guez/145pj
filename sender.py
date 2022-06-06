import binascii
import socket
import struct
import hashlib
import sys
import time

def encodeMessage(m):
    M = m.encode()
    return M

iM = 'ID6d93e931'
iD = ''
portS = 6734
portR = 0
ipR = '10.0.7.141'
path = ''
transID = '0'


# Set up UDP connection 
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get arguments 
args = sys.argv

for i in range(len(args)):
        if args[i] == '-f':
                path = args[i+1]
        if args[i] == '-a':
                ipR = args[i+1]
        if args[i] == '-s':
                portR = int(args[i+1])
        if args[i] == '-c':
                portS = int(args[i+1])
        if args[i] == '-i':
                iD = args[i+1]

# Send intent message to receiver and listen from client port
M = encodeMessage('ID6d93e931')
udpSocket.bind(('',portS))
print(M)

udpSocket.sendto(M, (ipR, portR))

# Receive from server
data, addr = udpSocket.recvfrom(1024)

# Get transaction number
if len(data) > 0:
	print(addr)
	transID = data.decode()

print(transID)

# Get content/payload from file
f = open(path, 'r')
pyld = f.read()
pyld_sub = ''
seq = 0
z = 0

# Initialize values for finding processing time
first = 1
t1 = 0
t2 = 0
payloadSize = 1
i = 0

while i < len(pyld):

	# Size of remaining payload is still larger than max payload size; packet to send is not yet the last
	if len(pyld) - i >= int(payloadSize):
		pyld_sub = pyld[i:i+int(payloadSize)]
		if len(pyld) - i == int(payloadSize):
			z = 1
		else:
			z = 0

	# Packet to send is the last one
	elif len(pyld) - i < int(payloadSize):
		pyld_sub = pyld[i:]
		z = 1

	w = iD
	x = '{0:07d}'.format(seq)
	y = transID

	packet = 'ID{}SN{}TXN{}LAST{}{}'.format(w, x, y, z, pyld_sub)

	M = encodeMessage(packet)

	print(M)

	udpSocket.sendto(M, (ipR, portR))

	if first == 1:
		t1 = time.time()

	data, addr = udpSocket.recvfrom(1024)
	if first == 1:
		t2 = time.time()
		Tproc = t2 - t1
		print(Tproc)
		payloadSize = Tproc / 100 * (len(pyld)-1)

	print(i, int(payloadSize))
	if len(data) > 0:
		print(addr)
		print(data.decode())

	seq += 1

	if first == 0:
		i += int(payloadSize)
	else:
		i += 1
		first = 0

