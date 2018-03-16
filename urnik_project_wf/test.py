import csv
from random import sample

def preference_csv_to_dict(csvfilename, keyfield):
    """
    prebere CSV file z imenom csvfilename,
    vrne dict of dicts, v katerem so tehniki in njihove preference
    """
    table = {}
    with open(csvfilename, "rt", newline="") as csvfile:
        csvreader = csv.DictReader(csvfile,
                                   skipinitialspace=True)
        for row in csvreader:
            table[row[keyfield]] = row
    return table

def check_if_candidates(dan, tehniki):
    """
    input: Dan, dict of dicts Tehnikov.
    output: vrne list tehnikov, ki bi radi delali ta dan,
    razvrscen po tockah (1. z najvec hoce_tmp)
    """
    kandidati = []
    for key, val in tehniki.items():
        print(val.preference["hoce"])
        if dan.cifra in val.preference["hoce"]:
            kandidati.append(val)
    sortirani_kandidati = sorted(kandidati, key=lambda tehnik : tehnik.tocke["hoce_tmp"], reverse=True)
    print("sortirani kandidati, ki hocejo delati ta dan: ", [s.name for s in sortirani_kandidati])
    return sortirani_kandidati

def naredi_urnik(mesec, tehniki):
    #
    """urnik = {}
    temp_stanje = {}
    for dan in mesec:
        tehniki = sample(tehniki, k=len(tehniki)) #premesa vrstni red tehnikov, trenutno nakljucno
    """
    print("delam urnik...")
    st_dni = len(mesec)
    print("st. dni: ", st_dni)

    #tehnikom daj temporary tocke na 0, ker se dela nov urnik:
    for t in tehniki.values():
        t.tocke["hoce_tmp"] = 0
        t.tocke["noce_tmp"] = 0
        t.tocke["opt_tmp"] = 0
        print("ime: ", t.name, ", tmp_tocke: ", t.tocke)

    dnevi_za_zafilat = [] #sem gredo dnevi, ko lab dela in ni dolocenega tehnika
    #for dan in mesec:
    #preveri ce je lab odprt:
        #if dan.laboratorij_odprt:
    #        print("kle sm ostal, 59")
            #preveri, ce je se prosto mesto za tehnika:
    #        if not dan.tehnik_dela:
                #doloci najustreznejsega tehnika s seznama prostovoljcev za ta dan
    #                       pass

class Tehnik: #ima ime, preference (max/min/zeleno stevilo nocnih; dneve, ko ne more; dneve, ko bi; zaporedne da/ne)

    def __init__(self, name):
        self.name = name
        self.preference = {}
        self.tocke = {}
        """
                        tole je dict 6 vrednosti:
                        hoce - hoce (+ na dan, ko ne dela, pa bi rad)
                        noce - noce (+ na dan, ko dela, pa noce)
                        opt - optimalno (+, ko stevilo nocnih, ko dela, odstopa)
                        hoce_tmp - hoce temporary (0 na zacetku izdelave urnika)
                        noce_tmp
                        opt_tmp
        """
    def __str__(self):
        return str(self.name)

    def add_nocne_max(self, nocne_max):
        self.preference["nocne_max"] = nocne_max

    def add_nocne_min(self, nocne_min):
        self.preference["nocne_min"] = nocne_min

    def add_nocne_opt(self, nocne_opt): #optimalno stevilo nocnih
        self.preference["nocne_opt"] = nocne_opt

    def add_hoce(self, hoce_str): #dnevi, ko bi rad delal - prejme string, vrne list
        hoce_list_stringov = hoce_str.split(sep=",") #iz str naredi list stringov
        hoce_list = [int(day) for day in hoce_list_stringov] #tole bo list integerjev...
        print("hoce_list", hoce_list, "len: ", len(hoce_list))
        self.preference["hoce"] = hoce_list

    def add_noce(self, noce_str): #dnevi, ko noce/ne more delati
        noce_list_stringov = noce_str.split(sep=",")
        noce_list = [(int(day)) for day in noce_list_stringov]
        print("noce_list", noce_list, "len: ", len(noce_list))
        self.preference["noce"] = noce_list

    def add_zaporedne(self, zaporedne): #koliko zaporednih
        self.preference["zaporedne"] = zaporedne
        #to do: ne, vseeno, z veseljem, koliko_max...

    def tocke_add_nece_pa_more(self, nece_pa_more):
        self.tocke["nece_pa_more"] = nece_pa_more

    def tocke_add_hoce_pa_nau(self, hoce_pa_nau):
        self.tocke["hoce_pa_nau"] = hoce_pa_nau

    def tocke_add_zeleno_stevilo(self, zeleno_stevilo):
        self.tocke["zeleno_stevilo"] = zeleno_stevilo


