from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Institution(db.Model):
    __tablename__ = 'institutions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    address = db.Column(db.String(128))
    telephone_1 = db.Column(db.String(128))
    telephone_2 = db.Column(db.String(128))
    email = db.Column(db.String(128))
    headoffice = db.Column(db.String(128))
    category = db.Column(db.String(128))
    about = db.Column(db.Text(128))
    period_incorporated = db.Column(db.String(128))
    reports = db.relationship("Report", backref='institution', lazy="dynamic")
    key_metrics = db.relationship(
        "KeyMetrics", backref='institution', lazy="dynamic")
    other_details = db.relationship(
        "OtherDetail", backref='institution', lazy="dynamic")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, ForeignKey("users.id"))


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(128))
    type = db.Column(db.String(128))
    summary = db.Column(db.Text())
    description = db.Column(db.Text())
    report = db.Column(db.LargeBinary())
    institution_id = db.Column(
        db.String(128), db.ForeignKey("institutions.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, ForeignKey("users.id"))


class KeyMetrics(db.Model):
    __tablename__ = "key_metrics"
    id = db.Column(db.Integer, primary_key=True)
    capital_adequacy = db.Column(db.Integer)
    owners_equity = db.Column(db.Integer)
    total_liability = db.Column(db.Integer)
    nonperforming_loans_ratio = db.Column(db.Integer)
    period = db.Column(db.String(128))
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, ForeignKey("users.id"))


class OtherDetail(db.Model):
    __tablename__ = "other_details"
    id = db.Column(db.Integer, primary_key=True)
    directors = db.Column(db.String(256))
    board_members = db.Column(db.String(256))
    managing_director = db.Column(db.String(256))
    board_chairman = db.Column(db.String(256))
    period = db.Column(db.String(128))
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, ForeignKey("users.id"))


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(128), nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    institutions = db.relationship(
        "Institution", backref="user", lazy="dynamic")
    keymetrics = db.relationship("KeyMetric", backref="user", lazy="dynamic")
    other_details = db.relationship(
        "OtherDetail", backref="user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="users", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self, perm):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    class Permission():
        PUBLISH_BLOG = 1
        ADD_INSITUTITION = 2
        DELETE_INSTITUTION = 4
        VIEW_INSTITUTION = 8
        UPDATE_INSTITUTTION = 16
