# Audio: bron, licentie en uitspraak

De bestanden in `audio/` zijn op 3 november 2026 lokaal gegenereerd met Piper 1.4.2 en de Nederlandse stem `nl_NL-pim-medium`. Er is geen betaalde spraakdienst of API-sleutel nodig. De app verstuurt geen stemopnames van kinderen.

## Herkomst en hergebruik

- Dataset: Pim, OHF-Voice / Nabu Casa Voice Datasets. De dataset is beschikbaar onder **CC0 1.0**: https://github.com/OHF-Voice/voice-datasets/tree/master/nl_NL/pim
- Modelkaart vermeldt datasetlicentie CC0: https://huggingface.co/rhasspy/piper-voices/blob/e7229f7d33a10e145e109b886d661984201ac3c4/nl/nl_NL/pim/medium/MODEL_CARD
- Een kopie van die kaart staat in `PIM_MODEL_CARD.txt`. `voice-lock.json` bevat de modelversie en SHA-256-controlesommen. Het model is niet in de uploadbundel opgenomen.
- De nieuw gegenereerde audiogolven worden voor zover daarop nieuwe rechten ontstaan beschikbaar gesteld onder CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/ . Dit verandert geen eventuele bestaande rechten op de oorspronkelijke werkbladteksten en verhalen in deze repository.
- De apart geïnstalleerde Piper-software heeft licentie GPL-3.0: https://github.com/OHF-Voice/piper1-gpl . De app bevat geen Piper-programma of model; de iPad speelt uitsluitend vooraf gemaakte WAV-bestanden af.

## Uitspraakkeuzes

140 losse woorden: spreekduur ingesteld op 1,35 maal de standaardduur, oorspronkelijke toonhoogte. Vijf verhalen: 1,25 maal de standaardduur, met 320 ms extra stilte na iedere regel. Vier neutrale labels: “Optie A”, “Optie B”, “Optie C”, “Optie D”. Alle vier opties gebruiken exact dezelfde woordopnames als de oefenwoorden; de juiste optie krijgt geen andere stem, toon of pauze.

De vijf leesklanken zijn rechtstreeks als fonemen aangeboden: d /d/, oe /u/, z /z/, ij /ɛɪ/, h /h/. Daardoor wordt de tekst niet omgezet in alfabetnamen “dee”, “zet”, “haa”. Een plofklank zoals /d/ wordt kort gehouden; er wordt geen extra klinker geschreven. De “mmmm” in het ijsverhaal is vervangen door een zoemklank /mː/, omdat de gewone tekstinvoer viermaal “em” opleverde.

`audio-audit.json` vermeldt per bestand de invoer, foneeminvoer, duur, bestandsgrootte en SHA-256. `audio-manifest.json` noemt uitsluitend de complete bundel. `audio-version.js` koppelt de offline-cache aan de bundelinhoud.

## Grenzen van de controle

De bestanden zijn echt gegenereerd; formaat, niet-lege golfvorm, dekking en afspeelbaarheid worden gecontroleerd. De foneeminvoer is geïnspecteerd. Een foneem als invoer garandeert niet dat een spraakmodel elke klank perfect realiseert. Er heeft hier geen onafhankelijke luisterbeoordeling door een Nederlandstalige leerkracht of logopedist plaatsgevonden. Luister voor gebruik met kinderen vooral d, h, z, oe en ij na. De app meet de uitspraak van het kind niet.
