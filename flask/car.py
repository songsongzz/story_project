from pxr import Usd


stage_ref = Usd.Stage.Open('car.usda')

prim_ref = stage_ref.GetPrimAtPath('/Car')
child_prim_ref = prim_ref.GetChild('Wheel')

# Prims can be cast as bool, so you can check if the prim exists by comparing
# its bool() overload
if child_prim_ref:
    print("/Car/Wheel exists") # This will execute

print(child_prim_ref.GetPath()) # Prints ""/Car/Wheel"


stage_ref = Usd.Stage.Open('car.usda')

for prim_ref in stage_ref.Traverse():
    print(prim_ref.GetPath())