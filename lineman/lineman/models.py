from datetime import datetime
from app import db
from marshmallow_sqlalchemy import ModelSchema


class Barrier(db.Model):
    __tablename__ = "barrier"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default="opened")
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)


class BarrierSchema(ModelSchema):
    class Meta:
        model = Barrier
        fields = ("status", "updated_at")
