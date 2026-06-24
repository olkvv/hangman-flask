import random, time

# FUNKCJE:

def wczytaj_slowa(nazwa_pliku):
    with open(nazwa_pliku, "r", encoding="utf-8") as plik:
        slowa = plik.read().splitlines()
    return slowa

def przygotuj_haslo(haslo, odgadniete_litery):
    wyswietlane_haslo = ""

    for znak in haslo:
        if znak in odgadniete_litery:
            wyswietlane_haslo = wyswietlane_haslo + znak + " "
        else:
            wyswietlane_haslo = wyswietlane_haslo + "_ "

    return wyswietlane_haslo

def sprawdz_wygrana(haslo, odgadniete_litery):
    for znak in haslo:
        if znak not in odgadniete_litery:
            return False
    return True

def wybierz_poziom():
    print("Wybierz poziom trudności:")
    print("1 - Łatwy: 8 prób")
    print("2 - Średni: 6 prób")
    print("3 - Trudny: 4 próby")

    wybor_poziomu = input("Podaj numer poziomu: ")

    if wybor_poziomu == "1":
        return "Łatwy", 8
    elif wybor_poziomu == "2":
        return "Średni", 6
    elif wybor_poziomu == "3":
        return "Trudny", 4
    else:
        print("Nieprawidłowy wybór. Domyślnie wybrano poziom: Średni")
        return "Średni", 6

def wybierz_kategorie():
    print("\nWybierz kategorię:")
    print("1 - Programowanie")
    print("2 - Zwierzęta")

    wybor = input("Podaj numer kategorii: ")

    if wybor == "1":
        return "Programowanie", "slowa/programowanie.txt"
    elif wybor == "2":
        return "Zwierzęta", "slowa/zwierzeta.txt"
    else:
        print("Nieprawidłowy wybór. Domyślnie wybrano kategorię: Programowanie")
        return "Programowanie", "slowa/programowanie.txt"

def uzyj_podpowiedzi(haslo, odgadniete_litery, proby):
    if proby <= 1:
        print("Nie możesz użyć podpowiedzi, bo została Ci tylko 1 próba.")
        return proby

    nieodgadniete_litery = []

    for znak in haslo:
        if znak not in odgadniete_litery:
            nieodgadniete_litery.append(znak)

    if len(nieodgadniete_litery) > 0:
        podpowiedz = random.choice(nieodgadniete_litery)
        odgadniete_litery.append(podpowiedz)
        proby = proby - 1

        print("Podpowiedź odkryła literę:", podpowiedz)
        print("Pozostało prób:", proby)
    else:
        print("Nie ma już liter do podpowiedzi.")

    return proby

def czy_poprawna_litera(litera):
    if len(litera) != 1 or not litera.isalpha():
        return False
    return True


def main ():
    print("Witaj w grze Wisielec!")

    poziom, proby = wybierz_poziom()

    nazwa_kategorii, plik_kategorii = wybierz_kategorie()

    slowa = wczytaj_slowa(plik_kategorii)
    haslo = random.choice(slowa)

    odgadniete_litery = []

    czas_start = time.time()

    print("Kategoria:", nazwa_kategorii)
    print("Hasło ma", len(haslo), "liter.")


    while proby > 0:
        print("\nHasło:")

        print(przygotuj_haslo(haslo, odgadniete_litery))

        print("\nWpisane litery:", odgadniete_litery)

        litera = input("\nPodaj literę albo wpisz ? aby użyć podpowiedzi: ").lower()

        if litera == "?":
            proby = uzyj_podpowiedzi(haslo, odgadniete_litery, proby)
            continue

        if not czy_poprawna_litera(litera):
            print("Podaj dokładnie jedną literę.")
            continue

        if litera in odgadniete_litery:
            print("Ta litera była już wpisana.")
            continue

        odgadniete_litery.append(litera)

        if litera in haslo:
            print("Dobrze!")
        else:
            print("Nie ma takiej litery.")
            proby = proby - 1
            print("Pozostało prób:", proby)

        if sprawdz_wygrana(haslo, odgadniete_litery):
            czas_koniec = time.time()
            czas_gry = round(czas_koniec - czas_start, 2)

            print("\nGratulacje! Odgadłaś hasło:", haslo)
            print("Czas gry:", czas_gry, "sekund")
            break

    if proby == 0:
        czas_koniec = time.time()
        czas_gry = round(czas_koniec - czas_start, 2)

        print("\nKoniec gry. Hasło to:", haslo)
        print("Czas gry:", czas_gry, "sekund")

if __name__ == "__main__":
    main()
