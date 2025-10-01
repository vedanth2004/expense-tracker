import io
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from database.models import Expense, Income
from sqlalchemy.orm import Session

class Reports:
    def generate_csv(self, db: Session, user_id: int, start, end) -> bytes:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["type", "date", "category/source", "amount", "currency", "note"])
        for r in db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start, Expense.date <= end).all():
            writer.writerow(["expense", r.date.isoformat(), r.category, r.amount, r.currency, r.note])
        for r in db.query(Income).filter(Income.user_id == user_id, Income.date >= start, Income.date <= end).all():
            writer.writerow(["income", r.date.isoformat(), r.source, r.amount, r.currency, ""])
        return output.getvalue().encode("utf-8")

    def generate_pdf(self, db: Session, user_id: int, start, end) -> bytes:
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=LETTER)
        width, height = LETTER
        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Expense Report")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Range: {start} to {end}")
        y -= 20
        c.drawString(50, y, "Expenses:")
        y -= 15
        for r in db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start, Expense.date <= end).all():
            c.drawString(60, y, f"{r.date} | {r.category} | {r.amount} {r.currency} | {r.note[:40]}")
            y -= 12
            if y < 60:
                c.showPage()
                y = height - 50
        y -= 10
        c.drawString(50, y, "Income:")
        y -= 15
        for r in db.query(Income).filter(Income.user_id == user_id, Income.date >= start, Income.date <= end).all():
            c.drawString(60, y, f"{r.date} | {r.source} | {r.amount} {r.currency}")
            y -= 12
            if y < 60:
                c.showPage()
                y = height - 50
        c.showPage()
        c.save()
        return buf.getvalue()
