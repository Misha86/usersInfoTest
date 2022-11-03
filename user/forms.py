from django import forms


class UploadFileForm(forms.Form):
    file_csv = forms.FileField(widget=forms.FileInput(attrs={'accept': '.csv'}))
    file_xml = forms.FileField(widget=forms.FileInput(attrs={'accept': '.xml'}))
