#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

#ser = serial.Serial('/dev/cu.SLAB_USBtoUART',115200);
#ser = serial.Serial('/dev/ttyS0',115200);
ser = serial.Serial('/dev/serial0',9600);
ser.flushInput();

phone_number = '12076192651';
text_message = 'this is a test';
power_key = 4;
rec_buff = '';

def check_for_msg():
	rec_buff = '';
	time.sleep(0.25);
	if ser.inWaiting():
		time.sleep(0.01 );
		rec_buff = ser.read(ser.inWaiting());

	print('sim.check_for_msg() ~ rec_buff: ' + rec_buff.decode());
	return rec_buff.decode();

def send_at(command,back,timeout):
	rec_buff = '';
	ser.write((command+'\r\n').encode());
	time.sleep(timeout);
	if ser.inWaiting():
		time.sleep(0.01 );
		rec_buff = ser.read(ser.inWaiting());
	if back not in rec_buff.decode():
		print(command + ' ERROR');
		print(command + ' back:\t' + rec_buff.decode());
		return 'ERROR';
	else:
		print(rec_buff.decode());
		return rec_buff.decode();

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
		if ser != None:
			ser.close();

	if ser != None:
		ser.close();

def check_voltage():
	try:
		resp = send_at('AT+CBC','OK',0.5);
		print('sim.check_voltage() ~ resp: ' + resp);
	except:
		print('sim.check_voltage() ~ error getting voltage');

def make_call(phone_number):
	try:
		#power_on();
		send_at('ATD'+phone_number+';','OK',1);
		time.sleep(10);
		ser.write('AT+CHUP\r\n'.encode());
		print('Call disconnected');
		#power_down();
	except :
		if ser != None:
			ser.close();
			GPIO.cleanup();

	if ser != None:
		ser.close();
		GPIO.cleanup();

def send_short_message(phone_number,text_message):
	print("Setting SMS mode...");
	send_at("AT+CMGF=1","OK",1);
	print("Sending Short Message");
	answer = send_at("AT+CMGS=\""+phone_number+"\"",">",2);
	if 1 == answer:
		ser.write(text_message.encode());
		ser.write(b'\x1A');
		answer = send_at('','OK',20);
		if 1 == answer:
			print('send successfully');
		else:
			print('error');
	else:
		print('error%d'%answer);

def receive_short_message(msgId):
	rec_buff = '';
	print('Setting SMS mode...');
	send_at('AT+CMGF=1','OK',1);
	send_at('AT+CPMS=\"SM\",\"SM\",\"SM\"', 'OK', 1);
	answer = send_at('AT+CMGR='+msgId,'+CMGR:',2);
	if 1 == answer:
		answer = 0;
		if 'OK' in rec_buff:
			answer = 1;
			print(rec_buff);
	else:
		print('error%d'%answer);
		return False;
	return True;

def delete_message(msgId):
	print('Deleting message');
	answer = send_at('AT+CMGD='+msgId,'OK',5);
	if 1 == answer:
		print('delete successfully');
	else:
		print('error%d'%answer);

def read_voltage():
	print('Reading voltage');
	send_at('AT+CBC','',2);
