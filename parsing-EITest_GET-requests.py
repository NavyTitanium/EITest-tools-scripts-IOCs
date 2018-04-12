import binascii
import hashlib
import sys
import os
import urllib
import threading
import Queue
import base64
import woothee
from tld import get_tld
import pygeoip
import pyodbc
import hashlib

QUEUE_SIZE = 50000
sentinel = object()
sentinel2 = object()
countrydb = pygeoip.GeoIP('C:\\GeoIP.dat')
citydb = pygeoip.GeoIP('C:\\GeoLiteCity.dat')
asndb = pygeoip.GeoIP('C:\\GeoIPASNum.dat')
cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 ANSI Driver};SERVER=127.0.0.1;DATABASE=eitest;USER=eitest;PASSWORD=some_pass')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setencoding(str, encoding='utf-8')

class victims:
	HTTP_USER_AGENT= ""
	HTTP_REFERER= ""
	REMOTE_ADDR= ""
	HTTP_HOST= ""
	PHP_SELF= ""	
	victime_country= ""
	victime_city= ""
	asn_victime= ""
	ua_category= ""
	ua_name= ""
	ua_os= ""
	website_tld= ""
	opcode=""
	line=""
	
def xor_str(str1, str2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(str1, str2))

def decrypt(data, op):
    try:
        g = ''

        while len(g) < len(data):
            op = binascii.unhexlify(hashlib.md5(g + str(op) + 'q1w2e3r4').hexdigest())
            g += op[0: 8]

        return xor_str(data, g)
    except TypeError:
        return ''

def safe_base64_decode(data):
    missing_padding = len(data) % 4

    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)

    return data.decode('base64')
			
def decode(inqueue):
	try:
		parse=inqueue.split(":::::")
		line=parse[1]
		inqeue=parse[0]		
		data = inqueue.split("?")
		content=data[1]
		encode=data[0].split("/")
		encode=encode[1]
	except:
		print("Decoding failed")
		return
		
	response_data = urllib.unquote(urllib.unquote(content))
	operation_code = encode
	params = response_data.split('.')
	victim=victims()
	decoded=[]
	
	for i, param in enumerate(params):
		try:
			plain_param = safe_base64_decode(param)
		except:
			print("Decoding failed because b64")
			return
			
		decrypted_param = decrypt(plain_param, operation_code)

		if decrypted_param != '':
			decoded.append(decrypted_param)
		else:
			decoded.append("NULL")

	try:
		victim.HTTP_USER_AGENT=decoded[0].rstrip()
	except IndexError:
		victim.HTTP_USER_AGENT=""
		pass
	
	try:	
		victim.HTTP_REFERER=decoded[1].rstrip()
	except IndexError:
		victim.HTTP_REFERER=""
		pass
	
	try:
		victim.REMOTE_ADDR=decoded[2].rstrip()
	except IndexError:
		victim.REMOTE_ADDR=""
		pass
	
	try:
		victim.HTTP_HOST=decoded[3].rstrip()
	except IndexError:
		victim.HTTP_HOST=""
		pass
	
	try:
		victim.PHP_SELF=decoded[4].rstrip()
	except IndexError:
		victim.PHP_SELF=""
		pass
		
	victim.opcode = operation_code
	victim.line = line
	return victim						

def read_file(name, queue):
    with open(name) as f:
        count=0
        for line in f:			
			if "GET /in.php?i=" not in line:
				queue.put(line+":::::"+str(count))
			count += 1
        	
			if (count % 100000) == 0:
				print("*****IN Queue******")
				print(str(count))
				print(queue.qsize())	
				
    queue.put(sentinel)

def process(inqueue, outqueue):
    for line in iter(inqueue.get, sentinel):
        outqueue.put(decode(line))
    outqueue.put(sentinel)
	
