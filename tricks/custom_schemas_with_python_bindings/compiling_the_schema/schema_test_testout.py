#!/usr/bin/env python
#
from pxr import Usd
from testout import Testout

path = "/home/selecaoone/projects/usd_experiments/cpp_test/schema_generation3/using_schema2/Test.usda"
stage = Usd.Stage.Open(path)
cp = stage.GetPrimAtPath("/Complex")
simple = Testout.Simple(cp)
target = simple.GetTargetRel()
intAttr = simple.GetIntAttrAttr()
complex = Testout.Complex(cp)
print 'complexString: %s' % complex.GetComplexStringAttr().Get()
obj = stage.GetPrimAtPath("/Object")
paramsAPI = Testout.ParamsAPI.Apply(obj);
# assert obj.HasAPI(Testout.ParamsAPI)
print 'mass: %s' % paramsAPI.GetMassAttr().Get()
print 'velocity: %s' % paramsAPI.GetVelocityAttr().Get()
print 'volume: %s' % paramsAPI.GetVolumeAttr().Get()
