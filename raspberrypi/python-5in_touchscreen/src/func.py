import datetime;

def print_test():
    print('This is a test');

def log(file, service, text):
    f = open("./phone.log", "a");
    now = datetime.datetime.now();
    mystring = str(now.strftime('%Y-%m-%d %H:%M:%S')) + ' *** ' + str(file) + ' *** ' + str(service) + '() ~ ' + str(text);
    print(mystring);
    f.write(mystring+'\r\n');
