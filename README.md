# CutTrack

Ett Python-verktyg för att logga vikt, kalorier, protein, steg och träning under en deff (viktnedgång med fokus på att behålla muskelmassa), och få regelbaserade råd baserat på loggarna.

## Mål
Många som deffar har svårt att skilja en verklig trend från vanliga dagliga svängningar, och att veta om protein, steg och träning faktiskt ligger på rätt nivå för att nå målet utan att tappa muskelmassa. Jag har löst det manuellt tidigare, med klipp och klistra i kalkylark. CutTrack är ett första steg mot att göra det till ett program, öppet för fler än en användare.

Kopplingen till AI-utvecklarrollen: projektet innehåller ingen AI, men bygger på samma grundarbete som all AI-utveckling börjar med, att samla in, strukturera och analysera data på ett sätt som går att bygga vidare på. Insamling, rengöring och regelbaserad analys av användardata är precis det steg som föregår ett maskininlärningsprojekt.

## Metod
Programmet är byggt kring tre klasser: `DailyLog` för en enskild dagslogg, `User` som basklass för en användare, och `CutProfile` som ärver från `User` och lägger till mål (målvikt, proteinmål, stegmål, träningsmål). `CutProfile(User)` med `super().__init__()` är projektets exempel på arv.

Regelbaserade råd byggs i `check_goals()`, som jämför senaste veckans snitt mot användarens egna mål på fyra områden: vikttrend, protein, steg och träningsfrekvens.

Koden är uppdelad i tre filer:
- `models.py`: klasserna
- `analysis.py`: filhantering och diagram (spara/läsa profil som JSON, exportera/importera loggar som CSV, rita viktdiagram med matplotlib)
- `cuttrack_minimal.ipynb`: den interaktiva menyn (`input()`-baserad) och alla test- och democeller

Felhantering är uppdelad per feltyp istället för ett generellt except: `load_profile` har tre skilda except-block (fil saknas, trasig JSON, saknat fält), `import_logs_csv` hoppar över en trasig CSV-rad i taget utan att stoppa hela importen, och filskrivning fångar `OSError` separat.

Standardbibliotek: `json`, `csv`, `os`, `datetime`, `random` (för testdata). Externt bibliotek: `matplotlib`.

Extern data hämtas genom CSV-inläsning (`import_logs_csv`), som uppfyller kravet på extern data utan att kräva ett externt API.

Den interaktiva delen (`create_profile`, `log_today`, `run_menu`) är testad genom att `input()` byts ut mot en lista med förberedda svar med `unittest.mock.patch`, så att hela menyflödet kan köras och verifieras utan att någon sitter och skriver in svar manuellt varje gång notebooken körs.

## Resultat
Testkörning med fjorton genererade loggar för en exempelanvändare, Testperson, gav:

```
Testperson har nu 14 loggar.
- Vikten har gått ner 0.9 kg de senaste 7 loggarna. Rätt riktning.
- Proteinmålet nås inte: snitt 159.3 g mot mål 161.5 g.
- Stegmålet nås: snitt 8332 steg mot mål 8000.
- Träningsmålet nås: 4 pass mot mål 3.
```

Profilen sparades som `testperson_profile.json`, loggarna exporterades som `testperson_logs.csv`, och ett viktdiagram med målvikten inritad sparades som `testperson_weight_chart.png`.

Den simulerade menykörningen (skapa profil, logga en dag, visa analys, visa diagram, spara och avsluta) gick igenom utan fel, vilket visar att den interaktiva delen fungerar, inte bara klasserna och beräkningarna.

## Analys
Projektet visar hur användardata kan samlas in strukturerat (klasser med validering redan vid inmatning), sparas på två format beroende på syfte (JSON för hela profilen, CSV för loggarna som ska kunna öppnas och granskas separat), och analyseras med enkla regler. Det är precis det arbetsflödet som ligger till grund för AI-utveckling: innan en modell kan tränas på data måste datan samlas in konsekvent och struktureras på ett sätt som går att lita på. En framtida version av CutTrack skulle kunna byta ut de regelbaserade råden i `check_goals()` mot en modell tränad på loggad data från många användare, utan att behöva ändra hur datan samlas in.

Branschmässigt är det här också representativt för hur mycket AI-utvecklarrollen i praktiken handlar om datahantering och verktygsbyggande snarare än att träna modeller från grunden, särskilt i tidiga skeden av ett projekt eller en karriär.

## Certifikat
Ett naturligt första certifikat efter den här kursen är **AI-901, Microsoft Azure AI Fundamentals**. Det är Microsofts nybörjarcertifiering för AI på Azure, ingen förkunskap krävs. Notera att AI-901 ersatte det tidigare AI-900 den 30 juni 2026, det gamla provet går inte längre att boka. Skillnaden är att AI-901 lutar mer åt praktisk implementation, med Python, REST-API:er, SDK:er och Microsoft Foundry, jämfört med AI-900 som mest var konceptuellt. Det passar bra ihop med den här kursen, eftersom AI-901 faktiskt förutsätter grundläggande Python-kunskap, vilket den här kursen ger. Kostnad omkring 99 USD, prissatt per land.

Ett rimligt nästa steg efter det är **AI-103, Azure AI Apps and Agents Developer Associate**, som ersatte det tidigare AI-102 samma datum. Den kräver mer utvecklingserfarenhet och fokuserar på att bygga AI-appar och agenter i Azure, snarare än bara att beskriva vad tjänsterna gör. Kostnad omkring 165 USD.

