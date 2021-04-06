import time;

f = None;

def print_test():
    print('This is a test');

def log(file, service, text):
    global f;
    mystring = str(time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime())) + ' *** ' + str(service) + '() ~ ' + str(text);
    print(mystring);
    f.write(mystring + '\r\n');


def init_logfile():
    global f;
    f = open("/home/pi/justaphone/python/phone.log", "a");

