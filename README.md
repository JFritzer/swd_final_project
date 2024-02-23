# Musikerkennungstool (like Shazam)

Bei diesem Softwareprojekt handelt es sich um ein Abschlussprojekt für Vorlesung "Software-Design" des Vollzeitstudiums Mechatronik Design & Innovation am MCI-Innsbruck.

## Standard Funktionen:

* Musikstücke einlernen
* Musikstücke erkennen
* Musikstücke können über Adminpanel wiedergegeben werden


## Optionale Funktionen:

* Passwortgesichertes Adminpanel erstellt, um auf Datenbank zuzugreifen und Musikstücke zu verwalten.
* Supportpage eingebaut, um Userfeedback per E-Mail zu erhalten (z.B. für Fehlermeldungen).
* Youtubedownloader eingebaut, um Musikstücke zu erkennen, die in einem Teilbereich eines Youtubevideos vorkommen (Mit Ausschnittfunktion). (Test der Funktionalität z.B: https://www.youtube.com/watch?v=mmr6MVhycws)
* Musikerkennung über Mikrofon implementiert.
* Erkennungs- und Einlesevorgangsfortschrittserkennung implementiert (Ladebalken).
* Albumcover wird bei Erkennung mit ausgegeben.
* Teilmusikstücke zum testen bereitgestellt.
* Einstellungsseite als .py erstellt, um Variablen anzupassen innerhalb des Codes: `settings.py`
* Multithreading implementiert.


## Installation:

1. Repository clonen.
1. In VSCode virtual environment erstellen: `python -m venv venv`
2. Benötigte Bibliotheken über die Requierements.txt installieren: `pip install -r requirements.txt`
3. Starten von Streamlit: `streamlit run home.py`
4. Für Verwendung der Supportseite: E-Mail-Adresse und Passwort in `support.py` eintragen. (Aktuell konfiguriert auf Gmail inkl. 2FA) Hierbei muss ein App-Passwort verwendet werden.

## Benutzung:

1. Für das beste Erlebnis empfehlen wir die Verwendung von Google Chrome.
2. Musikstücke einlernen über das Music-Import-Panel.
3. Musikstücke erkennen über das Music-Recognition-Panel.
4. Musikstücke erkennen über den Youtube Downloader.
5. Musikstücke erkennen über das Mikrofon.
6. Bei Problemen das Support-Panel benutzen.
7. Falls Support nicht hilft, einfach das Admin-Panel benutzen. (Passwort = 1)

Hinweis: Die Audio Ausschnitte sollten 10-20 Sekunden nicht übersteigen, da ansonsten die Recognition zu lange dauert.

## Troubleshoting:

* Falls bei der Recognition über 20-30 Sekunden verwendet werden, kann es sein, dass er ewig ladet -> Streamlit nochmal starten und kürzeren Ausschnitt verwenden.
* Falls der Youtube Downloader nicht funktioniert, handelt es sich wahrscheinlich um ein Copyright geschütztes Video -> Anderes Video verwenden.
* Falls die Mikrofon-Recognition nicht funktioniert -> Wahrscheinlich Grundrauschen in der Aufnahme zu hoch -> Qualitativ höherwertiges Mikrofon verwenden.


## Quellen:

* Musikstücke: Free Copyright Music from Youtube
* Youtube Downloader: Pytube Bibliothek 
* Mikrofonaufnahmeprogramm: https://github.com/stefanrmmr/streamlit-audio-recorder
* Teile des Codes wurden mithilfe von CHAT-GPT erstellt und gedebuggt.
* Supportseite: https://github.com/tonykipkemboi/streamlit-smtp-test/blob/main/streamlit_app.py / https://discuss.streamlit.io/t/send-email-with-smtp-and-gmail-address/48145/4
* Grundwissen: https://www.cameronmacleod.com/blog/how-does-shazam-work
* Grundwissen: Matthias Panny - Abschlussprojekt_Aufgabenstellung - MCI 2024


## Ersteller:

* Patrick Monthaler
* Simon Mariacher
* Julian Fritzer