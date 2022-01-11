from datetime import datetime
from views import app, db, Barrier

with app.app_context():
    db.create_all()
    b = Barrier(updated_at=datetime.now())
    db.session.add(b)
    db.session.commit()
