#!/usr/bin/python

import sys;
import re;
import RPi.GPIO as GPIO;
import serial;
import time;
import func;

mydevice = '/dev/serial0';
#mydevice = '/dev/ttyUSB0';
mybaud = 9600;
mytimeout = 0.25;

#ser = serial.Serial('/dev/cu.SLAB_USBtoUART',115200);
#ser = serial.Serial('/dev/ttyS0',115200);
#ser = serial.Serial('/dev/serial0',9600,timeout=0.25);
#ser = serial.Serial('/dev/ttyUSB0',9600,timeout=0.25);

ser = serial.Serial(mydevice, mybaud, timeout=mytimeout);
ser.flushInput();

power_key = 4;

def clear_serial():
	global ser, mydevice, mybaud, mytimeout;
	try:
		func.log('sim.py', 'clear_serial', 'attempting to reset serial with device: ' + mydevice + ' baud: ' + str(mybaud) + ' timeout: ' + str(mytimeout));
		ser = serial.Serial(mydevice, mybaud, timeout=mytimeout);
		ser.flushInput();
	except:
		func.log('sim.py', 'clear_serial', 'error: ' + str(sys.exc_info()));

def check_for_msg():
	global ser;
	resp = "";
	try:
		rec_buff = '';
		time.sleep(0.25);
		if ser.inWaiting():
			time.sleep(0.25);
			rec_buff = ser.read(ser.inWaiting());

		resp = str(rec_buff.decode().replace('\n', '|').replace('\r', '').encode('utf-8'));
		if len(resp) > 0:
			func.log('sim.py', 'check_for_msg', 'resp: ' + resp);
	except:
		resp = "*ERROR*";
		func.log('sim.py', 'check_for_msg', 'error: ' + str(sys.exc_info()));
		clear_serial();
	return resp;

def send_at(command,back,timeout):
	global ser;
	rec_buff = '';
	ser.write((command+'\r\n').encode());
	time.sleep(timeout);
	if ser.inWaiting():
		time.sleep(0.25);
		rec_buff = ser.read(ser.inWaiting());
	if back not in rec_buff.decode():
		resp = str(rec_buff.decode().replace('\n', '|').replace('\r', ''));
		func.log('sim.py', 'send_at', command + ' ERROR');
		func.log('sim.py', 'send_at', command + ' back:\t' + rec_buff.decode());
		return resp;
	else:
		resp = str(rec_buff.decode().replace('\n', '|').replace('\r', ''));
		if len(resp) > 0:
			func.log('sim.py', 'send_at', resp);
		return resp;

def power_on():
	global ser, power_key;
	GPIO.setmode(GPIO.BCM);
	GPIO.setwarnings(False);
	GPIO.setup(power_key,GPIO.OUT);
	time.sleep(0.25);
	GPIO.output(power_key,GPIO.HIGH);
	time.sleep(2);
	GPIO.output(power_key,GPIO.LOW);
	#time.sleep(20);
	time.sleep(2);
	ser.flushInput();

def power_off():
	try:
		global ser, power_key;
		GPIO.setmode(GPIO.BCM);
		GPIO.setwarnings(False);
		GPIO.setup(power_key,GPIO.OUT);
		time.sleep(0.25);
		GPIO.output(power_key,GPIO.LOW);
		#time.sleep(20);
		time.sleep(2);
		ser.flushInput();
		send_at('AT+CPOF','OK',1);
	except :
		func.log('sim.py', 'power_off', 'error: ' + str(sys.exc_info()[0]));

def check_voltage():
	voltage = '';
	try:
		resp = send_at('AT+CBC','OK',0.5);
		#func.log('sim.py', 'check_voltage', 'resp: ' + resp);
		if "V" in resp:
			voltage = resp[13:19];
	except:
		func.log('sim.py', 'check_voltage', 'error: ' + str(sys.exc_info()[0]));
	return voltage;

def get_call_info():
	resp = '';
	try:
		resp = send_at('AT+CLCC','CLCC',0.5);

		#|+CLCC: 2,1,4,0,0,"+12076192651",145||OK|
		call_info = '';
		temp = re.findall('"([^"]*)"', resp);
		if len(temp) > 0:
			call_info = temp[0];
		#func.log('sim.py', 'get_call_info', 'resp: ' + call_info);
	except:
		func.log('sim.py', 'get_call_info', 'error: ' + str(sys.exc_info()[0]));

	return call_info;

def get_signal():
	resp = '';
	signal = '';

	try:
		resp = send_at('AT+CSQ','OK',0.5);
		signal = resp[resp.find(': ')+1 : resp.find('||')];
	except:
		func.log('sim.py', 'get_signal', 'error: ' + str(sys.exc_info()[0]));
	
	#func.log('sim.py', 'get_signal', 'signal: ' + signal);
	return signal;

def get_network():
	resp = '';
	network = '';

	try:
		resp = send_at('AT+CPSI?','OK',0.5);
		network = resp[resp.find(': ')+1 : resp.find(',')];
	except:
		func.log('sim.py', 'get_network', 'error: ' + str(sys.exc_info()[0]));
	
	#func.log('sim.py', 'get_network', 'network: ' + network);
	return network;

def send_tone(tone):
	try:
		send_at('AT+VTS="'+tone+'"','OK',1);
	except :
		func.log('sim.py', 'send_tone', 'error: ' + sys.exc_info()[0]);

def make_call(phone_number):
	try:
		send_at(b'ATD' + phone_number.encode() +b';\r','OK',4);
	except :
		func.log('sim.py', 'make_call', 'error: ' + sys.exc_info()[0]);

def send_short_message(phone_number,text_message):
	global ser;
	func.log('sim.py', 'send_short_message', 'Setting SMS mode...');
	send_at("AT+CMGF=1","OK",0.5);
	func.log('sim.py', 'send_short_message', 'Sending Short Message');
	answer = send_at("AT+CMGS=\""+phone_number.encode()+"\"",">",1);
	ser.write(text_message.encode());
	ser.write(b'\x1A');
	return answer;

def receive_short_message(msgId):
	rec_buff = '';
	send_at('AT+CMGF=1','OK',0.5);
	send_at('AT+CPMS=\"SM\",\"SM\",\"SM\"', 'OK', 1);
	answer = send_at('AT+CMGR='+msgId,'+CMGR:',2);
	if 1 == answer:
		answer = 0;
		if 'OK' in rec_buff:
			answer = 1;
			func.log('sim.py', 'receive_short_message', 'rec_buff: ' + rec_buff.decode());
	else:
		func.log('sim.py', 'receive_short_message', 'error%d'%answer);
		return False;
	return True;

def delete_message(msgId):
	func.log('sim.py', 'delete_message', 'Deleting message');
	answer = send_at('AT+CMGD='+msgId,'OK',5);
	if 1 == answer:
		func.log('sim.py', 'delete_message', 'delete successfully');
	else:
		func.log('sim.py', 'delete_message', 'error%d'%answer);

def hangup():
	global ser;
	try:
		ser.write('AT+CHUP\r\n'.encode());
	except :
		func.log('sim.py', 'hangup', 'error: ' + str(sys.exc_info()[0]));

def answer_call():
	try:
		send_at('ATA','OK',0.5);
	except :
		func.log('sim.py', 'answer_call', 'error: ' + str(sys.exc_info()[0]));
