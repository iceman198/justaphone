import time;

f = open("/home/pi/justaphone/python/phone.log", "a");

def print_test():
    print('This is a test');

def log(file, service, text):
    global f;
    mystring = str(time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime())) + ' *** ' + str(file) + ' *** ' + str(service) + '() ~ ' + str(text);
    print(mystring);
    f.write(mystring+'\r\n');
