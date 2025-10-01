import streamlit as st
import pandas as pd
from database.models import Expense, Income
from sqlalchemy.orm import Session
import plotly.express as px

def render_dashboard(db: Session, user_id: int, currency):
    # Totals
    exp_q = db.query(Expense).filter(Expense.user_id == user_id)
    inc_q = db.query(Income).filter(Income.user_id == user_id)

    total_exp = sum([currency.convert(r.amount, r.currency) for r in exp_q.all()])
    total_inc = sum([currency.convert(r.amount, r.currency) for r in inc_q.all()])
    balance = total_inc - total_exp

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Income (base)", f"{total_inc:.2f}")
    c2.metric("Total Expense (base)", f"{total_exp:.2f}")
    c3.metric("Balance (base)", f"{balance:.2f}")

    # Expense by category
    rows = [{"category": r.category, "amount": currency.convert(r.amount, r.currency)} for r in exp_q.all()]
    if rows:
        df = pd.DataFrame(rows)
        by_cat = df.groupby("category")["amount"].sum().reset_index()
        fig = px.pie(by_cat, names="category", values="amount", title="Expenses by Category")
        st.plotly_chart(fig, use_container_width=True)

    # Trend by month
    rows2 = [{"month": r.date.strftime("%Y-%m"), "amount": currency.convert(r.amount, r.currency)} for r in exp_q.all()]
    if rows2:
        df2 = pd.DataFrame(rows2)
        trend = df2.groupby("month")["amount"].sum().reset_index()
        fig2 = px.bar(trend, x="month", y="amount", title="Monthly Expense Trend")
        st.plotly_chart(fig2, use_container_width=True)
