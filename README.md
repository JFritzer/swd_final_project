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
* Multithreading implementiert bei Recognition.


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

## Zusatzinformationen für Matthias Panny:

Haben das ganze Backend (Grundfunktion der Software) ohne Vorlage aus Github geschrieben. Nur auf Basis des Papers. Kein kopieren vom Code der verlinkt ist / war.

Komischerweise funktionieren unsere 2 Beispielsongs ohne Probleme. Dein Cantina Sound funktioniert ebenfalls, aber Starwars haut einfach nicht hin. Wir können uns nicht erklären warum. Auch wenn wir das CantinaBand Lied von Youtube in die Datenbank einspielen und dann dein example recognisen funktioniert alles. Nur bei StarWars nicht.

Auch über Youtube funktionieren unsere 2 Songs ohne Probleme. 
* Romeo and Juliet: https://www.youtube.com/watch?v=zNGqtG4tjzQ
* Memorybox: https://www.youtube.com/watch?v=DFyIA76BvD0

Falls du irgendwelche Fragen hast, bitte bei uns melden.

Schöne Grüße
Fritzer Julian, Patrick Monthaler, Simon Mariacher

