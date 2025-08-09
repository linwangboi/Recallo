# recallo/api/business/review_sheduler.py

from datetime import timedelta

# Schedule in days for each sequence number
REVIEW_SCHEDULE = {
    0: 1,   # after creating study item
    1: 2,   # after first review
    2: 4,   # after second review
    3: 8,   # after third review
    4: 15,  # after fourth review
    5: None # after fifth review (no more reminders)
}

def get_next_review_date(sequence, missed=False, last_action_date=None):
    """
    Calculate the next scheduled review date.
    sequence: int — current review sequence (0 = just studied)
    missed: bool — whether the last scheduled review was missed
    last_action_date: date or datetime — when the last review/study happened
    """
    if not last_action_date:
        raise ValueError("last_action_date is required")

    # Missed review handling
    if missed:
        if sequence in (1, 4, 5):
            # Daily until done
            return last_action_date + timedelta(days=1)
        else:
            # Restart cycle at seq 1
            return last_action_date + timedelta(days=REVIEW_SCHEDULE[1])

    # Normal schedule
    days = REVIEW_SCHEDULE.get(sequence)
    if days is None:
        return None
    return last_action_date + timedelta(days=days)
