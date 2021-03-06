import datetime
from enum import Enum

from sqlalchemy.orm import relationship

from app.models import db


class AdminTypeChoice(Enum):
    ROOT = 1
    ADMINISTRATION = 2
    QNA = 3
    INTERVIEW = 4


class AdminModel(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    admin_type = db.Column(db.Enum(AdminTypeChoice), nullable=False, default=AdminTypeChoice.INTERVIEW)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DATETIME, nullable=True, default=datetime.datetime.utcnow)


class SchoolModel(db.Model):
    __tablename__ = 'school'

    code = db.Column(db.String(10), primary_key=True)
    government = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # one to one3
    graduate_info = relationship("GraduateInfoModel", uselist=False, backref="user")
