""" Runs oai-harvest command in shell and reads all xml files.
Deletes all previous records and writes the new ones into the database.
Database URI must be set in a file settings.py in the src directory (e.g. password:user@localhost:5432/database)
"""
import os
import sys
import xml.etree.ElementTree as ET

from sqlalchemy import create_engine, Column, Integer, String, Text, Date, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings

Base = declarative_base()


class Record(Base):
    __tablename__ = "records"

    identifier = Column(String, primary_key=True)
    language = Column(String)
    content = Column(String)
    abstract = Column(Text)
    publication_year = Column(Integer)
    publication_lineage = Column(String)
    geography = Column(String)
    extent = Column(String)
    geodata_type = Column(String)
    source = Column(String)
    metadata_link = Column(String)
    access_link = Column(String)
    base_link = Column(String)
    collection = Column(String)
    dataset = Column(String)
    arcgis_layer_link = Column(String)
    qgis_layer_link = Column(String)
    arcgis_symbology_link = Column(String)
    qgis_symbology_link = Column(String)
    service_type = Column(String)
    crs = Column(String)
    term_link = Column(String)
    proved = Column(Date)
    visibility = Column(String)
    modified = Column(TIMESTAMP)
    login_name = Column(String)


def read_records(target_dir):
    records = []
    for fn in os.listdir(target_dir):
        tree = ET.parse(target_dir + '/' + fn)
        root = tree.getroot()
        record = {}
        for child in root:
            content = child.text
            tag = child.tag.split('}', 1)[1]
            record[tag] = content
        records.append(record)
    return records


def insert_records_into_db(records):
    engine = db_connect()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session.query(Record).delete()
    for record in records:
        db_record = Record(**record)
        session.add(db_record)
    session.commit()


def db_connect():
    return create_engine('postgresql://' + settings.DATABASE_URL)


def harvest():
    os.system('oai-harvest all')
    target_dir = sys.argv[1]
    record_list = read_records(target_dir)
    insert_records_into_db(record_list)

if __name__ == "__main__":
    sys.exit(harvest())
