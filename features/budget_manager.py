from sqlalchemy.orm import Session
from database.models import Budget, Expense
import pandas as pd
from datetime import date

class BudgetManager:
    def __init__(self, db: Session, user_id: int, currency):
        self.db = db
        self.user_id = user_id
        self.currency = currency

    def set_budget(self, category: str, monthly_limit: float):
        b = self.db.query(Budget).filter(Budget.user_id == self.user_id, Budget.category == category).first()
        if b:
            b.monthly_limit = monthly_limit
        else:
            b = Budget(user_id=self.user_id, category=category, monthly_limit=monthly_limit)
            self.db.add(b)

    def list_budgets_df(self) -> pd.DataFrame:
        q = self.db.query(Budget).filter(Budget.user_id == self.user_id)
        return pd.DataFrame([{"category": r.category, "monthly_limit": r.monthly_limit} for r in q.all()])

    def budget_status_summary(self) -> str:
        # Calculate current month spend per category vs budget
        import calendar, datetime
        now = datetime.date.today()
        start = now.replace(day=1)
        end_day = calendar.monthrange(now.year, now.month)[1]
        end = now.replace(day=end_day)

        # expenses current month
        q = self.db.query(Expense).filter(
            Expense.user_id == self.user_id,
            Expense.date >= start,
            Expense.date <= end
        )
        spent = {}
        for r in q.all():
            amt = self.currency.convert(r.amount, r.currency)
            spent[r.category] = spent.get(r.category, 0.0) + amt

        # compare with budgets
        q2 = self.db.query(Budget).filter(Budget.user_id == self.user_id)
        lines = []
        for b in q2.all():
            s = spent.get(b.category, 0.0)
            pct = 0 if b.monthly_limit == 0 else (s / b.monthly_limit) * 100
            lines.append(f"{b.category}: {s:.2f}/{b.monthly_limit:.2f} ({pct:.0f}%)")
        return "\n".join(lines) if lines else "No budgets set"
