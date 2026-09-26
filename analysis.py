import json
import csv
import os

from models import CutProfile, DailyLog


def make_filename(name, suffix):
    """
    Bygger ett säkert filnamn från ett användarnamn. Användarens text
    går aldrig rakt in i ett filnamn, bara de tecken som är bokstäver
    eller siffror plockas ut, teckenvis i en loop.
    """
    safe_chars = ""
    for char in name:
        if char.isalnum():
            safe_chars = safe_chars + char.lower()

    if safe_chars == "":
        safe_chars = "user"

    return f"{safe_chars}_{suffix}"


def save_profile(profile):
    """Sparar profilen som JSON. Filnamnet byggs från profilens namn."""
    filename = make_filename(profile.name, "profile.json")

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

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Profilen sparad i {filename}")
    except OSError as e:
        print(f"Kunde inte spara profilen: {e}")


def load_profile(name):
    """Läser in en profil baserat på namn. Filnamnet byggs på samma sätt som i save_profile."""
    filename = make_filename(name, "profile.json")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        profile = CutProfile(
            data["name"], data["height_cm"], data["age"], data["sex"],
            data["start_weight"], data["goal_weight"],
            data["protein_goal_per_kg"], data["step_goal"], data["training_goal_days"]
        )
        print(f"Profilen {profile.name} inläst från {filename}")
        return profile

    except FileNotFoundError:
        print(f"Hittade ingen fil: {filename}")
        return None
    except json.JSONDecodeError:
        print(f"Filen {filename} innehåller inte giltig JSON.")
        return None
    except KeyError as e:
        print(f"Ett fält saknas i filen: {e}")
        return None

def export_logs_csv(profile):
    """Sparar loggarna som CSV. Det här är datafilen som lämnas in vid examinationen."""
    filename = make_filename(profile.name, "logs.csv")

    if os.path.exists(filename):
        print(f"{filename} finns redan, skriver över.")
    else:
        print(f"Skapar ny fil: {filename}")

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "weight", "calories", "protein", "steps", "trained"])
            for log in profile.logs:
                writer.writerow([log.date, log.weight, log.calories, log.protein, log.steps, log.trained])
        print(f"Sparade {len(profile.logs)} loggar i {filename}")
    except OSError as e:
        print(f"Kunde inte spara loggarna: {e}")


def import_logs_csv(profile, filename):
    """
    Läser in loggar från en valfri CSV-fil. Skiljer sig från export_logs_csv
    genom att filnamnet kommer utifrån, inte från profilens namn.
    """
    imported = 0
    skipped = 0
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
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
                except (ValueError, KeyError):
                    skipped = skipped + 1

        print(f"Importerade {imported} loggar, hoppade över {skipped} felaktiga rader.")
    except FileNotFoundError:
        print(f"Hittade ingen fil: {filename}")