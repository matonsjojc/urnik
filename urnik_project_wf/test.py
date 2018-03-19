import csv
from random import choice

def preference_csv_to_dict(csvfilename, keyfield):
    """
    helper funkcija za naredi_tehnike_iz_csv.
    vrne dict of dicts, v katerem so tehniki in njihove preference
    """
    table = {}
    with open(csvfilename, "rt", newline="") as csvfile:
        csvreader = csv.DictReader(csvfile,
                                   skipinitialspace=True)
        for row in csvreader:
            table[row[keyfield]] = row
    return table

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
    #print(tehniki)
    return(tehniki)


def check_if_candidates(dan, tehniki):
    """
    input: Dan, dict of dicts Tehnikov.
    output: vrne list tehnikov, ki bi radi delali ta dan,
    razvrscen po tockah (1. z najvec hoce_tmp)
    """
    kandidati = []
    for key, val in tehniki.items():
        if dan.cifra in val.preference["hoce"]:
            kandidati.append(val)
    sortirani_kandidati = sorted(kandidati, key=lambda tehnik : tehnik.tocke["hoce_tmp"], reverse=True)
    #print("funkcija 'check_if_candidates', sortirani kandidati, ki hocejo delati ta dan: ", [s.name for s in sortirani_kandidati])
    return sortirani_kandidati

def zafilaj_proste_dni(dnevi_za_zafilat, tehniki):
    """
    in: list dni, ko ni se nihce dolocen/prostovoljec, dict tehnikov
    out: list, [0]: list dni, ko noben ne more, [1]: updatan dict tehnikov
    kaj: zapolni dneve, dolocenim tehnikom updata tocke["napisan_tmp"]
    """
    nobenega_ni_dnevi = [] #dnevi, ko ne more noben delati
    for dan in dnevi_za_zafilat:
        #tehniki, ki niso dali "noce" na ta dan in jih admin ni izlocil zz ta dan
        dostopni_tehniki = [t for t in tehniki.values() if (dan.cifra not in t.preference["noce"] and t.name not in dan.tehnik_ne_dela)]
        print("na ", dan.cifra, ". dan dostopni tehniki: ", [t.name for t in dostopni_tehniki])
        #izmed dostopnih izberi nakljucnega tehnika
        if dostopni_tehniki:
            dan.tehnik_dela = choice(dostopni_tehniki)
            dan.tehnik_dela.tocke["napisan_tmp"] += 1
            print("srečni izbranec od dostopnih: ", dan.tehnik_dela, "njegov napisan_tmp: ", dan.tehnik_dela.tocke["napisan_tmp"])
        else:
            nobenega_ni_dnevi.append(dan)
        print("dnevi, ko nobenega ni: ", [d.cifra for d in nobenega_ni_dnevi])
        return [nobenega_ni_dnevi, tehniki]


