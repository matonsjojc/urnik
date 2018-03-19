"""
dct = {"prvi": {"key_od_val_prvega": "vallll"}, "drugi": 2, "tretji": 3}
print(dct)

for item in dct:
    print(dct[item])

print(dct["prvi"]["key_od_val_prvega"])


strng = "1,2,3,4"
a = strng.split(sep=",") #str.strip() uporabno...
print(type(a))
print(a)
print(len(a))
"""

"""
class TestClass:

    def __init__(self, atribut_a):
        self.atribut_a = atribut_a

a = TestClass(3)
print(a.atribut_a)

class Dan:

    def __init__(self):
        self.cifra = None
        self.ne_bi_delal = None
        self.rad_bi_delal = []
        self.tehnik_dela = None
        self.vsote_tock = [0, 0, 0]

    def __str__(self):
        return str(self.cifra)

d = Dan
d.cifra = 0
print(d.cifra)
"""
