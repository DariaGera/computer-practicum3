from app import db
from datetime import datetime


class Town(db.Model):
    town = db.Column(db.String, primary_key=True)

    @classmethod
    def find(cls, **where):
        columns = [cls]
        # умови фільтрації
        if where:
            return db.session.query(*columns).filter(db.and_(
                *[cls.__table__.columns[column_name] == column_value for column_name, column_value in
                  where.items()])).all()
        return db.session.query(*columns).all()

    @classmethod
    def add(cls, town):
        new_town = Town(town=town)
        db.session.add(new_town)
        db.session.commit()

    def create(self):
        db.session.add(self)
        db.session.commit()


class Address(db.Model):
    place_id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String, db.ForeignKey("town.town"))
    address = db.Column(db.String, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('town', 'address', name='Address_UN'),
    )
    twn = db.relationship('Town', backref="addresses", foreign_keys=[town])

    @classmethod
    def find(cls, **where):
        columns = [cls]
        # умови фільтрації
        if where:
            return db.session.query(*columns).filter(db.and_(
                *[cls.__table__.columns[column_name] == column_value for column_name, column_value in
                  where.items()])).all()
        return db.session.query(*columns).all()

    @classmethod
    def add(cls, town, address):
        new_address = Address(town=town, address=address)
        db.session.add(new_address)
        db.session.commit()
        return new_address

    def create(self):
        db.session.add(self)
        db.session.commit()


class Call_center_911(db.Model):
    depart_id = db.Column(db.Integer, primary_key=True)
    department_number = db.Column(db.Integer,  nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("address.place_id"))
    __table_args__ = (
        db.UniqueConstraint('department_number', 'place_id', name='Center_UN'),
    )
    depart_identif = db.relationship('Address', backref="centers", foreign_keys=[place_id])

    def create(self):
        db.session.add(self)
        db.session.commit()


class Person(db.Model):
    passport_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()


class Phone(db.Model):
    phone_number = db.Column(db.String, primary_key=True)

    @classmethod
    def find(cls, **where):
        columns = [cls]
        # умови фільтрації
        if where:
            return db.session.query(*columns).filter(db.and_(
                *[cls.__table__.columns[column_name] == column_value for column_name, column_value in
                  where.items()])).all()
        return db.session.query(*columns).all()

    def create(self):
        db.session.add(self)
        db.session.commit()


class Phone_owner(db.Model):
    passport_id = db.Column(db.String, primary_key=True)
    phone_number = db.Column(db.String, primary_key=True)
    data_own = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    __table_args__ = (
        db.ForeignKeyConstraint(['passport_id'], ['person.passport_id'], name='Owner_fk1'),
        db.ForeignKeyConstraint(['phone_number'], ['phone.phone_number'], name='Owner_fk2'),
    )
    pers = db.relationship('Person', backref="people", foreign_keys=[passport_id])
    phone_num = db.relationship('Phone', backref="phones", foreign_keys=[phone_number])

    def create(self):
        db.session.add(self)
        db.session.commit()


class Witness_accident(db.Model):
    witness_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String, db.ForeignKey("phone.phone_number"))
    place_id = db.Column(db.Integer, db.ForeignKey("address.place_id"))
    title = db.Column(db.String, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('phone_number', 'place_id', 'title', name='accident_UN'),
    )
    pers = db.relationship('Phone', backref="phonnes", foreign_keys=[phone_number])
    phone_num = db.relationship('Address', backref="addresses", foreign_keys=[place_id])

    def title_update(self, new_title):
        self.title = new_title
        db.session.commit()

    @classmethod
    def find(cls, **where):
        columns = [cls]
        # умови фільтрації
        if where:
            return db.session.query(*columns).filter(db.and_(
                *[cls.__table__.columns[column_name] == column_value for column_name, column_value in
                  where.items()])).all()
        return db.session.query(*columns).all()

    @classmethod
    def add(cls, place_id, title):
        phone_number = '0134-56-67'
        new_witn = Witness_accident(phone_number=phone_number, place_id=place_id, title=title)
        db.session.add(new_witn)
        db.session.commit()
        return new_witn

    def create(self):
        db.session.add(self)
        db.session.commit()


class Operator_911(db.Model):
    operator_pass_id = db.Column(db.String, db.ForeignKey("person.passport_id"))
    depart_id = db.Column(db.Integer, db.ForeignKey("call_center_911.depart_id"))
    __table_args__ = (
        db.PrimaryKeyConstraint('operator_pass_id', name='operator_pk'),
    )
    operator_pass = db.relationship('Person', backref="operators",  foreign_keys=[operator_pass_id])
    depart = db.relationship('Call_center_911', backref="departs", foreign_keys=[depart_id])

    def __repr__(self):
        return "<Operator_911(operator_pass_id='%s'; depart_id='%s')>" % (self.operator_pass_id, self.depart_id)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find(cls, **where):
        columns = [cls]
        # умови фільтрації
        if where:
            return db.session.query(*columns).filter(db.and_(
                *[cls.__table__.columns[column_name] == column_value for column_name, column_value in where.items()])).all()
        return db.session.query(*columns).all()