Ingen av de här är tagen ännu, det här är en kort redogörelse för vad som är relevant, inte en bekräftelse på avklarad certifiering.

## Reflektion
Det jag uppskattade mest var arbetssättet. Jag planerade och skissade lösningen innan jag började skriva kod, byggde en del i taget och testade varje funktion innan jag gick vidare. Det gjorde projektet lättare att förstå och minskade risken för att fel skulle följa med till senare delar. Jag fick också bättre kontroll över koden än om jag hade försökt bygga hela notebooken på en gång.

Jag byggde också först en mer avancerad version av projektet, med bland annat kaloriberäkning baserad på Mifflin-St Jeor-formeln, ett kalorigolv och en bedömning av viktnedgångens takt. Efter att ha jämfört den planen mot vad examinationen faktiskt kräver valde jag att skala ner till den version som lämnas in här, för att öka säkerheten i leveransen. Den fulla koden hade blivit betydligt mer omfattande, och med tiden jag hade kvar kändes det säkrare att leverera en mindre, komplett och testad version än att riskera att inte hinna färdigställa och verifiera allt i den ursprungliga planen. Arbetet är inte bortkastat, jag tänker bygga vidare på den mer avancerade planen efter kursen, så tiden jag lade på att tänka igenom kaloriberäkningen och taktbedömningen kommer till nytta även om den inte syns i den här inlämningen.

Den största tekniska utmaningen var att förstå hur central metoden `get_logs` är för resten av `User`-klassen, inte att skriva den. Den använder bara enkel listindexering (`logs[-days:]`) för att välja de senaste loggade posterna, men nästan alla andra metoder, medelvikt, medelprotein, medelsteg, viktförändring och träningsfrekvens, bygger vidare på exakt det den returnerar. Ett missförstånd om vad `get_logs` faktiskt gav tillbaka hade alltså spridit sig till varje beräkning i klassen. Jag övervägde att istället räkna bakåt utifrån kalenderdatum, så att metoden hoppar över dagar som saknar logg istället för att bara räkna rader i listan, men valde bort det eftersom det kräver att jämföra datumobjekt, en typ av logik jag inte behövde för att lösa uppgiften. När jag väl förstod hur `get_logs` fungerade blev resten av klassen mycket lättare att följa, och jag såg fördelen med att samla filtreringen på ett ställe istället för att upprepa samma logik i flera metoder.

Om jag gjorde om projektet skulle jag bestämma fil- och mappstrukturen redan från början. Under arbetet skapades dubbla mappar och vissa filer hamnade både i docs och i projektroten. Det kostade en hel kväll att reda ut och gjorde det svårare att veta vilken version som var aktuell. Nästa gång skulle jag tidigt skilja på exempelvis kod, data, dokumentation och tester. Den viktigaste lärdomen är därför att en tydlig struktur runt koden är lika viktig som att själva koden fungerar.

CutTrack visar även skillnaden mellan regelbaserad programmering och maskininlärning. I den nuvarande versionen har jag själv bestämt reglerna, bland annat sjudagarsfönstret och hur proteinmålet beräknas mot målvikten. Metoden `check_goals` jämför användarens resultat mot dessa fasta gränser och ger återkoppling utifrån dem.

Vid en framtida vidareutveckling skulle stora delar av den befintliga lösningen kunna återanvändas. Klasserna, valideringen, filhanteringen och datainsamlingen fyller samma funktion även om bedömningen görs med maskininlärning. Däremot skulle ytterligare delar behövas för att förbereda data, träna och utvärdera en modell samt använda modellens resultat i programmet. `check_goals` skulle då kunna basera sin återkoppling på modellens förutsägelse i stället för enbart på mina fasta regler.

Projektet har därmed gjort kopplingen till AI-utveckling konkret för mig. En modell kan inte ge tillförlitliga bedömningar utan tillräcklig och välstrukturerad data. CutTrack bygger inte en sådan modell, men skapar det dataflöde som en framtida AI-lösning skulle vara beroende av.

## AI-användning
Jag har använt Claude (Anthropic) som bollplank och studiecoach genom hela projektet. Idén, produktvisionen och de bärande besluten är mina: vad programmet ska logga, vilka råd det ska ge, att skala ner till en enklare version för att hinna leverera något komplett, och att koden ska hållas på en nivå jag kan förklara muntligt.

Jag har byggt upp projektet steg för steg i repot, kört och testat varje del på min egen dator, felsökt det som gick fel och skrivit om förslag som inte stämde med vad jag ville. AI:n har jag använt som understöd under hela processen som vi bearbetat tillsammans. Vi har därefter gått igenom koden funktion för funktion. 

Ingen riktig användardata har skickats till AI-verktyget, all testdata är påhittad.

## Installation
1. Se till att `models.py`, `analysis.py` och `cuttrack_minimal.ipynb` ligger i samma mapp
2. Skapa en virtuell miljö och installera beroenden:
   ```
   python3 -m venv .venv
   .venv/bin/Activate.ps1        # Mac/Linux. På Windows: .venv\Scripts\Activate.ps1
   python3 -m pip install matplotlib
   ```
3. Öppna `cuttrack_minimal.ipynb` i Jupyter Notebook, VS Code eller Google Colab, och välj `.venv` som kernel
4. Kör cellerna i ordning. Testcellen med `unittest.mock.patch` kör automatiskt, resten kan köras interaktivt genom att anropa `run_menu(profile)` med en egen profil

## GitHub-länk
https://github.com/NiklasEkeskar/cuttrack_minimal