def naredi_urnik(mesec, tehniki):
    #
    """
    for dan in mesec:
        tehniki = sample(tehniki, k=len(tehniki)) #premesa vrstni red tehnikov, trenutno nakljucno
    """
    print("funkcija naredi_urnik...")
    st_dni = len(mesec)
    print("st. dni: ", st_dni)

    #tehnikom daj temporary tocke na 0, ker se dela nov urnik:
    for t in tehniki.values():
        t.tocke["hoce_tmp"] = 0
        t.tocke["noce_tmp"] = 0
        t.tocke["opt_tmp"] = 0
        t.tocke["napisan_tmp"] = 0
        #print("ime: ", t.name, ", tmp_tocke: ", t.tocke)

    dnevi_za_zafilat = [] #sem bodo sli dnevi, ko lab dela in ni dolocenega tehnika
    for dan in mesec:
    #preveri ce je lab odprt:
        if dan.laboratorij_odprt:
            print("\n", dan.cifra, " - dan, laboratorij je odprt")
            #preveri, ce je se prosto mesto za tehnika: (to do: tehniku, ki je ze napisan, pristej napisan_tmp)
            if not dan.tehnik_dela:
                #doloci najustreznejsega tehnika s seznama prostovoljcev za ta dan
                prostovoljci = check_if_candidates(dan, tehniki)
                print("prostovoljci: ", [p.name for p in prostovoljci])
                if not prostovoljci:
                    #nobenega prostovoljca/ze dolocenega za delo, ta dan bo treba dodat k dnevi_za_zafilat
                    dnevi_za_zafilat.append(dan)
                else:
                    #doloci prvega prostovoljca s seznama
                    dan.tehnik_dela = prostovoljci[0]
                    print("prostovoljec = ", dan.tehnik_dela)
                    #izloci "zmagovalca" in ostalim prilagodi hoce_tmp tocke - zaenkrat samo pristej +1, to do: formula st vseh dni - st dni, za katere se je tehnik javil                   prostovoljci.pop(0) #to do: uporabi deque from collections - hitrost...
                    prostovoljci.pop(0) #to do: tole zamenjaj z deque
                    print("ostali prostovoljci: ", [p.name for p in prostovoljci])
                    for p in prostovoljci:
                        p.tocke["hoce_tmp"] += 1
                        print("tehnik ", p.name, "ima", p.tocke["hoce_tmp"], "hoce_tmp tock.")
            else:
            #admin je ze dolocil tehnika
                print("na ta dan je admin dolocil, da dela: ", dan.tehnik_dela)

    print("dnevi za zafilat: ", [d.cifra for d in dnevi_za_zafilat])

    #for dan in dnevi_za_zafilat:
    print("konec f. naredi_urnik")

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
                        napisan_tmp - kolikokrat je v trenutnem urniku ze napisan
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
        #print("hoce_list", hoce_list, "len: ", len(hoce_list))
        self.preference["hoce"] = hoce_list

    def add_noce(self, noce_str): #dnevi, ko noce/ne more delati
        noce_list_stringov = noce_str.split(sep=",")
        noce_list = [(int(day)) for day in noce_list_stringov]
        #print("noce_list", noce_list, "len: ", len(noce_list))
        self.preference["noce"] = noce_list

    def add_zaporedne(self, zaporedne): #zaenkrat: T/F, to do: koliko zaporednih
        self.preference["zaporedne"] = zaporedne
        #to do: ne, vseeno, z veseljem, koliko_max...

    def tocke_add_nece_pa_more(self, nece_pa_more):
        self.tocke["nece_pa_more"] = nece_pa_more

    def tocke_add_hoce_pa_nau(self, hoce_pa_nau):
        self.tocke["hoce_pa_nau"] = hoce_pa_nau

    def tocke_add_zeleno_stevilo(self, zeleno_stevilo):
        self.tocke["zeleno_stevilo"] = zeleno_stevilo


class Dan:

    #to_do: __init__, __str__, povezi z Date objectom ali podobnim...
    def __init__(self):
        self.cifra = None #integer 1-31, kateri dan je... spremeni v Date object enkrat
        self.ne_bi_delal = None #tehniki, ki ne bi delali ta dan
        self.rad_bi_delal = [] #tehniki, ki bi delali ta dan
        self.tehnik_dela = None #ta tehnik dela
        self.tehnik_ne_dela = [] #ti tehniki ne delajo - doloci admin
        self.vsote_tock = [0, 0, 0] #hoce/noce/optimalno
        self.laboratorij_odprt = True

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
        self.tocke = [0, 0, 0] #vsote tock - hoce/noce/optimalno; to do: dodaj max odstopanje pri posameznem tehniku
        self.votes = 0 #glasovi tehnikov


#test zone



#naredi dict Tehnikov iz csv fajla
tehniki = naredi_tehnike_iz_csv("preference.csv", "id")
#print("tehniki iz csv, type: ", type(tehniki))
#print("tehniki iz csv: ", tehniki)

#naredi mesec - list Dni, za 1. dan dolocimo tehnika #na zac... 5 dni
mesec = []
for dan in range(1,6):
    d = Dan()
    d.cifra = dan
    if dan == 1:
        d.tehnik_dela = "fsfs"
    mesec.append(d)

#naredi urnik:

print("---------------")
naredi_urnik(mesec, tehniki)
