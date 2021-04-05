import time;

def print_test():
    print('This is a test');

def log(file, service, text):
    mytime = time.strftime('%a, %d %b %Y %H:%M:%S GMT' + time.localtime());
    print(str(file) + '.' + str(mytime) + '() ~ ' + str(text));