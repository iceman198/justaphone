import time;

def print_test():
    print('This is a test');

def log(file, service, text):
    mystring = str(time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime())) + ' *** ' + str(service) + '() ~ ' + str(text);
    print(mystring);


