from sqlalchemy.orm import Session
from database.db_manager import get_session
from database.models import Share, User
from email_validator import validate_email, EmailNotValidError

class SharedAccounts:
    def invite(self, owner_id: int, member_email: str):
        try:
            validate_email(member_email)
        except EmailNotValidError as e:
            return False, str(e)
        with get_session() as db:
            s = Share(owner_id=owner_id, member_email=member_email)
            db.add(s)
        return True, "Invitation recorded"

    def list_shared(self, owner_id: int):
        with get_session() as db:
            q = db.query(Share).filter(Share.owner_id == owner_id)
            rows = [{"member_email": r.member_email, "since": r.created_at} for r in q.all()]
        import pandas as pd
        return pd.DataFrame(rows)
