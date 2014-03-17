import jpype
import os
from sfilter.bloomfilter import bf
import ywbweb.settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ywbweb.settings")
from merchant.models import *

if __name__ == "__main__":
  classpath = ".:./sfilter/IKAnalyzer2012_u6.jar" 
  jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % classpath)
  print os.getcwd()
  checkclass = jpype.JClass("Segmenter")

  #contentcol = Commercial.objects.all()
  for obj in Commercial.objects.all():
    checkobj = checkclass(obj.content)
    isvalid = True
    for item in checkobj.CutWord():
      print item
      if bf.lookup(item.encode('utf-8')):
        isvalid = False
        break
    if not isvalid:
      print "contain sensitive infomation"
      #obj.content = ""
      #obj.save()

 
   