def output(queue,keu2):
	for line in iter(queue.get, sentinel):			
		if line:
			if(line.HTTP_USER_AGENT and len(line.HTTP_USER_AGENT)>5 and "decode" not in line.HTTP_USER_AGENT):
				try:
					user_agent = woothee.parse(line.HTTP_USER_AGENT)
					line.ua_os=user_agent['os']
					line.ua_name=user_agent['name']
					line.ua_category=user_agent['category']
				except:
					line.ua_os=""
					line.ua_name=""
					line.ua_category=""
			else:
				line.ua_os=""
				line.ua_name=""
				line.ua_category=""
				
			if(len(line.REMOTE_ADDR)<16 and len(line.REMOTE_ADDR)>3):
				try:
					line.victime_country=countrydb.country_name_by_addr(line.REMOTE_ADDR)
				except:
					line.victime_country="unknown"
					
				if not line.victime_country:
					line.victime_country="unknown"
				
				try:
					city=citydb.record_by_addr(line.REMOTE_ADDR)
					
				except:					
					line.victime_city="unknown"
				try:
					line.asn_victime=asndb.org_by_name(line.REMOTE_ADDR)
				except:
					line.asn_victime="unknown"
					
				if not line.asn_victime:
					line.asn_victime="unknown"
			else:
				line.victime_country="unknown"
				line.asn_victime="unknown"
				
			if city and "unknown" not in city:
				line.victime_city=city['city']
				if not line.victime_city:
					line.victime_city="unknown"
			else:
				line.victime_city="unknown"
			
			try:
				line.website_tld = get_tld(line.HTTP_HOST, fix_protocol=True, as_object=True).suffix
			except:
				line.website_tld = line.HTTP_HOST
				
			
			keu2.put(line)
			
	keu2.put(sentinel2)		

def process2(inqueue, outqueue):
    for line in iter(inqueue.get, sentinel2):
		database(line)

def database(out):	
	if out:
	
		if(int(out.line) % 10000 == 0):
				print("*****OUT Queue******")
				print(out.line)
				
		try:			
			cursor = cnxn.cursor()
			m = hashlib.md5()
			
			cursor.execute("SELECT ID FROM websites where URL ='" + out.HTTP_HOST + "'")
			id_website=""
			row_count = cursor.rowcount
			if row_count == 0:
				sqlwebsite= "INSERT IGNORE INTO websites (URL,tld) VALUES ('" + out.HTTP_HOST + "','" + out.website_tld + "')"
				cursor.execute(sqlwebsite)			
				cnxn.commit()
				cursor.execute("SELECT ID FROM websites where URL ='" + out.HTTP_HOST + "'")
				for row2 in cursor.fetchall():
					id_website= row2
				id_website=id_website[0]
			else:		
				for row2 in cursor.fetchall():
					id_website= row2
				id_website=id_website[0]
				
			cursor.execute('SELECT ID FROM ua where `user-agent` ="' + out.HTTP_USER_AGENT +'"')
			row_count = cursor.rowcount
			id_ua=""
			if row_count == 0:
				sqlua='INSERT IGNORE INTO `ua` (`user-agent`,`category`,`name`,`os`) VALUES ("' + out.HTTP_USER_AGENT + '","' + out.ua_category + '", "' + out.ua_name + '", "' + out.ua_os + '")'
				cursor.execute(sqlua)
				cnxn.commit()
				cursor.execute('SELECT ID FROM ua where `user-agent` ="' + out.HTTP_USER_AGENT +'"')
				for row1 in cursor.fetchall():
					id_ua= row1
				id_ua=id_ua[0]
			else:
				for row1 in cursor.fetchall():
					id_ua= row1
				id_ua=id_ua[0]
			
			m.update(out.opcode + out.REMOTE_ADDR+ out.HTTP_REFERER + str(id_ua) + str(id_website) + str(out.line))
			hash=m.hexdigest()
			
			cursor.execute("SELECT COUNT(*) FROM victim WHERE md5 = '" + hash + "'")
			row_count = cursor.rowcount
			if row_count == 0:
				sqlvictim='INSERT INTO `victim` (`md5`, `ip`,`country`,`city`,`asn`,`ua`,`website`) VALUES ("' + hash + '","' + out.REMOTE_ADDR + '", "'  + out.victime_country + '","' + out.victime_city + '","' + out.asn_victime + '","' + str(id_ua) + '", "' + str(id_website) + '")'			
				cursor.execute(sqlvictim)			
				cnxn.commit()
				
			cursor.close()		
			
		except Exception as ex:
			template = "exception {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			if "IntegrityError" not in message:
				print message
										
	return out.line
	
inq = Queue.Queue(maxsize=QUEUE_SIZE)
outq = Queue.Queue(maxsize=QUEUE_SIZE)
keu2 = Queue.Queue(maxsize=QUEUE_SIZE)	
keu3 = Queue.Queue(maxsize=QUEUE_SIZE)

threading.Thread(target=read_file, args=("E:\\EITest-sinkhole_data\\out3.txt", inq)).start()
threading.Thread(target=process, args=(inq, outq)).start()
threading.Thread(target=process, args=(inq, outq)).start()
threading.Thread(target=output, args=(outq,keu2)).start()
threading.Thread(target=output, args=(outq,keu2)).start()

for x in range(20):
	threading.Thread(target=process2, args=(keu2, keu3)).start()
