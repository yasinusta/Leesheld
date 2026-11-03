# Testresultaten — 3 november 2026

Getest op deze Mac met Python 3.12.2, Piper 1.4.2 en Playwright 1.64.1 / WebKit 27.2 (build 2370). Browserinstelling: iPad-achtig scherm van 820 × 1180, aanraakbediening, mobiel profiel. Dat is een echte WebKit-testbrowser op macOS, geen fysieke iPad of Safari-app op iPadOS.

## Geslaagd

- Complete dekking: 140 werkbladwoorden, vijf verhalen, vijf leesklanken, vier gesproken ABCD-labels. Alle 154 WAV-bestanden bestaan, zijn mono PCM 16-bit / 22.050 Hz, hebben een niet-lege golfvorm zonder volle-schaalclipping en kloppen met het auditbestand en de SHA-256-hashes. Totale audiogrootte circa 13,4 MB.
- Vastgelegde modelbestanden gecontroleerd tegen hun SHA-256-hashes. Regeneratie hergebruikt ongewijzigde, gecontroleerde bestanden. De gewijzigde zoemklank in het ijsverhaal is opnieuw gegenereerd.
- JavaScript- en Python-syntax, startscript-syntax en Git-wijzigingscontrole geslaagd.
- **17 browsercontroles** geslaagd: offline-dienst vanuit de bestaande submap; echte audio na tik; alle vier optielabels en woorden op volgorde; uitsluitend A–D in de zichtbare knoppen en neutrale toegankelijkheidslabels; eerste tik luistert, tweede bevestigt; geen woordhulp, sterren, juistheidskleur of antwoordfeedback tijdens de toets; volledige afspeellijst geannuleerd bij teruggaan naar het menu; onvolledige offline-download toont een fout; hervatten via wifi levert alle 154 geverifieerde bestanden; alle bestanden vervolgens offline gedecodeerd; correct afhandelen van begin-, open en achterwaartse bytebereiken en ongeldige bereiken; afspelen na offline herladen; foutmelding bij ontbrekende audio zonder vervangende apparaatstem; geen ongevangen JavaScript-fouten; offline heropenen na volledig sluiten van de browser.
- **Migratiecontrole** geslaagd: oorspronkelijke app uit commit `d818b586af3703e1aa25becf1ac29b2a6f2865bb` eerst echt offline geïnstalleerd; daarna bijgewerkt naar deze versie. Oude v2-cache opgeruimd, nieuwe app offline geopend, voortgang met 42 sterren behouden.
- Startscherm op iPad-formaat visueel geïnspecteerd.

## Nog handmatig controleren

- Geluid en vliegtuigmodus op de eigen fysieke iPad, zowel Safari als de beginscherm-app. Ook volume/stille modus, schermvergrendeling en de geïnstalleerde iPadOS-versie kunnen verschil maken.
- Luisterbeoordeling door een Nederlandstalige leerkracht: vooral de korte /d/, ademklank /h/, /z/, /u/ en /ɛɪ/. Foneeminvoer is gecontroleerd; de gerealiseerde uitspraak en ervaren natuurlijkheid zijn niet onafhankelijk op gehoor goedgekeurd.
- Werkelijk opslagtekort en langdurige verwijdering van websitegegevens door iPadOS zijn niet nagebootst. Foutafhandeling is aanwezig; blijvende offline-opslag kan niet worden gegarandeerd.

Publicatie naar GitHub en het online adres zijn afzonderlijke stappen. Dit rapport bewijst de lokale integratie; zie het meegeleverde overdrachtsbestand voor de publicatiestatus.
