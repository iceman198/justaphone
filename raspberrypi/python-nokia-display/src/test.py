#!/usr/bin/python
import sys;
import os;

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic');
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib');
if os.path.exists(libdir):
    sys.path.append(libdir);

print os.sys.path;

import sim;

sim.SendShortMessage("12076192651","this is a test");
#sim.ReceiveShortMessage("1");
#sim.DeleteMessage("2");

#sim.ReadVoltage();

#sim.power_down();
#sim.power_on();