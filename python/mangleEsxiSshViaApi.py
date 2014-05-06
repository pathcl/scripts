#!/usr/bin/env python
import sys
import time
try:
  from setproctitle import setproctitle
except ImportError, e:
  errMsg = "please install setproctitle see http://goo.gl/GNmtIX :C"
  print >> sys.stderr, errMsg
  sys.exit(2)
try:
   from pysphere import *
   from pysphere.resources import VimService_services as VI
except ImportError, e:
  errMsg = "please install pysphere see http://goo.gl/c7HGGi :C"
  print >> sys.stderr, errMsg
  sys.exit(2)


def StartService(self, strService):

    try:
        request = VI.StartServiceRequestMsg()
        #morHostServiceSystem = request.new__this("HostServiceSystem")
        result = self._retrieve_properties_traversal(['configManager.serviceSystem'], obj_type=MORTypes.HostSystem)[0]
        for prop in result.PropSet:
            if prop.Name == 'configManager.serviceSystem':
                morHostServiceSystem = request.new__this(prop.Val)
                morHostServiceSystem.set_attribute_type(MORTypes.HostServiceSystem)
                request.set_element__this(morHostServiceSystem)
                request.set_element_id(strService)
                self._proxy.StartService(request)
                return True
    except(VI.ZSI.FaultException), e:
        raise e
        return False


def StopService(self, strService):
    try:
        request = VI.StopServiceRequestMsg()

        #morHostServiceSystem = request.new__this("HostServiceSystem")
        result = self._retrieve_properties_traversal(['configManager.serviceSystem'], obj_type=MORTypes.HostSystem)[0]
        for prop in result.PropSet:
            if prop.Name == 'configManager.serviceSystem':
                morHostServiceSystem = request.new__this(prop.Val)
                morHostServiceSystem.set_attribute_type(MORTypes.HostServiceSystem)
                request.set_element__this(morHostServiceSystem)
                request.set_element_id(strService)
                self._proxy.StopService(request)

                return True
    except(VI.ZSI.FaultException), e:
        raise e
        return False


if (len(sys.argv) != 5):
  errMsg = ("%s %s %s") % ("usage", sys.argv[0], "[vcenter/esxi host] [login] [password] [start|stop] IN THAT ORDER!! :@")
  print >> sys.stderr, errMsg
  sys.exit(3)


host = str(sys.argv[1])
usr = str(sys.argv[2])
psw = str(sys.argv[3])


s = VIServer()
s.connect(host, usr, psw)
procname = ("%s %s %s %s") % (sys.argv[0], host, usr, "xxxxx")
setproctitle(procname)

action = str(sys.argv[4])

# Start SSH
if (action == "start"):
  StartService(s, 'TSM-SSH')
  time.sleep(10)

if (action == "stop"):
  StopService(s, 'TSM-SSH')
  time.sleep(10)
