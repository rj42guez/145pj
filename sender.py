import binascii
import socket
import struct
import hashlib
#import scapy
import sys

def compute_checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

def encodeMessage(m):
    M = m.encode('utf-8')
    return M

iM = 'ID6d93e931'
iD = ''
portS = 6734
portR = 0
ipR = '10.0.7.141'
path = ''
transID = '0'

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

M = encodeMessage('ID6d93e931')
udpSocket.bind(('',portS))
print(M)

udpSocket.sendto(M, (ipR, portR))

data, addr = udpSocket.recvfrom(4096)

if len(data) > 0:
	print(addr)
	transID = data.decode()

print(transID)

f = open(path, 'r')
pyld = f.read()

seq = 0

for i in range(0, len(pyld), 20):

	if len(pyld) - i >= 20:
		pyld_sub = pyld[i:i+20]
		z = 0

	elif len(pyld) - i < 20:
		pyld_sub = pyld[i:]
		z = 1

	w = iD
	x = '{0:07d}'.format(seq)
	y = transID

	packet = 'ID{}SN{}TXN{}LAST{}{}'.format(w, x, y, z, pyld_sub)

	M = encodeMessage(packet)

	print(M)

	udpSocket.sendto(M, (ipR, portR))

	data, addr = udpSocket.recvfrom(4096)

	if len(data) > 0:
		print(addr)
		print(data.decode())
		cs = compute_checksum(data.decode())
		print(cs)

	seq += 1

