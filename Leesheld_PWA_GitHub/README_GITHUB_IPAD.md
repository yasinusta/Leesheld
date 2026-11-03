# Leesheld met Nederlandse AI-audio

Deze versie bevat direct bruikbare audio: **154 WAV-bestanden, circa 13,4 MB**. Zelf genereren is niet nodig om de app te gebruiken.

## Gebruiken op de iPad

1. Open https://yasinusta.github.io/Leesheld/Leesheld_PWA_GitHub/ in Safari, zodra deze versie op GitHub staat.
2. Sluit een oude geopende versie en heropen de link via wifi. De app installeert de bijgewerkte offline-dienst; een bestaande pagina kan daarbij eenmaal herladen.
3. Tik op een leesklank of “Lees woord voor”. Geluid begint na een tik; het start nooit automatisch bij het openen van een toets.
4. Bij ABCD: de eerste tik speelt “Optie A/B/C/D” en het woord; de tweede tik op dezelfde letter bevestigt het antwoord. “Alle keuzes horen” speelt de vier labels en woorden op volgorde. De geschreven antwoorden staan niet in de knoppen of hun toegankelijkheidslabels.
5. Bij de toets zijn woordhulp en sterren verborgen. De app toont tijdens de toets alleen “Antwoord opgeslagen”, zonder groen/rood of de juiste keuze. De score verschijnt na afloop.
6. Kies **Deel → Zet op beginscherm** en open Leesheld vanaf het beginscherm. Tik daar op **Download alle stemmen** en houd de app open tot “154 audiobestanden offline beschikbaar” verschijnt. Safari en de beginscherm-app kunnen aparte opslag hebben: download in de omgeving die je gaat gebruiken.
7. Zet vliegtuigmodus aan, sluit Leesheld en open opnieuw. Test een leesklank, oefenwoord, ABCD en een verhaaltje.

Bij een onderbroken download: zet wifi aan en tik opnieuw. Reeds opgeslagen, gecontroleerde bestanden worden hergebruikt. Een gereedmelding verschijnt pas nadat alle 154 bestanden zijn gecontroleerd. Bij te weinig opslag verschijnt een foutmelding. Download na een audio-update opnieuw.

Bij ontbrekende audio meldt de app de fout. Er is bewust geen stille wissel naar een andere iPad-stem die de letters als alfabetnamen kan uitspreken.

Safari kan websitegegevens bij opslagtekort of langdurige inactiviteit verwijderen. De app vraagt waar ondersteund om blijvende opslag, maar kan die niet garanderen. Wis geen Safari-websitegegevens als je de offline-audio en voortgang wilt behouden. Zie https://webkit.org/blog/14403/updates-to-storage-policy/ .

## Bestaande GitHub-repository bijwerken

Behoud de map **Leesheld_PWA_GitHub/** in de hoofdmap van **yasinusta/Leesheld**. Zet de bestanden dus niet in een tweede, gelijknamige submap.

Met Git: kopieer de nieuwe map over de bestaande map in een actuele clone, controleer de wijzigingen, voeg die toe, commit en push naar `main`. Publiceer ook `audio/`, `audio-audit.json`, `audio-version.js`, `audio-player.js` en het nieuwe `sw.js`; alleen `index.html` vervangen is onvoldoende.

Via de website:

1. Pak de geleverde ZIP uit.
2. Open https://github.com/yasinusta/Leesheld en kies **Add file → Upload files** vanuit de hoofdmap.
3. GitHub staat maximaal 100 bestanden per upload toe (https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository). Gebruik daarom bij voorkeur de drie aparte uploadbundels naast de volledige ZIP. Pak elke bundel apart uit en sleep telkens de daarin opgenomen map **Leesheld_PWA_GitHub** naar het uploadvak in de hoofdmap. De ZIP zelf wordt niet door GitHub Pages uitgepakt.
4. Upload en commit achtereenvolgens **Upload_1_app.zip**, **Upload_2_audio.zip** en **Upload_3_audio.zip**. Elke bundel bevat minder dan 100 bestanden en behoudt het juiste submappad. Bestaande bestanden worden vervangen; bestanden uit eerdere bundels blijven staan. Controleer steeds dat het pad maar eenmaal `Leesheld_PWA_GitHub/` bevat. Tijdens de drie uploads is de update tijdelijk onvolledig; gebruik de app pas na de laatste geslaagde Pages-publicatie.
5. Wacht op een geslaagde **pages build and deployment** bij https://github.com/yasinusta/Leesheld/actions . De bestaande Pages-instelling blijft `main`, `/(root)`.
6. Open de app-link hierboven en controleer de iPad-stappen.

De originele ZIP in de repository is ook bijgewerkt zodat die niet meer de oude versie zonder audio bevat.

## Audio later opnieuw genereren (optioneel)

Op een Mac met Python 3.10 of nieuwer: dubbelklik `Maak_AI_stem.command`, of voer in deze map `bash Maak_AI_stem.command` uit. Dit installeert Piper 1.4.2 in een lokale virtuele omgeving en downloadt het vastgelegde model van circa 64 MB. De download wordt met SHA-256 gecontroleerd. Het script maakt ontbrekende of gewijzigde opnames en schrijft het manifest pas na een volledige generatie. Voor alles opnieuw genereren: `.piper-venv/bin/python make_audio.py --force`.

Upload `models/` en `.piper-venv/` niet naar GitHub. De iPad heeft ze niet nodig. Lees `AUDIO_LICENSE.md` voor de CC0-bron, uitspraakkeuzes en beperkingen. De generator leest de vijf werkbladen uit de bestaande app en faalt als die niet volledig gevonden worden.

## Technische controles opnieuw uitvoeren

Vanuit de repository: `python3 tests/check_audio.py`. Dit vereist alleen Python en controleert dekking, hashes, WAV-formaat, duren, pieken en foneeminvoer. Voor de echte browsercontrole: installeer `playwright==1.64.1`, voer `python3 -m playwright install webkit` uit, daarna `python3 tests/browser_check.py`. Deze test start zelf een lokale server en gebruikt een schoon browserprofiel. Resultaten komen in `test-results/`.