class Call_911(db.Model):
    operator_pass_id = db.Column(db.String, db.ForeignKey("operator_911.operator_pass_id"))
    call_begin = db.Column(db.DateTime)
    witness_id = db.Column(db.Integer, db.ForeignKey("witness_accident.witness_id"))
    call_end = db.Column(db.DateTime, nullable=True)
    __table_args__ = (
        db.PrimaryKeyConstraint('operator_pass_id', 'call_begin', name='call_pk'),
    )
    operator = db.relationship('Operator_911', backref="operators", foreign_keys=[operator_pass_id])
    place = db.relationship('Witness_accident', backref="accidents", foreign_keys=[witness_id])

    def __repr__(self):
        return "<Call_911(operator_pass_id='%s'; call_begin='%s'; witness_id='%s'; call_end='%s')>" % (
            self.operator_pass_id, self.call_begin, self.witness_id, self.call_end)

    def delete_self(self):
        db.session.delete(self)
        db.session.commit()

    def operator_update(self, pass_id):
        self.operator_pass_id = pass_id
        self.call_begin = datetime.today()
        self.call_end = None
        db.session.commit()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def main_query(cls, **where):
        if where:
            return db.session.query(Call_911, Witness_accident, Address).select_from(Call_911).join(
                Witness_accident).join(Address).filter(db.and_(*[cls.__table__.columns[column_name] == column_value for column_name, column_value in where.items()])).all()
        return db.session.query(Call_911, Witness_accident, Address).select_from(Call_911).join(
            Witness_accident).join(Address).all()

    @classmethod
    def find(cls, **where):
        columns = [cls]
        # умови фільтрації
        if where:
            return db.session.query(*columns).filter(db.and_(
                *[cls.__table__.columns[column_name] == column_value for column_name, column_value in
                  where.items()])).all()
        return db.session.query(*columns).all()


db.create_all()


"""
Town(town='NEW HANOVER').create()
Town(town='NORRISTOWN').create()
Town(town='SKIPPACK').create()
Town(town='LOWER SALFORD').create()
Address(town='NEW HANOVER', address='REINDEER CT and DEAD END').create()
Address(town='NEW HANOVER', address='CHARLOTTE ST and MILES RD').create()
Address(town='NORRISTOWN', address='HAWS AVE').create()
Address(town='SKIPPACK', address='COLLEGEVILLE RD and LYWISKI RD').create()
Address(town='LOWER SALFORD', address='MAIN ST and OLD SUMNEYTOWN PIKE').create()
Call_center_911(department_number=1562, place_id=3).create()
Call_center_911(department_number=2163, place_id=4).create()
Person(passport_id='ID65738UKR', name='Bob Bobanenko').create()
Person(passport_id='ID54321USA', name='Boba Smith').create()
Person(passport_id='ID64888USA', name='Kate Poy').create()
Person(passport_id='ID12345USA', name='Mark Bobanchuk').create()
Person(passport_id='ID11111PO', name='Paul Goro').create()
Phone(phone_number='0128-44-34').create()
Phone(phone_number='0134-56-67').create()
Phone(phone_number='0500-01-01').create()
Phone_owner(passport_id='ID65738UKR', phone_number='0128-44-34', data_own=datetime(2018, 7, 25).date(), status=0).create()
Phone_owner(passport_id='ID64888USA', phone_number='0134-56-67', data_own=datetime(2018, 7, 26).date(), status=0).create()
Phone_owner(passport_id='ID54321USA', phone_number='0134-56-67', data_own=datetime(2019, 7, 25).date(), status=1).create()
Phone_owner(passport_id='ID11111PO', phone_number='0128-44-34', data_own=datetime(2019, 7, 25).date(), status=1).create()
Phone_owner(passport_id='ID12345USA', phone_number='0500-01-01', data_own=datetime(2019, 7, 27).date(), status=0).create()
Phone_owner(passport_id='ID65738UKR', phone_number='0500-01-01', data_own=datetime(2019, 8, 28).date(), status=1).create()
Witness_accident(phone_number='0128-44-34', place_id=3, title='EMS: CARDIAC EMERGENCY').create()
Witness_accident(phone_number='0134-56-67', place_id=3, title='Traffic: VEHICLE ACCIDENT').create()
Witness_accident(phone_number='0500-01-01', place_id=4, title='EMS: FALL VICTIM').create()
Witness_accident(phone_number='0128-44-34', place_id=3, title='Fire: BUILDING FIRE').create()
Operator_911(operator_pass_id='ID64888USA', depart_id=1).create()
Operator_911(operator_pass_id='ID12345USA', depart_id=1).create()
Operator_911(operator_pass_id='ID11111PO', depart_id=2).create()
Call_911(operator_pass_id='ID64888USA', call_begin=datetime(2018, 7, 25, 13, 17, 41), witness_id=1,
         call_end=datetime(2018, 7, 25, 15, 5, 23)).create()
Call_911(operator_pass_id='ID12345USA', call_begin=datetime(2019, 7, 25, 21, 24, 40), witness_id=4,
         call_end=datetime(2019, 7, 25, 21, 31, 44)).create()
Call_911(operator_pass_id='ID11111PO', call_begin=datetime(2019, 8, 29, 19, 33, 31), witness_id=3,
         call_end=datetime(2019, 8, 29, 20, 6, 12)).create()
"""



