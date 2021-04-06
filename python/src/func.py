import time;

def print_test():
    print('This is a test');

def log(file, service, text):
    f = open("/home/pi/justaphone/python/phone.log", "a");
    mystring = str(time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime())) + ' *** ' + str(service) + '() ~ ' + str(text);
    
    if "send_at" in str(service):
        # don't print
        f.write(mystring + '\r\n');

    print(mystring);


