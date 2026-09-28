# Kommentarerna i den här filen förklarar varje ny konstruktion första
# gången den används.

# import hämtar in färdig kod från en modul så att vi kan använda den.
# datetime kommer från Pythons standardbibliotek och hanterar datum och tid.
# Vi behöver den för att hämta dagens datum i User-klassen.
from datetime import datetime


# class skapar en klass, en ritning för hur ett objekt ska se ut.
# Varje DailyLog-objekt blir en enskild dags logg.
class DailyLog:
    """En daglig logg med vikt, kalorier, protein, steg och träning."""

    # __init__ körs automatiskt varje gång ett nytt objekt skapas.
    # self är objektet självt. De andra namnen (date, weight och så vidare)
    # är värdena som skickas in när objektet skapas.
    def __init__(self, date, weight, calories, protein, steps, trained):
        # Validering sker här, i __init__, så att ett orimligt värde stoppas
        # så tidigt som möjligt, innan det hinner spridas vidare till någon
        # beräkning. Den som skapar en DailyLog (import_logs_csv, log_today)
        # fångar felet med try/except.
        #
        # if kollar ett villkor. or betyder att villkoret är sant om minst
        # en av de två delarna är sant. <= betyder mindre än eller lika med.
        if weight <= 0 or weight > 400:
            # raise ValueError(...) stoppar programmet med ett felmeddelande.
            # Om ingen fångar felet med try/except kraschar programmet.
            # f"...{weight}" är en f-sträng: värdet inom { } sätts in i texten.
            raise ValueError(f"Orimligt vikt-värde: {weight}")
        if calories < 0 or calories > 10000:
            raise ValueError(f"Orimligt kalori-värde: {calories}")

        # self.date = date sparar värdet på objektet som ett attribut, så att
        # det finns kvar efter att __init__ är klar och kan läsas senare
        # med till exempel log.date.
        self.date = date
        self.weight = weight
        self.calories = calories
        self.protein = protein
        self.steps = steps
        self.trained = trained


# User är en basklass: den innehåller det som gäller alla användare.
# CutProfile längre ner ärver från den.
class User:
    """Bas-klass för en användare som loggar sin data."""

    def __init__(self, name, height_cm, age, sex, start_weight):
        self.name = name
        self.height_cm = height_cm
        self.age = age
        self.sex = sex
        self.start_weight = start_weight
        # datetime.now() ger nuvarande tidpunkt. .strftime("%Y-%m-%d")
        # gör om den till text i formatet år-månad-dag, till exempel
        # 2026-09-28. %Y är år, %m är månad och %d är dag.
        self.created_date = datetime.now().strftime("%Y-%m-%d")
        # [] är en tom lista. Här samlas alla användarens DailyLog-objekt.
        self.logs = []

    def add_log(self, log):
        # .append() lägger till ett element sist i en lista.
        self.logs.append(log)

    def get_logs(self, days):
        """Ger de senaste 'days' loggade posterna (inte kalenderdagar)."""
        # len(x) ger antalet element i listan x.
        # >= betyder större än eller lika med.
        # return skickar tillbaka ett värde till den som anropade metoden
        # och avslutar metoden.
        #
        # logs[-days:] plockar de sista "days" elementen i listan, oavsett
        # vilka datum de faktiskt har. Ett negativt tal i hakparentes
        # räknar från slutet av listan. Om användaren missat att logga en dag
        # räknas alltså inte det som ett hål, listan glider bara ett steg
        # längre bak i tiden. En kalenderbaserad version hade behövt jämföra
        # riktiga datumobjekt istället, mer kod för samma sak.
        if days >= len(self.logs):
            return self.logs
        return self.logs[-days:]

    def average_weight(self, days):
        # Alla average_-metoder följer samma mönster: hämta rätt loggar,
        # kolla att listan inte är tom (annars division med noll), summera
        # för hand i en loop, dela på antalet. Ingen statistics.mean(),
        # för att hela uträkningen ska synas i klartext.
        logs = self.get_logs(days)
        # == jämför två värden (ett enkelt = tilldelar ett värde).
        if len(logs) == 0:
            # None betyder "inget värde". Returneras när det inte finns
            # någon data att räkna på.
            return None
        # total = 0 skapar en summa som vi bygger på i loopen.
        total = 0
        # for-loop: går igenom listan ett element i taget. log är det
        # element loopen är på just nu.
        for log in logs:
            # log.weight hämtar attributet weight från loggen.
            total = total + log.weight
        # round(x, 1) avrundar talet x till 1 decimal.
        # / är vanlig division och ger ett decimaltal.
        return round(total / len(logs), 1)

    def average_protein(self, days):
        # Samma mönster som average_weight, se förklaringen där.
        logs = self.get_logs(days)
        if len(logs) == 0:
            return None
        total = 0
        for log in logs:
            total = total + log.protein
        return round(total / len(logs), 1)

    def average_steps(self, days):
        # Samma mönster som average_weight. round(x) utan andra argument
        # avrundar till ett heltal, vilket passar för steg.
        logs = self.get_logs(days)
        if len(logs) == 0:
            return None
        total = 0
        for log in logs:
            total = total + log.steps
        return round(total / len(logs))

    def weight_change(self, days):
        # Kräver minst två loggar, annars finns det inget att jämföra mot,
        # en enda vikt kan inte visa en förändring. logs[-1] är senaste
        # loggen (index -1 räknar från slutet), logs[0] är den äldsta
        # inom fönstret (index 0 är första elementet).
        logs = self.get_logs(days)
        # < betyder mindre än.
        if len(logs) < 2:
            return None
        return round(logs[-1].weight - logs[0].weight, 1)

    def training_days(self, days):
        # Skillnad mot metoderna ovan: här returneras 0, inte None, när
        # listan är tom. Noll träningspass är ett giltigt, korrekt svar,
        # till skillnad från ett medelvärde som inte går att räkna ut alls
        # utan data.
        logs = self.get_logs(days)
        count = 0
        for log in logs:
            # log.trained är True eller False, så if log.trained: räcker
            # (det behövs ingen jämförelse med == True).
            if log.trained:
                count = count + 1
        return count


