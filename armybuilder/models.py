from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Text, create_engine, Table, Boolean
from sqlalchemy.orm import relationship
import os
from typing import Type

DB_DIALECT = 'sqlite'
DB_PATH = os.path.join(os.path.dirname(__file__), '.db', 'db.sqlite')

def get_sqlalchemy_uri() -> str:
    # triple quotes for sqlite, update this with dialect change
    uri = f'{DB_DIALECT}:///{DB_PATH}'

    # For SQLite, make sure DB dir exists and create the tables
    # Update this if dialect changes
    if not os.path.exists(DB_PATH):
        db_dir = os.path.dirname(DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        os.system(f'touch "{DB_PATH}"')
        engine = create_engine(uri)
        Base.metadata.create_all(engine)

    return uri


Base = declarative_base()


def make_secondary_table(a: str, b: str) -> Table:
    table_name = f'{a}_{b}_secondary'
    association_table = Table(table_name, Base.metadata,
        Column(f'{a}_id', Integer, ForeignKey(f'{a}.id')),
        Column(f'{b}_id', Integer, ForeignKey(f'{b}.id'))
    )
    return association_table

figure_keyword_table = make_secondary_table('figure', 'keyword')
figure_ability_table = make_secondary_table('figure', 'ability')
wargear_ability_table = make_secondary_table('wargear', 'ability')
roster_entry_wargear_table = make_secondary_table('rosterentry', 'wargear')
faction_ability_table = make_secondary_table('faction', 'ability')
figure_faction_table = make_secondary_table('figure', 'faction')
tactic_faction_table = make_secondary_table('tactic', 'faction')
roster_faction_table = make_secondary_table('roster', 'faction')
class Figure(Base):
    __tablename__ = 'figure'
    id = Column(Integer, primary_key=True)
    figure_type = Column(Text)
    figure_name = Column(Text)
    points = Column(Integer)
    move = Column(Text)
    weapon_skill = Column(Integer)
    ballistic_skill = Column(Integer)
    strength = Column(Text)
    toughness = Column(Text)
    wounds = Column(Text)
    attacks = Column(Text)
    leadership = Column(Text)
    save = Column(Text)
    max_number = Column(Integer)

    factions = relationship(
        'Faction', secondary=figure_faction_table,
        back_populates='figures',
        lazy='subquery'
    )

    keywords = relationship(
        'Keyword',
        secondary=figure_keyword_table,
        back_populates='figures',
        lazy='subquery'
    )
    abilities = relationship(
        'Ability',
        secondary=figure_ability_table,
        back_populates='figures',
        lazy='subquery'
    )

    def __str__(self):
        return f'{self.figure_type if self.figure_type else ""} {self.figure_name if self.figure_name else ""}'

class Wargear(Base):
    __tablename__ = 'wargear'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    profile = Column(Text)
    wargear_range = Column(Text)
    wargear_type = Column(Text)
    strength = Column(Text)
    ap = Column(Text)
    damage = Column(Text)
    points = Column(Integer)

    abilities = relationship(
        'Ability',
        secondary=wargear_ability_table,
        back_populates='wargear',
        lazy='subquery'
    )

    roster_entries = relationship(
        'RosterEntry',
        secondary=roster_entry_wargear_table,
        back_populates='wargear',
        lazy='subquery'
    )

    def __str__(self):
        return self.name

class Keyword(Base):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    label = Column(Text)
    names = Column(Text)
    figures = relationship(
        'Figure',
        secondary=figure_keyword_table,
        back_populates='keywords',
        lazy='subquery'
    )

    def __str__(self):
        return self.label

class Ability(Base):
    __tablename__ = 'ability'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    text = Column(Text)

    wargear = relationship(
        'Wargear',
        secondary=wargear_ability_table,
        back_populates='abilities',
        lazy='subquery'
    )

    figures = relationship(
        'Figure',
        secondary=figure_ability_table,
        back_populates='abilities',
        lazy='subquery'
    )

    factions = relationship(
        'Faction',
        secondary=faction_ability_table,
        back_populates='abilities'
    )

    def __str__(self):
        return self.name

class Specialization(Base):
    __tablename__ = 'specialization'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    tactic_id = Column(Integer, ForeignKey('tactic.id'))
    tactic = relationship('Tactic')
    passive = Column(Text)

    def __str__(self):
        return self.name
class Tactic(Base):
    __tablename__ = 'tactic'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    cost = Column(Integer)
    text = Column(Text)
    

    keyword_id = Column(Integer, ForeignKey('keyword.id'))
    keyword = relationship('Keyword')

    factions = relationship('Faction',
        secondary=tactic_faction_table,
        back_populates='tactics')

    def __str__(self):
        return self.name
class Roster(Base):
    __tablename__ = 'roster'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    player_name = Column(Text)

    factions = relationship('Faction', secondary=roster_faction_table, back_populates='rosters', lazy='subquery')
    entries = relationship('RosterEntry', cascade='delete', lazy='subquery')

    def __str__(self):
        return self.name

    @property
    def points(self):
        return sum(e.points for e in self.entries)

class RosterEntry(Base):
    __tablename__ = 'rosterentry'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    figure_id = Column(Integer, ForeignKey('figure.id'))
    figure = relationship('Figure', lazy='subquery')

    specialization_id = Column(Integer, ForeignKey('specialization.id'))
    specialization = relationship('Specialization', lazy='subquery')

    roster_id = Column(Integer, ForeignKey('roster.id'))
    roster = relationship('Roster')

    wargear = relationship(
        'Wargear',
        secondary=roster_entry_wargear_table,
        back_populates='roster_entries',
        lazy='subquery'
    )

    def __str__(self):
        return self.name


    @property
    def points(self):
        wargear_points = sum([ w.points if w.points else 0 for w in self.wargear ]) if self.wargear else 0
        figure_points = self.figure.points if self.figure.points else 0
        return wargear_points + figure_points

class Faction(Base):
    __tablename__ = 'faction'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    keyword_id = Column(Integer, ForeignKey('keyword.id'))
    keyword = relationship('Keyword')

    is_subfaction = Column(Boolean, default=False)

    abilities = relationship('Ability', secondary=faction_ability_table, back_populates='factions', lazy='subquery')
    figures = relationship(
        'Figure', secondary=figure_faction_table,
        back_populates='factions'
    )
    tactics = relationship('Tactic',
        secondary=tactic_faction_table,
        back_populates='factions')

    rosters = relationship('Roster',
        secondary=roster_faction_table,
        back_populates='factions')

    def __str__(self):
        return self.name