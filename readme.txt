*******************************Hilfe, wie funktioniert nun diese GUI!*******************************

Verbindungsaufbau:
Nachdem der USB Anschluss der universalen Brueckenschaltung (UEB) mit dem Computer verbunden wurde,
kann ueber das Dropdown Menue in der Kopfzeile der richtige COM Port ausgewaehlt werden.
Wurde der korrekte COM Port ausgewaehlt, wird durch ein Klick auf die Verbinden-Schaltflaeche
eine Verbindung zur UEB aufgebaut. Eine erfolgreiche Verbindung wird durch ein gruenes Element daneben signalisiert.

UEB-Parameter einstellen:
Auf der Seite UEB Einstellungen koennen alle zu diesem Zeitpunkt aenderbaren Parameter geaendert werden.
Durch eine Druck auf "Einstellungen auf Controller schreiben" werden die vorgenommenen Einstellungen
an den Controller gesendet. Diese koennen zur schnelleren Einrichtung auch ueber "Einstellungen in
Datei speichern/laden" in eine Datei gespeichert werden.

Kommunikationseinstellungen / Messdaten einstellen:
Neben den Parametern des UEB koennen auch voreingestellte Daten des UEB an die GUI uebertragen werden.
Jeder uebertragungsslot besitzt eine eindeutige ID (auf seiten des UEBs und der GUI). 
Mit dieser ID kann nun im UEB eine Datenuebertragung angestossen werden.
(z.B. ADC Daten von Spannung und Strom liegen unter ID = 228 ab)
Zum Startzeitpunkt der GUI werden immer die Standarduebertragungsparameter geladen.
Diese lassen sich durch einen Klick auf "Konfigurationsfenster oeffnen" anpassen.
Im Konfigurationsfenster befinden sich links die verfuegbaren und rechts die ausgewaehlten IDs.
Durch das Setzen eines Hakens im Feld ganz links, kann diese ID vorgemerkt werden.
Ist zu diesem Zeitpunkt bekannt wie die Daten hinter dieser ID aussehen (Array aus uint8_t),
kann dies im jeweiligen Drop-Down-Menue der ID eingestellt werden.
Im Teil CSV-Text kann der Spalte in der Datei ein Name zugewiesen werden.
Handelt es sich bei den Daten um einen String, so kann dieser mit einer Eingabe des gewuenschten
Trennzeichens (Leerzeichen, Komma, Semikolon,...) an dieser Stelle aufgespalten werden und 
in der Datei dementsprechend abgespeichert werden.
Wurden alle IDs wie gewuenscht konfiguriert, so wird durch ein Klick auf den Pfeil in der Mitte
alles in den Bereich "uebertragene IDs" uebernommen. 
Mit "OK" werden die Einstellungen uebernommen und in "UEB uebertragungseinstellungen" angezeigt.

Messung starten / Daten speichern:
Wurden alle Einstellungen den Wuenschen angepasst, kann ueber "Messung starten" auf der Seite
"UEB Einstellungen" eine Messung angestossen werden.
ACHTUNG! Diese Messung startet NICHT den Motor.
Damit der angeschlossene Motor gestartet werden kann, muss auf der Seite "UEB Status" die Schaltflaeche
"Motor Start" gedrueckt werden. Dies startet den Motor!
Um den Motor zu stoppen, muss "Motor STOP" gedrueckt werden.
Wird ein Haken bei "Messung bei Motorstart starten" gesetzt, so erscheint ein Dialogfenster mit dem Aufruf
den Platz fuer die uebertragenen Dateien zu definieren.
Ist kein Speicherort vorhanden so werden die Dateien auf dem Desktop abgelegt.
Mit "Messung starten" kann eine Messung auch waehrend des Motorbetriebs durchgefuehrt werden.

Terminal:
Im Terminal wird ein Grossteil der Kommunikation zwischen UEB und GUI angezeigt.
Am unternen Fensterrand befindet sich eine Zeile. Mit dieser koennen eigene Handeingaben an die UEB gesendet
werden. Bei falschen Eingaben wird im Kommandofenster (schwarzes Fenster) ein Error ausgegeben.


Viel Spass!



Version v1.0-v1.3 programmiert von
Pascal Kirchhoff und Marc Wechselberger
THU den 22.01.2023
GitHub: https://github.com/D0kRay/UEB_GUI_PyQt