Hilfe, wie funktioniert nun diese GUI!
Verbindungsaufbau:
Nachdem der USB Anschluss der universalen Brückenschaltung (UEB) mit dem Computer verbunden wurde,
kann über das Dropdown Menü in der Kopfzeile der richtige COM Port ausgewählt werden.
Wurde der korrekte COM Port ausgewählt, wird durch ein Klick auf die Verbinden-Schaltfläche
eine Verbindung zur UEB aufgebaut. Eine erfolgreiche Verbindung wird durch ein grünes Element 
daneben signalisiert. 
UEB-Parameter einstellen:
Auf der Seite UEB Einstellungen können alle zu diesem Zeitpunkt änderbaren Parameter geändert werden.
Durch eine Druck auf "Einstellungen auf Controller schreiben" werden die vorgenommenen Einstellungen
an den Controller gesendet. Diese können zur schnelleren Einrichtung auch über "Einstellungen in
Datei speichern/laden" in eine Datei gespeichert werden.

Kommunikationseinstellungen / Messdaten einstellen:
Neben den Parametern des UEB können auch voreingestellte Daten des UEB an die GUI übertragen werden.
Jeder Übertragungsslot besitzt eine eindeutige ID (auf seiten des UEBs und der GUI). 
Mit dieser ID kann nun im UEB eine Datenübertragung angestoßen werden.
(z.B. ADC Daten von Spannung und Strom liegen unter ID = 228 ab)
Zum Startzeitpunkt der GUI werden immer die Standardübertragungsparameter geladen.
Diese lassen sich durch einen Klick auf "Konfigurationsfenster öffnen" anpassen.
Im Konfigurationsfenster befinden sich links die verfügbaren und rechts die ausgewählten IDs.
Durch das Setzen eines Hakens im Feld ganz links, kann diese ID vorgemerkt werden.
Ist zu diesem Zeitpunkt bekannt wie die Daten hinter dieser ID aussehen (Array aus uint8_t),
kann dies im jeweiligen Drop-Down-Menü der ID eingestellt werden.
Im Teil CSV-Text kann der Spalte in der Datei ein Name zugewiesen werden.
Handelt es sich bei den Daten um einen String, so kann dieser mit einer Eingabe des gewünschten
Trennzeichens (Leerzeichen, Komma, Semikolon,...) an dieser Stelle aufgespalten werden und 
in der Datei dementsprechend abgespeichert werden.
Wurden alle IDs wie gewünscht konfiguriert, so wird durch ein Klick auf den Pfeil in der Mitte
alles in den Bereich "Übertragene IDs" übernommen. 
Mit "OK" werden die Einstellungen übernommen und in "UEB Übertragungseinstellungen" angezeigt.

Messung starten / Daten speichern
Wurden alle Einstellungen den Wünschen angepasst, kann über "Messung starten" auf der Seite
"UEB Einstellungen" eine Messung angestoßen werden.
ACHTUNG! Diese Messung startet NICHT den Motor.
Damit der angeschlossene Motor gestartet werden kann, muss auf der Seite "UEB Status" die Schaltfläche
"Motor Start" gedrückt werden. Dies startet den Motor!
Um den Motor zu stoppen, muss "Motor STOP" gedrückt werden.
Wird ein Haken bei "Messung bei Motorstart starten" gesetzt, so erscheint ein Dialogfenster mit dem Aufruf
den Platz für die übertragenen Dateien zu definieren.
Ist kein Speicherort vorhanden so werden die Dateien auf dem Desktop abgelegt.
Mit "Messung starten" kann eine Messung auch während des Motorbetriebs durchgeführt werden.

Terminal
Im Terminal wird ein Großteil der Kommunikation zwischen UEB und GUI angezeigt.
Am unternen Fensterrand befindet sich eine Zeile. Mit dieser können eigene Handeingaben an die UEB gesendet
werden. Bei falschen Eingaben wird im Kommandofenster (schwarzes Fenster) ein Error ausgegeben.


Viel Spaß!



Version v1.0-v1.3 programmiert von
Pascal Kirchhoff und Marc Wechselberger
THU den 22.01.2023
GitHub: https://github.com/D0kRay/UEB_GUI_PyQt