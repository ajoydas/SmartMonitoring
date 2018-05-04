from django import forms
from phonenumber_field.formfields import PhoneNumberField
import datetime

from api.models import Tracker


class TrackerForm(forms.ModelForm):
    module_id = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)
    lat = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    lon = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=10,
        required=False)
    selection = (('YES', 'Yes'), ('NO', 'No'))
    tracked = forms.ChoiceField(choices=selection)
    locked = forms.ChoiceField(choices=selection)
    contact_num = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}), label="Contact number",
                                 required=False, help_text='+ Country Code 11 digit phone\n'
                                                           'e.g. +8801XXXXXXXXX')

    class Meta:
        model = Tracker
        fields = ['module_id', 'lat', 'lon', 'password', 'tracked', 'locked', 'contact_num']
