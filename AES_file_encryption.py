from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import os, random

# Input is read in chunks of 16KB
chunk_size = 16*1024

def encrypt(key, filename):

	# Input read from inp_file, encrypted and written into out_file
	inp_file = open(filename, 'rb')
	out_file = open("(encrypted)" + filename, 'wb')

	filesize = str(os.path.getsize(filename)).zfill(16)

	# Constructing a 16 byte Initializing Vector
	IV = ''
	for _ in range(16):
		IV = IV + chr(random.randint(0, 0xFF))

	encryptor = AES.new(key, AES.MODE_CBC, IV)
	out_file.write(filesize)
	out_file.write(IV)

	while(True):
		chunk = inp_file.read(chunk_size)

		if len(chunk) == 0:
			break
		elif len(chunk) % 16 != 0:
			padding = ' ' * (16 - (len(chunk) % 16))
			chunk = chunk + padding

		out_file.write(encryptor.encrypt(chunk))

	inp_file.close()
	out_file.close()

def decrypt(key, filename):

	inp_file = open(filename, 'rb')
	out_file = open("(decrypted)" + filename[11:], 'wb')

	filesize = long(inp_file.read(16))
	IV = inp_file.read(16)
	decryptor = AES.new(key, AES.MODE_CBC, IV)

	while(True):
		chunk = inp_file.read(chunk_size)

		if len(chunk) == 0:
			break
		out_file.write(decryptor.decrypt(chunk))

	out_file.truncate(filesize)

def get_key(password):
	hasher = SHA256.new(password)
	return hasher.digest()

def main():

	while(True):
		opt = raw_input("(E)ncrypt, (D)ecrypt or (X)exit: ")

		if(opt == 'E'):
			f = raw_input("File to encrypt: ")
			p = raw_input("password: ")

			encrypt(get_key(p), f)
			print "Done\n"
		elif(opt == 'D'):
			f = raw_input("File to decrypt: ")
			p = raw_input("password: ")

			decrypt(get_key(p), f)
			print "Done\n"
		elif(opt == 'X'):
			break
		else:
			print "Invalid option. Chose an appropriate option...\n"

if __name__ == '__main__':
	main()

