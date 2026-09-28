# Kommentarerna i den här filen förklarar varje ny konstruktion första
# gången den används.

# import hämtar in färdig kod från en modul så att vi kan använda den.
# json är en modul i Pythons standardbibliotek för att läsa och skriva
# JSON-filer (text med nyckel och värde).
import json
# csv är en modul i standardbiblioteket för att läsa och skriva CSV-filer,
# alltså tabeller sparade som text med ett kommatecken mellan kolumnerna.
import csv
# os är en modul i standardbiblioteket för att prata med operativsystemet.
# Här används den bara för att kolla om en fil redan finns (os.path.exists).
import os
# matplotlib är ett externt bibliotek (installeras med pip) för att rita
# diagram. pyplot är den del som ritar. "as plt" ger den det korta namnet plt.
import matplotlib.pyplot as plt

# from models import ...: hämtar våra egna klasser från filen models.py.
from models import CutProfile, DailyLog


# def skapar en funktion. Värdena inom parentes (name, suffix) är parametrar,
# alltså det funktionen tar emot när den anropas.
def make_filename(name, suffix):
    """
    Bygger ett säkert filnamn från ett användarnamn. Användarens text
    går aldrig rakt in i ett filnamn, bara de tecken som är bokstäver
    eller siffror plockas ut, teckenvis i en loop.
    """
    # safe_chars = "" skapar en tom sträng (text) som vi bygger på med ett
    # tecken i taget.
    # for char in name: går igenom namnet tecken för tecken.
    # char.isalnum() är True för bokstäver och siffror, False för mellanslag,
    # bindestreck, snedstreck och liknande. Skriver användaren till
    # exempel "../hemligt" plockas bara "hemligt" ut, ingen del av
    # sökvägen kan smyga sig med.
    # char.lower() gör om tecknet till liten bokstav.
    # + mellan två strängar sätter ihop dem (safe_chars + "a" ger t.ex. "ta").
    safe_chars = ""
    for char in name:
        if char.isalnum():
            safe_chars = safe_chars + char.lower()

    # == jämför två värden (ett enkelt = tilldelar ett värde).
    if safe_chars == "":
        safe_chars = "user"

    # f"{safe_chars}_{suffix}" är en f-sträng: värdena inom { } sätts in i
    # texten. return skickar tillbaka resultatet till den som anropade.
    return f"{safe_chars}_{suffix}"


def save_profile(profile):
    """Sparar profilen som JSON. Filnamnet byggs från profilens namn."""
    filename = make_filename(profile.name, "profile.json")

    # Bygger dict:en manuellt, fält för fält, istället för profile.__dict__.
    # Det gör att logs (listan med DailyLog-objekt) aldrig hamnar i den här
    # filen av misstag, listan sparas separat via export_logs_csv, och det
    # gör exakt vilka fält som sparas synligt i klartext.
    # { } med "nyckel": värde-par är en dict (ordbok). Nycklarna, till exempel
    # "name", blir fältnamn i JSON-filen.
    data = {
        "name": profile.name,
        "height_cm": profile.height_cm,
        "age": profile.age,
        "sex": profile.sex,
        "start_weight": profile.start_weight,
        "goal_weight": profile.goal_weight,
        "protein_goal_per_kg": profile.protein_goal_per_kg,
        "step_goal": profile.step_goal,
        "training_goal_days": profile.training_goal_days,
        "created_date": profile.created_date,
    }

    # try/except: koden i try körs. Går något fel hoppar Python till except
    # istället för att krascha hela programmet.
    try:
        # open(filename, "w", encoding="utf-8") öppnar filen för skrivning
        # ("w" är write). Om filen redan finns skrivs den över.
        # encoding="utf-8" gör att å, ä och ö sparas rätt.
        # with ... as file: stänger filen automatiskt när blocket är klart,
        # även om något går fel.
        with open(filename, "w", encoding="utf-8") as file:
            # json.dump(data, file, ...) skriver dict:en till filen som JSON.
            # indent=2 gör filen läsbar med indrag.
            # ensure_ascii=False behåller å, ä och ö som de är.
            json.dump(data, file, indent=2, ensure_ascii=False)
        # print() skriver ut text i terminalen.
        print(f"Profilen sparad i {filename}")
    # OSError är felet som uppstår vid problem med filer, till exempel att
    # man saknar skrivrättighet. "as e" sparar felet i variabeln e så att vi
    # kan skriva ut det.
    except OSError as e:
        print(f"Kunde inte spara profilen: {e}")


def load_profile(name):
    """Läser in en profil baserat på namn. Filnamnet byggs på samma sätt som i save_profile."""
    filename = make_filename(name, "profile.json")

    try:
        # "r" är read: filen öppnas för läsning.
        with open(filename, "r", encoding="utf-8") as file:
            # json.load(file) läser JSON-filen och gör om den till en dict.
            data = json.load(file)

        # data["name"] hämtar värdet för nyckeln "name" ur dict:en. Saknas
        # nyckeln blir det ett KeyError, som fångas längre ner.
        profile = CutProfile(
            data["name"], data["height_cm"], data["age"], data["sex"],
            data["start_weight"], data["goal_weight"],
            data["protein_goal_per_kg"], data["step_goal"], data["training_goal_days"]
        )
        print(f"Profilen {profile.name} inläst från {filename}")
        return profile

    # Tre skilda except-block istället för ett generellt except Exception,
    # så att felmeddelandet till användaren kan vara specifikt om vad som
    # faktiskt gick fel:
    except FileNotFoundError:
        # Filen finns inte alls, t.ex. första gången ett namn används.
        # None betyder "inget värde". Funktionen returnerar None när ingen
        # profil kunde läsas in.
        print(f"Hittade ingen fil: {filename}")
        return None
    except json.JSONDecodeError:
        # Filen finns men innehållet är trasig JSON, t.ex. avbruten skrivning.
        print(f"Filen {filename} innehåller inte giltig JSON.")
        return None
    except KeyError as e:
        # Filen är giltig JSON men saknar ett fält CutProfile behöver.
        print(f"Ett fält saknas i filen: {e}")
        return None


