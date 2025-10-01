from sqlalchemy.orm import Session
from database.models import Badge, Expense
import pandas as pd
import datetime

class Achievements:
    def _evaluate(self, db: Session, user_id: int):
        # Example badges
        badges = []
        # 1) First Expense
        first = db.query(Expense).filter(Expense.user_id == user_id).first()
        if first:
            badges.append(("First Expense", "Logged the first expense"))
        # 2) Streak: expenses logged 3 days in a row
        dates = sorted({e.date for e in db.query(Expense).filter(Expense.user_id == user_id).all()})
        streak = 1
        best = 1
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                streak += 1
                best = max(best, streak)
            else:
                streak = 1
        if best >= 3:
            badges.append(("3-Day Streak", "Logged expenses three days in a row"))
        return badges

    def summary(self, db: Session, user_id: int) -> str:
        b = self._evaluate(db, user_id)
        return f"Unlocked {len(b)} badges"

    def list_badges(self, db: Session, user_id: int):
        data = [{"name": n, "detail": d} for n, d in self._evaluate(db, user_id)]
        return pd.DataFrame(data)
