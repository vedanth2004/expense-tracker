import streamlit as st
from config import settings
from auth.authenticator import Authenticator
from database.db_manager import init_db, get_session
from features.expense_manager import ExpenseManager
from features.income_manager import IncomeManager
from features.budget_manager import BudgetManager
from features.ocr_processor import OCRProcessor
from features.currency_converter import CurrencyConverter
from analytics.dashboard import render_dashboard
from analytics.reports import Reports
from analytics.ai_insights import AIInsights
from collaboration.shared_accounts import SharedAccounts
from gamification.achievements import Achievements
from notifications.email_handler import EmailHandler
from ui.theme import apply_theme
from ui.components import nav_bar
from config import settings
from utils.helpers import ensure_tables, safe_float

st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")
apply_theme()

# Initialize DB
engine = init_db()
ensure_tables(engine)

auth = Authenticator(settings.secret_key)
email_service = EmailHandler(settings)
currency = CurrencyConverter(settings.currency_base)
ai = AIInsights()
ocr = OCRProcessor()
reports = Reports()
shared = SharedAccounts()
achievements = Achievements()

# Session state
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

st.title("Expense Tracker 💸")

# Auth flow
if not st.session_state.token:
    tab_login, tab_signup = st.tabs(["Login", "Sign up"])
    with tab_login:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            ok, user, token, msg = auth.login(email, password)
            if ok:
                st.session_state.token = token
                st.session_state.user = user
                st.success("Logged in")
                st.rerun()
            else:
                st.error(msg)
    with tab_signup:
        name = st.text_input("Name")
        email2 = st.text_input("Email (signup)")
        pass1 = st.text_input("Password (signup)", type="password")
        if st.button("Create account"):
            ok, msg = auth.signup(name, email2, pass1)
            if ok:
                st.success("Account created. Please log in.")
            else:
                st.error(msg)
    st.stop()

# Authenticated app
user = st.session_state.user
token = st.session_state.token

page = nav_bar(["Dashboard", "Expenses", "Income", "Budgets", "Reports", "AI Insights", "Collaboration", "Gamification", "Settings"])

with get_session() as db:
    exp = ExpenseManager(db, user_id=user["id"], currency=currency)
    inc = IncomeManager(db, user_id=user["id"], currency=currency)
    bud = BudgetManager(db, user_id=user["id"], currency=currency)
    if page == "Dashboard":
        render_dashboard(db, user["id"], currency)
    elif page == "Expenses":
        st.subheader("Add Expense")
        col1, col2, col3 = st.columns(3)
        with col1:
            amount = st.text_input("Amount")
        with col2:
            category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Other"])
        with col3:
            currency_code = st.text_input("Currency", value=currency.base)
        note = st.text_input("Note")
        date = st.date_input("Date")
        receipt = st.file_uploader("Receipt image (optional)", type=["png", "jpg", "jpeg"])
        st.dataframe(shared.list_shared(user["id"]))
        if st.button("Add Expense"):
            amt = safe_float(amount)
            if amt is None:
                st.error("Invalid amount")
            else:
                ocr_text = None
                if receipt is not None:
                    ocr_text = ocr.extract_text(receipt)
                exp.add_expense(amount=amt, category=category, note=note, date=date, currency_code=currency_code.upper(), receipt_text=ocr_text)
                st.success("Expense added")

        st.divider()
        st.subheader("Expenses List")
        st.dataframe(exp.list_expenses_df())

    elif page == "Income":
        st.subheader("Add Income")
        col1, col2 = st.columns(2)
        with col1:
            amount = st.text_input("Amount")
        with col2:
            source = st.selectbox("Source", ["Salary", "Business", "Investment", "Other"])
        date = st.date_input("Date")
        currency_code = st.text_input("Currency", value=currency.base)
        if st.button("Add Income"):
            amt = safe_float(amount)
            if amt is None:
                st.error("Invalid amount")
            else:
                inc.add_income(amount=amt, source=source, date=date, currency_code=currency_code.upper())
                st.success("Income added")
        st.divider()
        st.subheader("Income List")
        st.dataframe(inc.list_income_df())

    elif page == "Budgets":
        st.subheader("Budgets")
        category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Other"])
        monthly_limit = st.text_input("Monthly Limit")
        if st.button("Set Budget"):
            amt = safe_float(monthly_limit)
            if amt is None:
                st.error("Invalid limit")
            else:
                bud.set_budget(category, amt)
                st.success("Budget set")
        st.dataframe(bud.list_budgets_df())
        st.info(bud.budget_status_summary())

    elif page == "Reports":
        st.subheader("Generate Report")
        start = st.date_input("Start Date")
        end = st.date_input("End Date")
        fmt = st.selectbox("Format", ["CSV", "PDF"])
        if st.button("Download"):
            if fmt == "CSV":
                data = reports.generate_csv(db, user["id"], start, end)
                st.download_button("Download CSV", data=data, file_name="report.csv", mime="text/csv")
            else:
                pdf_bytes = reports.generate_pdf(db, user["id"], start, end)
                st.download_button("Download PDF", data=pdf_bytes, file_name="report.pdf", mime="application/pdf")

    elif page == "AI Insights":
        st.subheader("Spending Insights")
        prompt = st.text_area("Ask about spending patterns")

        if st.button("Analyze"):
            if prompt.strip():  
                with st.spinner("Analyzing your spending..."):
                    out = ai.analyze(db, user["id"], prompt)
                st.write(out)
            else:
                st.warning("Please enter a prompt for analysis.")


    elif page == "Collaboration":
        st.subheader("Shared Accounts")
        email_other = st.text_input("Invite user email")
        if st.button("Invite"):
            ok, msg = shared.invite(user["id"], email_other)
            st.success(msg) if ok else st.error(msg)
        st.dataframe(shared.list_shared(user["id"]))
        
    elif page == "Gamification":
        st.subheader("Achievements")
        st.write(achievements.summary(db, user["id"]))
        st.dataframe(achievements.list_badges(db, user["id"]))

    elif page == "Settings":
        st.subheader("Profile & Notifications")
        email_notify = st.toggle("Email monthly summary")
        if st.button("Save"):
            if email_notify:
                email_service.send_test(user["email"], "Notifications enabled", "You'll receive monthly summaries.")
            st.success("Settings saved")

    st.sidebar.button("Logout", on_click=lambda: (st.session_state.update({"token": None, "user": None}), st.rerun()))
    
