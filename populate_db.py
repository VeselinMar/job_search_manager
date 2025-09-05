from job_search import create_app, db
from job_search.models import Application
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    # Clear existing data (optional)
    db.drop_all()
    db.create_all()

    # Sample data
    firms = ["Acme Corp", "Globex", "Initech", "Umbrella Corp", "Stark Industries"]
    positions = ["Software Engineer", "Data Analyst", "Product Manager", "DevOps Engineer", "QA Engineer"]
    statuses = ["Applied", "Interview", "Offer", "Rejected"]
    notes_samples = [
        "Contacted via LinkedIn",
        "Followed up after 1 week",
        "Received email from HR",
        "Phone interview scheduled",
        "Sent portfolio"
    ]

    # Create multiple applications per firm/position
    for firm in firms:
        for position in positions:
            # Each firm/position gets 2–4 applications
            for _ in range(random.randint(2, 4)):
                status = random.choice(statuses)
                note = random.choice(notes_samples)
                created_at = datetime.utcnow() - timedelta(days=random.randint(0, 60))

                app_entry = Application(
                    firm=firm,
                    position=position,
                    status=status,
                    note=note,
                    created_at=created_at
                )
                db.session.add(app_entry)

    db.session.commit()
    print("Database populated with multiple applications per firm/position!")
