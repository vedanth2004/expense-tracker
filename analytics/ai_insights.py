from sqlalchemy.orm import Session
from database.models import *
import google.generativeai as genai

# Paste your Gemini API key here
GEMINI_API_KEY = "AIzaSyDbSzekjgNHzm7vxou3YuQN4HeFqQo-j5g"  # Replace with your real key

class AIInsights:
    def __init__(self):
        pass  # No settings needed

    def _basic_rules(self, expenses):
        """Simple heuristic insights without external AI"""
        out = []
        by_cat = {}
        for e in expenses:
            by_cat.setdefault(e.category, 0.0)
            by_cat[e.category] += e.amount
        if by_cat:
            top_cat = max(by_cat, key=by_cat.get)
            out.append(f"Highest raw spend category: {top_cat}")
        return "\n".join(out) if out else "No data"

    def analyze(self, db: Session, user_id: int, prompt: str):
        """Generate AI insights including expenses, budgets, and income"""
        if not prompt.strip():
            return "Please provide a question or prompt for AI insights."

        # Fetch last 200 expenses
        exps = db.query(Expense).filter(Expense.user_id == user_id).all()

        # Fetch budgets
        budgets = db.query(Budget).filter(Budget.user_id == user_id).all()

        # Fetch income
        incomes = db.query(Income).filter(Income.user_id == user_id).all()

        if not exps and not budgets and not incomes:
            return "No data found for this user."

        # Prepare expenses context
        exp_context = "; ".join([
            f"{e.date}: {e.category}: {e.amount}{e.currency}: Note: {e.note or 'None'}; Receipt: {e.receipt_text or 'None'}"
            for e in exps[-200:]
        ])

        # Prepare budgets context
        budget_context = "; ".join([
            f"{b.category}: monthly limit {b.monthly_limit}" for b in budgets
        ])

        # Prepare income context
        income_context = "; ".join([
            f"{i.date}: {i.source}: {i.amount}{i.currency}" for i in incomes[-200:]
        ])

        # Combine everything for AI
        full_context = f"Expenses: {exp_context}\nBudgets: {budget_context}\nIncome: {income_context}"

        # Call Gemini AI
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("models/gemini-2.5-pro")
            response = model.generate_content(
                f"Analyze the following spending data and answer the question:\n{prompt}\n\nData:\n{full_context[:6000]}"
            )
            return response.text.strip() if response.text else "AI returned no answer"
        except Exception as e:
            # Fallback summary on error
            return f"AI request error: {str(e)}\n\nFallback summary:\n" + self._basic_rules(exps)
