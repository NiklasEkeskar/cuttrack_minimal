from datetime import datetime


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


class User:
    """Bas-klass för en användare som loggar sin data."""

    def __init__(self, name, height_cm, age, sex, start_weight):
        self.name = name
        self.height_cm = height_cm
        self.age = age
        self.sex = sex
        self.start_weight = start_weight
        self.created_date = datetime.now().strftime("%Y-%m-%d")
        self.logs = []

    def add_log(self, log):
        self.logs.append(log)

    def get_logs(self, days):
        if days >= len(self.logs):
            return self.logs
        return self.logs[-days:]

    def average_weight(self, days):
        logs = self.get_logs(days)
        if len(logs) == 0:
            return None
        total = 0
        for log in logs:
            total = total + log.weight
        return round(total / len(logs), 1)

    def average_protein(self, days):
        logs = self.get_logs(days)
        if len(logs) == 0:
            return None
        total = 0
        for log in logs:
            total = total + log.protein
        return round(total / len(logs), 1)

    def average_steps(self, days):
        logs = self.get_logs(days)
        if len(logs) == 0:
            return None
        total = 0
        for log in logs:
            total = total + log.steps
        return round(total / len(logs))

    def weight_change(self, days):
        logs = self.get_logs(days)
        if len(logs) < 2:
            return None
        return round(logs[-1].weight - logs[0].weight, 1)

    def training_days(self, days):
        logs = self.get_logs(days)
        count = 0
        for log in logs:
            if log.trained:
                count = count + 1
        return count

    class CutProfile(User):
    """Barnklass som lägger till mål ovanpå User."""

    def __init__(self, name, height_cm, age, sex, start_weight, goal_weight,
                 protein_goal_per_kg=1.9, step_goal=8000, training_goal_days=3):
        super().__init__(name, height_cm, age, sex, start_weight)

        if goal_weight >= start_weight:
            raise ValueError("Målvikten måste vara lägre än startvikten.")

        self.goal_weight = goal_weight
        self.protein_goal_per_kg = protein_goal_per_kg
        self.step_goal = step_goal
        self.training_goal_days = training_goal_days