import csv

from django.db.models import Q
from netaddr import IPNetwork, IPAddress
from django.conf import settings


# Check if connection comes from internal IP range
from api.models import TranslationTag


def is_internal(client_ip):
    for ip_range in settings.INTERNAL_IP_RANGES:
        if IPAddress(client_ip) in IPNetwork(ip_range):
            return True
    return False


def _clean_syn(syns):
    return [syn.strip() for syn in syns if syn]


def tag_loader(tag_csv_file):
    """
    loads a table with tags.

    Preferred Term (alle obligatorisch) und Synonyme

    The structure of the csv must be:

    tag_de,tag_en,tag_fr,,syn_de,syn_de,syn_de,syn_en,syn_en,syn_en,syn_fr,syn_fr,syn_fr

    3 preferred terms (one in each language), an empty row followed by optional synonyms

    Example:

        Areal,area,surface,Gebiet,Fläche,Grundstück,plot,,,régions,areal,intrigue

    :param tag_csv: the path to the csv
    :return: Nothing
    """
    with open(tag_csv_file) as tag_file:
        tag_reader = csv.reader(tag_file, delimiter=',', quotechar='"')
        for index, row in enumerate(tag_reader):
            if index != 0:
                tag_de, tag_en, tag_fr, _, *syn = row
                syn_de = _clean_syn(syn[0:3])
                syn_en = _clean_syn(syn[3:6])
                syn_fr = _clean_syn(syn[6:9])
                TranslationTag.objects.filter(
                    Q(tag_de=tag_de) | Q(tag_en=tag_en) | Q(tag_fr=tag_fr)
                ).delete()

                TranslationTag.objects.create(
                    tag_de=tag_de,
                    tag_en=tag_en,
                    tag_fr=tag_fr,
                    tag_alternatives_de=syn_de,
                    tag_alternatives_en=syn_en,
                    tag_alternatives_fr=syn_fr,
                )
                print(tag_de, tag_en, tag_fr, syn_de, syn_fr, syn_en)
