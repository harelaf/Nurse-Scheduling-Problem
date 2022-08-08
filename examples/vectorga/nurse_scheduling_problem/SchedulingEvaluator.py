from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator

SCHEDULING_DAYS = 7
SHIFTS_PER_DAY = 3
SHIFTS_PER_WEEK = SCHEDULING_DAYS * SHIFTS_PER_DAY

MORNING_SHIFT = 0
AFTERNOON_SHIFT = 1
NIGHT_SHIFT = 2

MORNING_CHIEF = 1
MORNING_NURSES = 3
AFTERNOON_CHIEF = 2
AFTERNOON_NURSES = 5
NIGHT_CHIEF = 2
NIGHT_NURSES = 7


class NurseSchedulingEvaluator(SimpleIndividualEvaluator):
    """
    Evaluator class for the 'Nurse Scheduling Problem'.

    Attributes
    -------
    nurse_amount: int
        The number of regular nurses.
    chief_amount: int
        The number of chief nurses.
    hard_weight: float
        The weight of hard constraints.
    soft_weight: float
        The weight of soft constraints.
    total_nurses: int
        The total amount of nurses (chief and regular).
    constraints: function list
        A list of the scheduling constraints, as evaluation functions.
    """

    def __init__(self, nurse_amount, chief_amount, hard_weight=10., soft_weight=1.):
        super().__init__()

        self.nurse_amount = nurse_amount
        self.chief_amount = chief_amount
        self.hard_weight = hard_weight
        self.soft_weight = soft_weight
        self.total_nurses = self.nurse_amount + self.chief_amount
        self.constraints = []
        self.init_constraints()

    def init_constraints(self):
        self.constraints.append(self.hard_no_3_consecutive_night_shifts)
        self.constraints.append(self.hard_no_morning_shift_after_night_shift)
        self.constraints.append(self.soft_at_least_one_off_day_per_week)
        self.constraints.append(self.soft_max_3_night_shifts_per_week)
        self.constraints.append(self.soft_no_3_consecutive_shifts)

    # Hard constraints
    def hard_no_3_consecutive_night_shifts(self, individual, nurse):
        consecutive_days = 0
        for i in range(SCHEDULING_DAYS):
            block = self.total_nurses * (i * SHIFTS_PER_DAY + NIGHT_SHIFT) + nurse
            if individual.cell_value(block):
                consecutive_days += 1
            else:
                consecutive_days = 0
            if consecutive_days >= 3:
                return self.hard_weight
        return 0.

    def hard_no_morning_shift_after_night_shift(self, individual, nurse):
        for i in range(1, SCHEDULING_DAYS):
            night_shift = self.total_nurses * ((i - 1) * SHIFTS_PER_DAY + NIGHT_SHIFT) + nurse
            morning_shift = self.total_nurses * (i * SHIFTS_PER_DAY + MORNING_SHIFT) + nurse
            if individual.cell_value(night_shift) and individual.cell_value(morning_shift):
                return self.hard_weight
        return 0.

    def hard_shift_nurse_constraints(self, individual, shift, chief_requirement, nurse_requirement):
        chiefs = 0
        nurses = 0
        result = 0.
        for i in range(SCHEDULING_DAYS):
            row = (i * SHIFTS_PER_DAY + shift) * self.total_nurses
            for j in range(self.chief_amount):
                chiefs += individual.cell_value(row + j)
            for j in range(self.chief_amount, self.total_nurses):
                nurses += individual.cell_value(row + j)
            if chiefs < chief_requirement:
                result += self.hard_weight
            elif chiefs > chief_requirement:
                result += self.soft_weight * (chiefs - chief_requirement)
            if nurses < nurse_requirement:
                result += self.hard_weight
            elif nurses > nurse_requirement:
                result += self.soft_weight * (nurses - nurse_requirement)
            chiefs = 0
            nurses = 0
        return result

    # Soft constraints
    def soft_at_least_one_off_day_per_week(self, individual, nurse):
        for i in range(SCHEDULING_DAYS):
            morning = self.total_nurses * (i * SHIFTS_PER_DAY + MORNING_SHIFT) + nurse
            afternoon = self.total_nurses * (i * SHIFTS_PER_DAY + AFTERNOON_SHIFT) + nurse
            night = self.total_nurses * (i * SHIFTS_PER_DAY + NIGHT_SHIFT) + nurse
            if (not individual.cell_value(morning)) and \
                    (not individual.cell_value(afternoon)) and \
                    (not individual.cell_value(night)):
                return 0.
        return self.soft_weight

    def soft_max_3_night_shifts_per_week(self, individual, nurse):
        night_days = 0
        for i in range(SCHEDULING_DAYS):
            block = self.total_nurses * (i * SHIFTS_PER_DAY + NIGHT_SHIFT) + nurse
            if individual.cell_value(block):
                night_days += 1
            if night_days >= 4:
                return self.soft_weight
        return 0.

    def soft_no_3_consecutive_shifts(self, individual, nurse):
        consecutive_shifts = 0
        for i in range(SHIFTS_PER_WEEK):
            block = self.total_nurses * i + nurse
            if individual.cell_value(block):
                consecutive_shifts += 1
            else:
                consecutive_shifts = 0
            if consecutive_shifts >= 3:
                return self.hard_weight
        return 0.

    def _evaluate_individual(self, individual):
        evaluation_score = 0.

        # General constraints
        evaluation_score += self.hard_shift_nurse_constraints(individual, MORNING_SHIFT, MORNING_CHIEF, MORNING_NURSES)
        evaluation_score += self.hard_shift_nurse_constraints(individual, AFTERNOON_SHIFT, AFTERNOON_CHIEF, AFTERNOON_NURSES)
        evaluation_score += self.hard_shift_nurse_constraints(individual, NIGHT_SHIFT, NIGHT_CHIEF, NIGHT_NURSES)

        # Constraints list
        for nurse in range(self.total_nurses):
            for func in self.constraints:
                evaluation_score += func(individual, nurse)

        return evaluation_score
