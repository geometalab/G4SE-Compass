import sys
import xml.etree.ElementTree as ET
from urllib import request
import csv
import io
import os

from sqlalchemy import create_engine, Column, Integer, String, Text, Date, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings

WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
Base = declarative_base()


class Record(Base):
    __tablename__ = "harvested_records"

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


def read_xml(url):
    tree = ET.ElementTree(file=request.urlopen(settings.FILESHARE_URL + url))
    root = tree.getroot()
    record = {}
    for child in root:
        content = child.text
        tag = child.tag.split('}', 1)[1]
        record[tag] = content
    return record


def read_csv(file):
    reader = csv.reader(io.TextIOWrapper(file), delimiter=' ')
    return list(reader)


def save_new_data_index():
    request.urlretrieve(settings.FILESHARE_URL + "/metadata.csv", os.path.join(WORKING_DIRECTORY, 'new_index.csv'))


def get_data_from_index(filename):
    with open(os.path.join(WORKING_DIRECTORY, filename)) as file:
        reader = csv.DictReader(file, delimiter=' ')
        index = list(reader)
    return index


def create_new_record(record_name, modified):
    data = read_xml(record_name)
    data['modified'] = modified
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    db_record = Record(**data)
    session.add(db_record)
    session.commit()


def update_record(record_name, modified):
    data = read_xml(record_name)
    data['modified'] = modified
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(Record).filter(Record.identifier == data['identifier']).update(data)
    session.commit()


def delete_record(record_name):
    id = record_name.split('.')[0]
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(Record).filter(Record.identifier == 'oai:geovite.ethz.ch:' + id).delete()
    session.commit()


def update_diff(new_index, old_index):
    for new_element in new_index:
        found = None
        for old_element in old_index:
            if new_element['Name'] == old_element['Name']:
                found = old_element
                break
        if found:
            if new_element['Last_modified'] != found['Last_modified']:
                if new_element['Status'] == '[Valid]':
                    update_record(new_element['Name'], new_element['Last_modified'])
                elif new_element['Status'] == '[Deleted]':
                    delete_record(new_element['Name'])
        else:
            if new_element['Status'] != '[Deleted]':
                create_new_record(new_element['Name'], new_element['Last_modified'])
    return new_index, old_index


def db_connect():
    return create_engine(settings.DATABASE_URL)


def harvest():
    save_new_data_index()
    new_index = get_data_from_index('new_index.csv')
    old_index = get_data_from_index('old_index.csv')
    update_diff(new_index, old_index)
    old_index_file_path = os.path.join(WORKING_DIRECTORY, 'old_index.csv')
    index_file_path = os.path.join(WORKING_DIRECTORY, 'new_index.csv')
    os.remove(old_index_file_path)
    os.rename(index_file_path, old_index_file_path)


if __name__ == "__main__":
    sys.exit(harvest())
