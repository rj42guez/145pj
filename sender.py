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

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)




args = sys.argv

for i in range(len(args)):
        if args[i] == '-f':
                path = ''
        if args[i] == '-a':
                ipR = args[i+1]
                print(ipR, '\n')
        if args[i] == '-s':
                portR = int(args[i+1])
                print(portR, '\n')
        if args[i] == '-c':
                portS = int(args[i+1])
                print(portS, '\n')
        if args[i] == '-i':
                iD = args[i+1]
                print(iD, '\n')

M = encodeMessage('ID'+iD)
print(M)
udpSocket.sendto(M, (ipR, portR))

#udpSocket.bind(('', portR))


udpSocket2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udpSocket2.bind(('',portS))
#tcpSocket.listen(5)



while True:

	data = udpSocket2.recvfrom(1024)

	if len(data) > 0:

		print(data.decode())

		break