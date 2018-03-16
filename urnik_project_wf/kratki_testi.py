"""
dct = {"prvi": {"key_od_val_prvega": "vallll"}, "drugi": 2, "tretji": 3}
print(dct)

for item in dct:
    print(dct[item])

print(dct["prvi"]["key_od_val_prvega"])
"""

strng = "1,2,3,4"
a = strng.split(sep=",") #str.strip() uporabno...
print(type(a))
print(a)
print(len(a))
