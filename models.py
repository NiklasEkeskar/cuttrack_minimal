class DailyLog:
    """En daglig logg med vikt, kalorier, protein, steg och träning."""

    def __init__(self, date, weight, calories, protein, steps, trained):
        if weight <= 0 or weight > 400:
            raise ValueError(f"Orimligt vikt-värde: {weight}")
        if calories < 0 or calories > 10000:
            raise ValueError(f"Orimligt kalori-värde: {calories}")

        self.date = date
        self.weight = weight
        self.calories = calories
        self.protein = protein
        self.steps = steps
        self.trained = trained
