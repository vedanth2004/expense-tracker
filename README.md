💸 Expense Tracker (Streamlit)

A production-ready, API-first, modular expense tracker with authentication, budgets, multi-currency support, OCR for receipts, analytics, AI insights, collaboration, gamification, and email notifications.

🚀 Quick Start

Create and activate a virtual environment:

Windows:
.venv\Scripts\activate

macOS/Linux:
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt


Configure environment:

cp .env.example .env
# Edit .env with your configuration


Run the app:

streamlit run app.py

⚙️ Environment Configuration (.env)
SECRET_KEY=change_me
DATABASE_URL=sqlite:///./expense.db
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=app_password
AI_PROVIDER=gemini  # AI Insights enabled via Gemini
CURRENCY_BASE=EUR


Note: The Gemini API key is embedded directly in the AIInsights module, so no separate key setup is required.

✨ Features

💰 Expenses & Income: Add, edit, and track transactions in multiple currencies; attach receipts and notes.

📊 Budgets: Set monthly budgets by category and monitor progress.

📝 OCR Receipts: Extract text from uploaded receipt images automatically.

📈 Analytics & Reports: Visual dashboards, charts, CSV/PDF reports.

🤖 AI Insights: Ask natural language questions about spending, income, and budgets; AI can access expenses, notes, receipts, budgets, and income for detailed analysis.

👥 Collaboration: Share accounts and expenses with other users.

🏆 Gamification: Earn badges and achievements for financial goals and habits.

✉️ Email Notifications: Receive monthly summaries and alerts via email.

💡 Using AI Insights

Ask natural language questions like:

"Did I spend anything on clothes this month?"

"How much did I spend on Food vs. Entertainment?"

"Am I close to exceeding my Rent budget?"

AI Insights can access your expense categories, amounts, notes, receipts (OCR), budgets, and income for detailed analysis.

📝 Notes

Uses SQLite via SQLAlchemy by default; swap DATABASE_URL for PostgreSQL in production.

OCR functionality requires Tesseract OCR installed and in PATH.

User sessions and tokens are short-lived; refresh via login if needed.

AI Insights directly integrates with your financial data for intelligent analysis.