# CutProfile(User): parentesen betyder att CutProfile ärver från User.
# Klassen får alla Users metoder och lägger till egna mål.
class CutProfile(User):
    """Barnklass som lägger till mål ovanpå User."""

    # protein_goal_per_kg=1.9, step_goal=8000 och training_goal_days=3 är
    # standardvärden: skickas inget värde in används värdet efter tecknet =.
    def __init__(self, name, height_cm, age, sex, start_weight, goal_weight,
                 protein_goal_per_kg=1.9, step_goal=8000, training_goal_days=3):
        # super().__init__() måste anropas innan CutProfile sätter sina egna
        # attribut. Det är den raden som faktiskt sätter self.name,
        # self.logs och så vidare, class CutProfile(User) i sig ger bara
        # tillgång till Users metoder, inte till att attributen redan finns.
        super().__init__(name, height_cm, age, sex, start_weight)

        if goal_weight >= start_weight:
            raise ValueError("Målvikten måste vara lägre än startvikten.")

        self.goal_weight = goal_weight
        self.protein_goal_per_kg = protein_goal_per_kg
        self.step_goal = step_goal
        self.training_goal_days = training_goal_days

    def protein_goal(self):
        # Räknas mot goal_weight (målvikten), inte mot aktuell vikt, så att
        # målet ligger stilla genom hela deffen. Räknade vi mot aktuell vikt
        # skulle proteinmålet sjunka i takt med kroppsvikten, fel riktning
        # när syftet är att bevara muskelmassa.
        # * är multiplikation.
        return round(self.protein_goal_per_kg * self.goal_weight, 1)

    def check_goals(self, days=7):
        """Regelbaserade råd. Jämför snitt mot mål, ingen fysiologisk beräkning."""
        # days=7 är ett standardvärde: anropas metoden utan argument
        # används 7.
        # Fyra oberoende kontroller, ingen inbördes prioritering. Var och en
        # bygger en textrad och lägger den i messages, som returneras som
        # en lista sist i metoden.
        messages = []

        # 1. Vikttrend: bara riktningen (upp/ner/still) räknas, ingen procent.
        change = self.weight_change(days)
        # is None kollar om ett värde är None. Vi använder is och inte ==
        # för None.
        if change is None:
            messages.append("Inte tillräckligt med loggar för att bedöma vikttrenden.")
        # elif betyder "annars om": kollas bara om if-villkoret ovan var falskt.
        elif change < 0:
            # abs() ger absolutvärdet, alltså talet utan minustecken. Vikten
            # har gått ner om change är negativt, men i texten vill vi skriva
            # 0.9 och inte -0.9.
            messages.append(f"Vikten har gått ner {abs(change)} kg de senaste {days} loggarna. Rätt riktning.")
        elif change == 0:
            messages.append("Vikten står still. Se över kaloriintaget om målet är nedgång.")
        else:
            messages.append(f"Vikten har gått upp {change} kg de senaste {days} loggarna.")

        # 2. Protein: snitt mot protein_goal(), som är räknat mot målvikten.
        avg_protein = self.average_protein(days)
        goal_protein = self.protein_goal()
        if avg_protein is None:
            messages.append("Inga loggar för protein än.")
        elif avg_protein >= goal_protein:
            messages.append(f"Proteinmålet nås: snitt {avg_protein} g mot mål {goal_protein} g.")
        else:
            messages.append(f"Proteinmålet nås inte: snitt {avg_protein} g mot mål {goal_protein} g.")

        # 3. Steg: snitt mot ett fast stegmål.
        avg_steps = self.average_steps(days)
        if avg_steps is None:
            messages.append("Inga loggar för steg än.")
        elif avg_steps >= self.step_goal:
            messages.append(f"Stegmålet nås: snitt {avg_steps} steg mot mål {self.step_goal}.")
        else:
            messages.append(f"Stegmålet nås inte: snitt {avg_steps} steg mot mål {self.step_goal}.")

        # 4. Träning: antal loggade pass mot ett fast mål, ingen procent.
        days_trained = self.training_days(days)
        if days_trained >= self.training_goal_days:
            messages.append(f"Träningsmålet nås: {days_trained} pass mot mål {self.training_goal_days}.")
        else:
            messages.append(f"Träningsmålet nås inte: {days_trained} pass mot mål {self.training_goal_days}.")

        return messages
