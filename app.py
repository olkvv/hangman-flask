import os
import random
import time

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "tajny_klucz_do_gry")

POZIOMY = {
    "latwy": {"nazwa": "Łatwy", "proby": 8},
    "sredni": {"nazwa": "Średni", "proby": 6},
    "trudny": {"nazwa": "Trudny", "proby": 4},
    "przyslowia": {
        "nazwa": "Przysłowia",
        "proby": 8,
        "plik": "slowa/przyslowia.txt",
    },
}

KATEGORIE = {
    "programowanie": {
        "nazwa": "Programowanie",
        "plik": "slowa/programowanie.txt",
        "opis": "Słowa ze świata kodu, komputerów i algorytmów.",
    },
    "zwierzeta": {
        "nazwa": "Zwierzęta",
        "plik": "slowa/zwierzeta.txt",
        "opis": "Nazwy zwierząt, od domowych po egzotyczne.",
    },
    "jedzenie": {
        "nazwa": "Jedzenie",
        "plik": "slowa/jedzenie.txt",
        "opis": "Potrawy, produkty i smaki z kuchni.",
    },
    "sport": {
        "nazwa": "Sport",
        "plik": "slowa/sport.txt",
        "opis": "Dyscypliny, sprzęt i pojęcia sportowe.",
    },
    "geografia": {
        "nazwa": "Geografia",
        "plik": "slowa/geografia.txt",
        "opis": "Miasta, kraje, kontynenty i miejsca na mapie.",
    },
    "muzyka": {
        "nazwa": "Muzyka",
        "plik": "slowa/muzyka.txt",
        "opis": "Instrumenty, gatunki i pojęcia muzyczne.",
    },
}

POLSKI_ALFABET = [
    "a", "ą", "b", "c", "ć", "d", "e", "ę", "f", "g", "h", "i", "j",
    "k", "l", "ł", "m", "n", "ń", "o", "ó", "p", "r", "s", "ś", "t",
    "u", "w", "y", "z", "ź", "ż", "q", "v", "x",
]


def wczytaj_slowa(nazwa_pliku):
    with open(nazwa_pliku, "r", encoding="utf-8") as plik:
        return [slowo.strip().lower() for slowo in plik if slowo.strip()]


def przygotuj_haslo(haslo, odgadniete_litery):
    return [
        znak if not znak.isalpha() or znak in odgadniete_litery else "_"
        for znak in haslo
    ]


def sprawdz_wygrana(haslo, odgadniete_litery):
    return all(not znak.isalpha() or znak in odgadniete_litery for znak in haslo)


def uzyj_podpowiedzi(haslo, odgadniete_litery, proby):
    if proby <= 1:
        return proby, "Podpowiedź jest zablokowana, bo została Ci ostatnia próba."

    nieodgadniete_litery = [
        znak for znak in haslo if znak.isalpha() and znak not in odgadniete_litery
    ]

    if nieodgadniete_litery:
        podpowiedz = random.choice(nieodgadniete_litery)
        odgadniete_litery.append(podpowiedz)
        return proby - 1, "Podpowiedź odkryła literę: " + podpowiedz.upper()

    return proby, "Nie ma już liter do podpowiedzi."


def rozpocznij_gre(poziom_id, kategoria_id):
    poziom = POZIOMY.get(poziom_id, POZIOMY["sredni"])
    kategoria = KATEGORIE.get(kategoria_id, KATEGORIE["programowanie"])
    plik_hasel = poziom.get("plik", kategoria["plik"])
    haslo = random.choice(wczytaj_slowa(plik_hasel))

    session["haslo"] = haslo
    session["proby"] = poziom["proby"]
    session["maks_proby"] = poziom["proby"]
    session["odgadniete_litery"] = []
    session["poziom"] = poziom["nazwa"]
    session["kategoria"] = "Przysłowia" if poziom_id == "przyslowia" else kategoria["nazwa"]
    session["poziom_id"] = poziom_id
    session["kategoria_id"] = kategoria_id
    session["czas_start"] = time.time()


