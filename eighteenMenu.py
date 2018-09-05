from oneMenu import oneMeal
import os

os.remove("/Users/christianjohnventura/Desktop/spis18/github/spisfinalproject2/menus/OVT/OVTBreakfast.csv")
os.remove("/Users/christianjohnventura/Desktop/spis18/github/spisfinalproject2/menus/OVT/OVTLunch.csv")
os.remove("/Users/christianjohnventura/Desktop/spis18/github/spisfinalproject2/menus/OVT/OVTDinner.csv")

# DegreesBreakfast = oneMeal(0, "64")
# DegreesLunch = oneMeal(1, "64")
# DegreesDinner = oneMeal(2, "64")

# cafeVBreakfast = oneMeal(0, "18")
# cafeVLunch = oneMeal(1, "18")
# cafeVDinner = oneMeal(2, "18")

# canyonVBreakfast = oneMeal(0, "24")
# canyonVLunch = oneMeal(1, "24")
# canyonVDinner = oneMeal(2, "24")

# FoodworxBreakfast = oneMeal(0, "11")
# FoodworxLunch = oneMeal(1, "11")
# FoodworxDinner = oneMeal(2, "11")

OVTBreakfast = oneMeal(0, "05")
OVTLunch = oneMeal(1, "05")
OVTDinner = oneMeal(2, "05")

# PinesBreakfast = oneMeal(0, "01")
# PinesLunch = oneMeal(1, "01")
# PinesDinner = oneMeal(2, "01")

if not (OVTBreakfast.empty):
    OVTBreakfast.to_csv("/Users/christianjohnventura/Desktop/spis18/github/spisfinalproject2/menus/OVT/OVTBreakfast.csv", header=None, index=None, sep=',', mode='a')
if not (OVTLunch.empty):
    OVTLunch.to_csv("/Users/christianjohnventura/Desktop/spis18/github/spisfinalproject2/menus/OVT/OVTLunch.csv", header=None, index=None, sep=',', mode='a')
if not (OVTDinner.empty):
    OVTDinner.to_csv("/Users/christianjohnventura/Desktop/spis18/github/spisfinalproject2/menus/OVT/OVTDinner.csv", header=None, index=None, sep=',', mode='a')


