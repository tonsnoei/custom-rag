# Chunking Methodologies

**1. Metadata toevoegen aan elke chunk**

De simpelste en meest gebruikte aanpak: je slaat bij elke chunk niet alleen de tekst op, maar ook metadata zoals de documenttitel, het hoofdstuk, en het pad van headers erboven (bijvoorbeeld "Artikel: Geschiedenis van Amsterdam > Hoofdstuk 3: Gouden Eeuw > Handel"). Bij retrieval geef je die metadata gewoon mee in de prompt naar het taalmodel, vóór de eigenlijke chunktekst. Zo weet het model bij het genereren van een antwoord altijd waar de chunk vandaan komt, ook al bevat de chunk zelf die context niet.

**2. Contextual prefixing (de chunk zelf verrijken)**

Een stap verder: je voegt die header-hiërarchie letterlijk toe aan het begin van de chunk-tekst zelf, vóór je hem omzet naar een vector. Dus niet alleen de paragraaf, maar "Dit fragment komt uit het hoofdstuk 'Gouden Eeuw' van het artikel 'Geschiedenis van Amsterdam'. [paragraaftekst]". Dit helpt zowel bij retrieval (de vector bevat nu ook signaal over het bredere onderwerp) als bij generatie.

**3. Overlapping chunks**

Chunks laten overlappen (bijvoorbeeld de laatste twee zinnen van chunk 1 herhalen als eerste zinnen van chunk 2) zodat een gedachte die over een chunk-grens heen loopt niet volledig wordt afgekapt. Lost het "missende grotere context"-probleem niet op, maar wel het "halve zin/gedachte"-probleem.

**4. Parent-child retrieval (ook wel "small-to-big")**

Een elegantere oplossing: je embedt kleine, precieze chunks (goed voor accurate retrieval), maar slaat ook op tot welk groter blok (bijvoorbeeld de hele sectie of het hele hoofdstuk) die chunk behoort. Bij een match haal je niet de kleine chunk op om naar het model te sturen, maar de bijbehorende grotere "parent"-chunk. Zo zoek je precies, maar geef je ruim context mee.

**5. Document-summary toevoegen**

Bij het indexeren laat je het LLM eerst een korte samenvatting van het hele document maken, en die samenvatting voeg je toe aan elke chunk uit dat document (of geef je apart mee in de prompt naast de gevonden chunks). Iets duurder om te bouwen, maar lost het "ik weet niet waar dit artikel over gaat"-probleem het meest fundamenteel op.
