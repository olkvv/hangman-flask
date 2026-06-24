# Wisielec

Przeglądarkowa gra w wisielca napisana we Flasku. Gracz wybiera poziom trudności i kategorię, a następnie odgaduje hasło za pomocą formularza lub klikalnej klawiatury.

## Funkcje

- wybór poziomu trudności,
- wybór kategorii haseł,
- podpowiedź kosztem jednej próby,
- rysunek wisielca aktualizowany po błędach,
- responsywny interfejs do gry w przeglądarce.

## Uruchomienie lokalne

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Aplikacja uruchomi się pod adresem `http://127.0.0.1:5000`.

## Wdrożenie na Render

1. Dodaj projekt do GitHuba.
2. W Render wybierz `New Web Service` i podłącz repozytorium.
3. Ustaw:
   - build command: `pip install -r requirements.txt`
   - start command: `gunicorn app:app`
4. Dodaj zmienną środowiskową `SECRET_KEY` z własną losową wartością.
# hangman-flask