def stan_gry(komunikat=None, koniec_gry=False, wygrana=False, czas_gry=None):
    haslo = session["haslo"]
    proby = session["proby"]
    maks_proby = session["maks_proby"]
    odgadniete_litery = session["odgadniete_litery"]
    wpisane_litery = sorted(
        odgadniete_litery,
        key=lambda znak: POLSKI_ALFABET.index(znak) if znak in POLSKI_ALFABET else 99,
    )
    bledy = maks_proby - proby
    etap_wisielca = min(6, round((bledy / maks_proby) * 6)) if maks_proby else 0

    return {
        "poziom": session["poziom"],
        "kategoria": session["kategoria"],
        "proby": proby,
        "maks_proby": maks_proby,
        "bledy": bledy,
        "etap_wisielca": etap_wisielca,
        "haslo": przygotuj_haslo(haslo, odgadniete_litery),
        "komunikat": komunikat,
        "wpisane_litery": wpisane_litery,
        "koniec_gry": koniec_gry,
        "wygrana": wygrana,
        "czas_gry": czas_gry,
        "alfabet": POLSKI_ALFABET,
    }


def zakoncz_jesli_trzeba(komunikat):
    haslo = session["haslo"]
    proby = session["proby"]
    odgadniete_litery = session["odgadniete_litery"]

    if sprawdz_wygrana(haslo, odgadniete_litery):
        czas_gry = round(time.time() - session["czas_start"], 2)
        return True, True, czas_gry, "Brawo! Odgadłaś całe hasło."

    if proby == 0:
        czas_gry = round(time.time() - session["czas_start"], 2)
        return True, False, czas_gry, "Koniec gry. Hasło to: " + haslo.upper()

    return False, False, None, komunikat


@app.route("/")
def home():
    return render_template("index.html", poziomy=POZIOMY, kategorie=KATEGORIE)


@app.route("/start", methods=["POST"])
def start():
    rozpocznij_gre(
        request.form.get("poziom", "sredni"),
        request.form.get("kategoria", "programowanie"),
    )
    return redirect(url_for("game"))


@app.route("/game")
def game():
    if "haslo" not in session:
        return redirect(url_for("home"))
    return render_template("game.html", **stan_gry())


@app.route("/guess", methods=["POST"])
def guess():
    if "haslo" not in session:
        return redirect(url_for("home"))

    litera = request.form.get("litera", "").strip().lower()
    haslo = session["haslo"]
    proby = session["proby"]
    odgadniete_litery = session["odgadniete_litery"]

    if len(litera) != 1 or not litera.isalpha():
        komunikat = "Podaj dokładnie jedną literę."
    elif litera in odgadniete_litery:
        komunikat = "Ta litera była już wpisana."
    else:
        odgadniete_litery.append(litera)
        if litera in haslo:
            komunikat = "Dobrze! Ta litera jest w haśle."
        else:
            proby -= 1
            komunikat = "Pudło. Spróbuj kolejną literę."

    session["proby"] = proby
    session["odgadniete_litery"] = odgadniete_litery

    koniec_gry, wygrana, czas_gry, komunikat = zakoncz_jesli_trzeba(komunikat)
    return render_template(
        "game.html",
        **stan_gry(komunikat, koniec_gry, wygrana, czas_gry)
    )


@app.route("/hint", methods=["POST"])
def hint():
    if "haslo" not in session:
        return redirect(url_for("home"))

    proby, komunikat = uzyj_podpowiedzi(
        session["haslo"],
        session["odgadniete_litery"],
        session["proby"],
    )

    session["proby"] = proby
    koniec_gry, wygrana, czas_gry, komunikat = zakoncz_jesli_trzeba(komunikat)
    return render_template(
        "game.html",
        **stan_gry(komunikat, koniec_gry, wygrana, czas_gry)
    )


@app.route("/restart", methods=["POST"])
def restart():
    if "poziom" not in session or "kategoria" not in session:
        return redirect(url_for("home"))

    poziom_id = session.get("poziom_id", "sredni")
    kategoria_id = session.get("kategoria_id", "programowanie")
    rozpocznij_gre(poziom_id, kategoria_id)
    return redirect(url_for("game"))


if __name__ == "__main__":
    app.run(debug=True)
