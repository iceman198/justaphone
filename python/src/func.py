import time;

def print_test():
    print('This is a test');

def log(file, service, text):
    print(str(file) + '.' + time.strftime('%a, %d %b %Y %H:%M:%S GMT' + time.localtime()) + '() ~ ' + str(text));