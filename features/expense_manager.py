from sqlalchemy.orm import Session
from database.models import Expense
import pandas as pd
from datetime import date

class ExpenseManager:
    def __init__(self, db: Session, user_id: int, currency):
        self.db = db
        self.user_id = user_id
        self.currency = currency

    def add_expense(self, amount: float, category: str, note: str, date, currency_code: str, receipt_text: str | None):
        e = Expense(user_id=self.user_id, amount=amount, category=category, note=note or "", date=date, currency=currency_code, receipt_text=receipt_text or "")
        self.db.add(e)

    def list_expenses_df(self) -> pd.DataFrame:
        q = self.db.query(Expense).filter(Expense.user_id == self.user_id).order_by(Expense.date.desc())
        rows = [{
            "id": r.id,
            "date": r.date,
            "category": r.category,
            "amount": r.amount,
            "currency": r.currency,
            "note": r.note
        } for r in q.all()]
        df = pd.DataFrame(rows)
        if not df.empty:
            df["amount_in_base"] = df.apply(lambda r: self.currency.convert(r["amount"], r["currency"]), axis=1)
        return df
