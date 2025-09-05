from . import db
from datetime import datetime

class Application(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
        )
    firm = db.Column(
        db.String(120),
        nullable=False
        )
    position = db.Column(
        db.String(120),
        nullable=False
        )
    status = db.Column(
        db.String(50),
        default="Applied"
        )
    note = db.Column(
        db.Text,
        nullable=True
        )
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint("firm", "position", "created_at", name="unique_application"),
    )


    def __repr__(self):
        return(f"<Application {self.firm} - {self.position}")