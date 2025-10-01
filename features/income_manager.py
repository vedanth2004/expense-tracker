from sqlalchemy.orm import Session
from database.models import Income
import pandas as pd

class IncomeManager:
    def __init__(self, db: Session, user_id: int, currency):
        self.db = db
        self.user_id = user_id
        self.currency = currency

    def add_income(self, amount: float, source: str, date, currency_code: str):
        r = Income(user_id=self.user_id, amount=amount, source=source, date=date, currency=currency_code)
        self.db.add(r)

    def list_income_df(self) -> pd.DataFrame:
        q = self.db.query(Income).filter(Income.user_id == self.user_id).order_by(Income.date.desc())
        rows = [{
            "id": r.id,
            "date": r.date,
            "source": r.source,
            "amount": r.amount,
            "currency": r.currency
        } for r in q.all()]
        df = pd.DataFrame(rows)
        if not df.empty:
            df["amount_in_base"] = df.apply(lambda r: self.currency.convert(r["amount"], r["currency"]), axis=1)
        return df
