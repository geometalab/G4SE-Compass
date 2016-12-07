import tempfile
import zipfile

from django.core.exceptions import ValidationError
from django import forms

from api.jobs import extract_xml_paths
from api.models import GeoVITeImportData


class GeoVITeImportDataAdminForm(forms.ModelForm):
    def clean_xml_zip(self):
        file = self.cleaned_data.get("xml_zip", None)
        if file is None:
            return
        with tempfile.NamedTemporaryFile() as possible_zip_file:
            possible_zip_file.write(file.read())
            if not zipfile.is_zipfile(possible_zip_file.name):
                raise ValidationError("File is not a zip-file.")
            with tempfile.TemporaryDirectory() as temp_dir:
                geovite_zip = zipfile.ZipFile(possible_zip_file.name)
                paths = extract_xml_paths(geovite_zip, temp_dir)
                if not paths:
                    raise ValidationError("File does not contain xml data")
        return file

    class Meta:
        model = GeoVITeImportData
        fields = ['xml_zip']
