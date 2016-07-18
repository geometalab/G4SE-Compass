from api.models import AllRecords, Record
from rest_framework.test import APITestCase
import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database')
class TestListViews(APITestCase):

    def test_record_list(self):
        record_list = self.client.get('/api/')
        assert 'Schweiz' in record_list.data[0].values()
        assert 'Zürich' in record_list.data[2].values()

    def test_internal_record_detail(self):
        record = self.client.get('/api/123455/')
        assert 'Schweiz' in record.data.values()

    def test_harvested_record_detail(self):
        record = self.client.get('/api/12380/')
        assert 'Zürich' in record.data.values()

    def test_search(self):
        result_list = self.client.get('/api/search/?query=Zürich')
        for result in result_list.data:
            assert 'Zürich' in result.values()


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database', 'test_user')
class TestAuthentication(APITestCase):

    def test_authenticate(self):
        assert self.client.login(username='admin', password='securepassword')
        self.client.logout()
        assert self.client.login(username='admin', password='wrongpassword') == False


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('setup_database', 'test_user')
class TestBackendViews(APITestCase):

    def test_internal_records_list(self):
        self.client.login(username='admin', password='securepassword')
        result_list = self.client.get('/api/edit/')
        assert len(result_list.data) == 2

    def test_insert_record(self):
        data = {
            "identifier": "1234567",
            "language": "de",
            "content": "Topologisches Landschaftsmodell TLM, Fliessgewässer",
            "abstract": "swissTLM3D ist das grossmassstäbliche Topografische Landschaftsmodell der Schweiz. Es umfasst die natürlichen und künstlichen Objekte wie auch die Namendaten in vektorieller Form. Mit einer hohen Genauigkeit und dem Einbezug der dritten Dimension ist swissTLM3D der genaueste und umfassendste 3D-Vektordatensatz der Schweiz. In dieser Feature Class werden die Fliessgewässer in linearer Form geführt. Die Linien sind in Richtung des Gewässerflusses gerichtet.",
            "publication_year": 2012,
            "publication_lineage": "2015, 2014, 2012",
            "geography": "Schweiz",
            "extent": "BOX(5.9335 45.7785,10.6891 47.839)",
            "geodata_type": "vector",
            "source": "Swisstopo",
            "metadata_link": "http://www.swisstopo.admin.ch/internet/swisstopo/de/home/products/landscape/swissTLM3D.parsysrelated1.47641.downloadList.97108.DownloadFile.tmp/201603swisstlm3d14okd.pdf",
            "access_link": "https://geodata4edu.hsr.ch/geodata/rest/services/swissTLM3D/TLM_FLIESSGEWAESSER/FeatureServer",
            "base_link": "https://geodata4edu.hsr.ch/geodata/rest/services/swissTLM3D/TLM_FLIESSGEWAESSER/FeatureServer",
            "collection": "/swissTLM3D/",
            "dataset": "TLM_FLIESSGEWAESSER",
            "arcgis_layer_link": "https://geodata4edu.hsr.ch/share/TLM_FLIESSGEWAESSER.pitem",
            "qgis_layer_link": "",
            "arcgis_symbology_link": "https://geodata4edu.hsr.ch/share/TLM_FLIESSGEWAESSER.lyr",
            "qgis_symbology_link": "https://geodata4edu.hsr.ch/share/TLM_FLIESSGEWAESSER_QGIS.zip",
            "service_type": "FeatureService",
            "crs": "EPSG:21781",
            "term_link": "http://www.swisstopo.admin.ch/internet/swisstopo/de/home/swisstopo/legal_bases/copyright.html",
            "proved": "2015-03-04",
            "visibility": "public",
            "login_name": ""
        }

        records_before_insert = AllRecords.objects.all().count()
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        self.client.post('/api/edit/', data, format='json')
        assert AllRecords.objects.all().count() == records_before_insert + 1
        # Cleanup
        Record.objects.filter(content='Topologisches Landschaftsmodell TLM, Fliessgewässer').delete()
