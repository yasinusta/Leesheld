# Leesheld als gratis iPad-webapp

## 1. AI-audio op Mac genereren (eenmalig)
Open de uitgepakte map op je Mac en dubbelklik `Maak_AI_stem.command`. Dit vereist internet en Python 3. Piper downloadt de gratis Nederlandse mannenstem `nl_NL-pim-medium` en maakt WAV-bestanden in `audio/`. De stem is synthetisch; controleer de uitspraak van beginnende leesklanken. Als macOS het script blokkeert: open Terminal, ga naar de map en voer `bash Maak_AI_stem.command` uit.

**Zonder deze stap gebruikt de app tijdelijk de standaard iPad-spraakstem.** De ZIP bevat nog geen ingesproken AI-audio.

## 2. Gratis publiceren op GitHub Pages
1. Maak gratis een GitHub-account op github.com.
2. Maak een **public** repository `leesheld`.
3. Upload de **inhoud** van deze map (inclusief `audio`, `icons`, `index.html`, `sw.js`, `manifest.webmanifest`, `audio-manifest.json`) naar de hoofdmap van de repository.
4. Ga naar **Settings → Pages → Build and deployment → Deploy from a branch**, selecteer `main` en `/(root)`, klik **Save**.
5. Wacht tot GitHub de link toont: `https://GEBRUIKERSNAAM.github.io/leesheld/`. Je hoeft geen domein te kopen.

## 3. Installeren op iPad
1. Open die HTTPS-link in **Safari**.
2. Tik **Deel → Zet op beginscherm → Voeg toe**.
3. Open Leesheld vanaf het beginscherm.
4. Tik bij **Offline AI-geluid** op **Download alle stemmen** en wacht op de groene gereedmelding.
5. Test met vliegtuigmodus. Voortgang blijft lokaal op die iPad bewaard.

**Opmerking:** De eerste download kan groot zijn, zeker door WAV-verhaaltjes. Verwijder Safari-websitegegevens niet, want daarmee verdwijnen de offline cache en mogelijk de voortgang. De toets controleert luisterkeuzes, niet de echte uitspraak van het kind.
