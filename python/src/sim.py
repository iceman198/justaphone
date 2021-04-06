#!/usr/bin/python

import sys;
import RPi.GPIO as GPIO;
import serial;
import time;
import func;

#ser = serial.Serial('/dev/cu.SLAB_USBtoUART',115200);
#ser = serial.Serial('/dev/ttyS0',115200);
ser = serial.Serial('/dev/serial0',9600);
ser.flushInput();

power_key = 4;

def check_for_msg():
	rec_buff = '';
	time.sleep(0.25);
	if ser.inWaiting():
		time.sleep(0.01 );
		rec_buff = ser.read(ser.inWaiting());

	resp = str(rec_buff.decode().replace('\n', '|').replace('\r', ''));
	if len(resp) > 0:
		func.log('sim.py', 'check_for_msg', 'resp: ' + resp);
	return resp;

def send_at(command,back,timeout):
	rec_buff = '';
	ser.write((command+'\r\n').encode());
	time.sleep(timeout);
	if ser.inWaiting():
		time.sleep(0.01);
		rec_buff = ser.read(ser.inWaiting());
	if back not in rec_buff.decode():
		func.log('sim.py', 'send_at', command + ' ERROR');
		func.log('sim.py', 'send_at', command + ' back:\t' + rec_buff.decode());
		return 'ERROR';
	else:
		resp = str(rec_buff.decode().replace('\n', '|').replace('\r', ''));
		if len(resp) > 0:
			func.log('sim.py', 'send_at', resp);
		return resp;

def power_on():
	GPIO.setmode(GPIO.BCM);
	GPIO.setwarnings(False);
	GPIO.setup(power_key,GPIO.OUT);
	time.sleep(0.1);
	GPIO.output(power_key,GPIO.HIGH);
	time.sleep(2);
	GPIO.output(power_key,GPIO.LOW);
	#time.sleep(20);
	time.sleep(2);
	ser.flushInput();

def power_off():
	try:
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

def make_call(phone_number):
	try:
		send_at('ATD'+phone_number+';','OK',1);
	except :
		func.log('sim.py', 'make_call', 'error: ' + sys.exc_info()[0]);

def send_short_message(phone_number,text_message):
	func.log('sim.py', 'send_short_message', 'Setting SMS mode...');
	send_at("AT+CMGF=1","OK",1);
	func.log('sim.py', 'send_short_message', 'Sending Short Message');
	answer = send_at("AT+CMGS=\""+phone_number+"\"",">",2);
	if 1 == answer:
		ser.write(text_message.encode());
		ser.write(b'\x1A');
		answer = send_at('','OK',20);
		if 1 == answer:
			func.log('sim.py', 'send_short_message', 'send successfully');
		else:
			func.log('sim.py', 'send_short_message', 'error');
	else:
		func.log('sim.py', 'send_short_message', 'error%d'%answer);

def receive_short_message(msgId):
	rec_buff = '';
	send_at('AT+CMGF=1','OK',1);
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
	try:
		ser.write('AT+CHUP\r\n'.encode());
	except :
		func.log('sim.py', 'hangup', 'error: ' + str(sys.exc_info()[0]));

def answer_call():
	try:
		send_at('ATA','OK',0.5);
	except :
		func.log('sim.py', 'answer_call', 'error: ' + str(sys.exc_info()[0]));
