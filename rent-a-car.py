from abc import ABC, abstractmethod
from datetime import date, datetime


class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def get_info(self):
        pass


class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ajtok_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ajtok_szama = ajtok_szama

    def get_info(self):
        return f"Személyautó: {self.tipus} ({self.rendszam}), {self.ajtok_szama} ajtós - {self.berleti_dij} Ft/nap"


class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, max_teher):
        super().__init__(rendszam, tipus, berleti_dij)
        self.max_teher = max_teher

    def get_info(self):
        return f"Teherautó: {self.tipus} ({self.rendszam}), max {self.max_teher} kg - {self.berleti_dij} Ft/nap"


class Berles:
    def __init__(self, auto, datum, berlo_neve):
        self.auto = auto
        self.datum = datum
        self.berlo_neve = berlo_neve

    def __str__(self):
        return f"{self.datum} - {self.auto.rendszam} ({self.auto.tipus}) - Bérelte: {self.berlo_neve}"


class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaad(self, auto):
        self.autok.append(auto)

    def listaz_autok(self):
        if not self.autok:
            return "Jelenleg nincs elérhető autó."
        return "\n".join(auto.get_info() for auto in self.autok)

    def foglalt_datumok(self, rendszam):
        return sorted(
            berles.datum for berles in self.berlesek if berles.auto.rendszam == rendszam
        )

    def berel_auto(self, rendszam, datum, berlo_neve):
        auto = next((a for a in self.autok if a.rendszam == rendszam), None)
        if not auto:
            return "Az Ön által megadott rendszámon nincs nyilvántartott autónk. Kérjük próbálja meg ismét, ügyelve a kis és nagy betükre."
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                return "Sajnálattal közöljük, hogy az Ön által választott autó már **foglalt** a kért időszakban. Kérjük válasszon egy másik autót. Amennyiben ragaszkodik az eredeti autómodellhez, javasoljuk, hogy módosítsa a bérlés dátumát."
        uj_berles = Berles(auto, datum, berlo_neve)
        self.berlesek.append(uj_berles)
        return f"Sikeres bérlés! Ár: {auto.berleti_dij} Ft"

    def lemond_berles(self, rendszam, datum):
        for i, berles in enumerate(self.berlesek):
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                del self.berlesek[i]
                return "Bérlése lemondásra került."
        return "Nem szerepel ilyen bérlés rendszerünkben. Kérjük próbálja meg ismételten, figyelve a helyesírásra és a kis és nagy betükre!"

    def listaz_berlesek(self):
        if not self.berlesek:
            return "Nincs aktuális bérlés."
        return "\n".join(str(b) for b in self.berlesek)


# Inicializálás
kolcsonzo = Autokolcsonzo("Rent-a-car")
kolcsonzo.auto_hozzaad(Szemelyauto("AAA-111", "Audi A8", 85000, 5))
kolcsonzo.auto_hozzaad(Szemelyauto("BBB-222", "Lamborghini Countach", 350000, 2))
kolcsonzo.auto_hozzaad(Teherauto("CCC-333", "Freightliner FLA 9664", 32000, 18100))

kolcsonzo.berel_auto("AAA-111", date(2025, 6, 1), "Jason Statham")
kolcsonzo.berel_auto("AAA-111", date(2025, 6, 2), "Madonna Louise Veronica Ciccone")
kolcsonzo.berel_auto("BBB-222", date(2025, 6, 1), "Jordan Belfort")
kolcsonzo.berel_auto("CCC-333", date(2025, 6, 3), "Robert Patrick")


# Felhasználói interfész
while True:
    print("\n--- Rent-a-car ---")
    print("1. Gépjármű bérlés")
    print("2. Bérlés lemondása")
    print("3. Bérlések listázása")
    print("0. Kilépés")
    valasztas = input("Válassz műveletet: ")

    if valasztas == "1":
        print("\nElérhető autók:")
        print(kolcsonzo.listaz_autok())
        rendszam = input("Add meg az autó rendszámát: ")

        auto = next((a for a in kolcsonzo.autok if a.rendszam == rendszam), None)
        if not auto:
            print("Nincs ilyen rendszámú autó. Kérlek, ellenőrizd a rendszámot, ügyelve a kis és nagy betűkre!")
            continue

        foglaltak = kolcsonzo.foglalt_datumok(rendszam)
        if foglaltak:
            print("Foglalt dátumok erre az autóra:")
            for d in foglaltak:
                print(f" - {d}")
        else:
            print("Ez az autó jelenleg szabad minden nap.")

        datum_str = input("Add meg a bérlés dátumát (éééé-hh-nn): ")
        berlo = input("Add meg a neved: ")
        try:
            ev, ho, nap = map(int, datum_str.split("-"))
            datum = date(ev, ho, nap)
            if datum <= date.today():
                print("Csak holnaptól lehet időpontot foglalni.")
                continue
            print(kolcsonzo.berel_auto(rendszam, datum, berlo))
        except ValueError:
            print("Hibás dátum formátum.")

    elif valasztas == "2":
        rendszam = input("Add meg a rendszámot: ")
        datum_str = input("Add meg a dátumot (éééé-hh-nn): ")
        try:
            ev, ho, nap = map(int, datum_str.split("-"))
            datum = date(ev, ho, nap)
            print(kolcsonzo.lemond_berles(rendszam, datum))
        except ValueError:
            print("Hibás dátum formátum.")

    elif valasztas == "3":
        print("\nAktuális bérlések:")
        print(kolcsonzo.listaz_berlesek())

    elif valasztas == "0":
        print("Köszönjük, hogy a Rent-a-car autókölcsönzőt választotta! Viszont látásra!")
        break

    else:
        print("Nincs ilyen menüpont!")