class Dan:

    laboratorij_odprt = True
    #to_do: __init__, __str__, povezi z Date objectom ali podobnim...
    def __init__(self):
        self.cifra = None #integer 1-31, kateri dan je... spremeni v Date object enkrat
        self.ne_bi_delal = [] #tehniki, ki ne bi delali ta dan
        self.rad_bi_delal = [] #tehniki, ki bi delali ta dan
        self.tehnik_dela = None #ta tehnik dela
        self.vsote_tock = [0, 0, 0] #hoce/noce/optimalno
        #self.laboratorij_odprt = laboratorij_odprt

    def __str__(self):
        return str(self.cifra)

    def add_tehnik_dela(self, tehnik):
        self.tehnik_dela = tehnik

    def add_ne_bi_delal(self, tehnik):
        self.ne_bi_delal.append(tehnik)

    def add_rad_bi_delal(self, tehnik):
        self.rad_bi_delal.append(tehnik)

    def laboratorij_zapri(self):
        self.laboratorij_odprt = False


class Urnik:

    def __init__(self):
        self.dnevi = [] #list of tuples (dan, tehnik_ki_dela)
        self.tocke = [0, 0, 0] #vsote tock - hoce/noce/zeleno
        self.votes = 0 #glasovi tehnikov


#test zone

#iz csv fajla naredi Tehnike s preferencami
def naredi_tehnike_iz_csv(csvfile, keyfield):
    """
    iz csv fajla naredi dict Tehnikov z njihovimi preferencami
    """
    preference = preference_csv_to_dict(csvfile, keyfield) #iz csv naredi dict of dicts (id: preference)
    tehniki = {}
    for tehnik, val in preference.items():
        tehniki[tehnik] = Tehnik(tehnik)
        tehniki[tehnik].add_nocne_max(val["nocne_max"])
        tehniki[tehnik].add_nocne_min(val["nocne_min"])
        tehniki[tehnik].add_nocne_opt(val["nocne_opt"])
        tehniki[tehnik].add_noce(val["noce"])
        tehniki[tehnik].add_hoce(val["hoce"])
        tehniki[tehnik].add_zaporedne(val["zaporedne"])

        print("Tehnik: ", tehniki[tehnik], "| bi delal max: ", tehniki[tehnik].preference["nocne_max"],
               "| min: ", tehniki[tehnik].preference["nocne_min"],
               "| opt: ", tehniki[tehnik].preference["nocne_opt"],
               "| noce: ", tehniki[tehnik].preference["noce"],
               "| hoce: ", tehniki[tehnik].preference["hoce"],
               "| zaporedne: ", tehniki[tehnik].preference["zaporedne"],)
        #print("jkljl", tehniki[tehnik].preference.nocne_max)
    print(tehniki)
    return(tehniki)


#naredi dict Tehnikov iz csv fajla
tehniki = naredi_tehnike_iz_csv("preference.csv", "id")
print("tehniki iz csv, type: ", type(tehniki))
print("tehniki iz csv: ", tehniki)

#naredi mesec - list Dni
mesec = []
for dan in range(1,31):
    d = Dan
    d.cifra = dan
    #d.laboratorij_odprt = True
    print("tole je 'laboratorij_odprt': ", d.laboratorij_odprt)
    mesec.append(d)
for dan in mesec:
    print(dan.laboratorij_odprt)

####
#testni dan:
testni_dan = Dan
testni_dan.cifra = 5
print(testni_dan.cifra)


#naredi urnik:

print("---------------")
naredi_urnik(mesec, tehniki)
kan = check_if_candidates(testni_dan, tehniki)
print("tile lahko delajo na testni_dan: ", kan)
print("-----test-sort---")
sortirani = sorted(tehniki.values(),key=lambda tehnik: tehnik.name,  reverse=True)
for s in range(len(sortirani)):
    print(sortirani[s].name)
