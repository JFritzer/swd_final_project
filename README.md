# Musikerkennungstool (like Shazam)

## Standard Funktionen:

* Musikstücke einlernen
* Musikstücke erkennen
* Musikstücke können über Adminpanel wiedergegeben werden


## Optionale Funktionen:

* Passwortgesichertes Adminpanel erstellt, um auf Datenbank zuzugreifen und Musikstücke zu verwalten.
* Supportpage eingebaut, um Userfeedback per E-Mail zu erhalten (z.B. für Fehlermeldungen).
* Youtubedownloader eingebaut, um Musikstücke zu erkennen, die in einem Teilbereich eines Youtubevideos vorkommen (Mit Ausschnittfunktion).
* Musikerkennung über Mikrofon implementiert.
* Erkennungs- und Einlesevorgangsfortschrittserkennung implementiert (Ladebalken).
* Albumcover wird bei Erkennung mit ausgegeben.
* Teilmusikstücke zum testen bereitgestellt.
* Einstellungsseite als .py erstellt, um Variablen anzupassen innerhalb des Codes.


## Installation:

1. Repository clonen.
1. In VSCode virtual environment erstellen: `python -m venv venv`
2. Benötigte Bibliotheken über die Requierements.txt installieren: `pip install -r requirements.txt`
3. Starten von Streamlit: `streamlit run home.py`

## Benutzung:

1. Musikstücke einlernen über das Music-Import-Panel.
2. Musikstücke erkennen über das Music-Recognition-Panel.
3. Musikstücke erkennen über den Youtube Downloader.
4. Musikstücke erkennen über das Mikrofon.
5. Bei Problemen das Support-Panel benutzen.
6. Falls Support nicht hilft, einfach das Admin-Panel benutzen. (Passwort = 1)


## Quellen:

* Musikstücke: Free Copyright Music from Youtube
* Youtube Downloader: Pytube Bibliothek
* Mikrofonaufnahmeprogramm: https://github.com/stefanrmmr/streamlit-audio-recorder
* Teile des Codes wurden mithilfe von CHAT-GPT erstellt und gedebuggt.
* Grundwissen: https://www.cameronmacleod.com/blog/how-does-shazam-work
* Grundwissen: Matthias Panny - Abschlussprojekt_Aufgabenstellung - MCI 2024