def export_logs_csv(profile):
    """Sparar loggarna som CSV. Det här är datafilen som lämnas in vid examinationen."""
    filename = make_filename(profile.name, "logs.csv")

    # Bara en informativ utskrift till användaren, ingen funktionell
    # skillnad i vad som händer, open(..., "w") skriver över filen oavsett.
    # os.path.exists(filename) ger True om filen redan finns.
    if os.path.exists(filename):
        print(f"{filename} finns redan, skriver över.")
    else:
        print(f"Skapar ny fil: {filename}")

    try:
        # newline="" behövs för att csv-modulen inte ska lägga till extra
        # tomma rader i filen.
        with open(filename, "w", newline="", encoding="utf-8") as file:
            # csv.writer(file) skapar ett objekt som kan skriva rader till
            # CSV-filen.
            writer = csv.writer(file)
            # writer.writerow([...]) skriver en rad. Listan innehåller
            # kolumnerna. Första raden är rubrikerna.
            writer.writerow(["date", "weight", "calories", "protein", "steps", "trained"])
            # for-loop: en rad skrivs för varje logg i listan.
            for log in profile.logs:
                writer.writerow([log.date, log.weight, log.calories, log.protein, log.steps, log.trained])
        # len(profile.logs) ger antalet loggar i listan.
        print(f"Sparade {len(profile.logs)} loggar i {filename}")
    except OSError as e:
        print(f"Kunde inte spara loggarna: {e}")


def import_logs_csv(profile, filename):
    """
    Läser in loggar från en valfri CSV-fil. Skiljer sig från export_logs_csv
    genom att filnamnet kommer utifrån, inte från profilens namn.
    """
    # imported och skipped är räknare (heltal, int). imported = imported + 1
    # ökar räknaren med ett.
    imported = 0
    skipped = 0
    try:
        with open(filename, "r", encoding="utf-8") as file:
            # csv.DictReader läser filen en rad i taget och gör varje rad till
            # en dict där rubrikerna är nycklar. row["date"] ger alltså
            # datumet på den raden.
            reader = csv.DictReader(file)
            for row in reader:
                # try/except ligger inuti loopen, inte runt hela den. Det
                # betyder att EN trasig rad hoppas över (räknas i skipped)
                # utan att resten av filen struntas i. Ligger try/except
                # utanför loopen istället stoppar en enda dålig rad
                # importen helt.
                try:
                    # Allt i en CSV-fil är text. float("79.5") gör om text
                    # till decimaltal och int("8000") till heltal. Är texten
                    # inte ett tal kastas ValueError.
                    # row["trained"] == "True" jämför texten med "True" och
                    # ger ett riktigt True eller False.
                    log = DailyLog(
                        row["date"],
                        float(row["weight"]),
                        float(row["calories"]),
                        float(row["protein"]),
                        int(row["steps"]),
                        row["trained"] == "True"
                    )
                    profile.add_log(log)
                    imported = imported + 1
                # (ValueError, KeyError) är en tupel med två feltyper, så
                # except fångar båda. KeyError betyder att en kolumn saknas.
                except (ValueError, KeyError):
                    skipped = skipped + 1

        print(f"Importerade {imported} loggar, hoppade över {skipped} felaktiga rader.")
    except FileNotFoundError:
        print(f"Hittade ingen fil: {filename}")


def plot_weight(profile):
    """Ritar och sparar ett viktdiagram med målvikten inritad som en streckad linje."""
    filename = make_filename(profile.name, "weight_chart.png")

    # Två tomma listor som fylls i loopen: datum till x-axeln och vikter
    # till y-axeln. .append() lägger till ett element sist i en lista.
    dates = []
    weights = []
    for log in profile.logs:
        dates.append(log.date)
        weights.append(log.weight)

    # plt.figure(figsize=(8, 4)) skapar en ny bild, 8 tum bred och 4 tum hög.
    plt.figure(figsize=(8, 4))
    # plt.plot(x, y, ...) ritar en linje. marker="o" sätter en prick vid
    # varje punkt. label är namnet som visas i förklaringsrutan.
    plt.plot(dates, weights, marker="o", label="Vikt")
    # plt.axhline(y=...) ritar en vågrät linje vid ett y-värde, här
    # målvikten. linestyle="--" gör den streckad, color="gray" gör den grå.
    plt.axhline(y=profile.goal_weight, linestyle="--", color="gray", label="Målvikt")
    # title, xlabel och ylabel sätter rubrik och text på axlarna.
    plt.title(f"Viktutveckling för {profile.name}")
    plt.xlabel("Datum")
    plt.ylabel("Vikt (kg)")
    # plt.xticks(rotation=45) vrider datumtexterna 45 grader så att de
    # inte skriver över varandra.
    plt.xticks(rotation=45)
    # plt.legend() visar förklaringsrutan med label-texterna.
    plt.legend()
    # plt.tight_layout() justerar marginalerna så att inget klipps bort.
    plt.tight_layout()
    # savefig körs före show(): filen sparas till disk oavsett om
    # diagramfönstret sedan stängs utan att sparas manuellt.
    # plt.savefig(filename) sparar bilden som en fil, plt.show() visar den.
    plt.savefig(filename)
    plt.show()
    print(f"Diagrammet sparat som {filename}")
