from django import forms
from phonenumber_field.formfields import PhoneNumberField
import datetime

from api.models import Tracker


class TrackerForm(forms.ModelForm):
    module_id = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        label='Module Id'
    )
    lat = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label='Destination Latitude'
    )
    lon = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label='Destination Longitude'
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=10,
        required=False,
        label='Password'
    )
    selection = (('True', 'True'), ('False', 'False'))
    tracked = forms.ChoiceField(
        choices=selection,
        label='Track the tracker?'
    )
    locked = forms.ChoiceField(
        choices=selection,
        label='Is the tracker locked?'
    )
    contact_num = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}), label="Contact number",
                                 required=False, help_text='+ Country Code 11 digit phone'
                                                           'e.g. +8801XXXXXXXXX')

    class Meta:
        model = Tracker
        fields = ['module_id', 'lat', 'lon', 'password', 'tracked', 'locked', 'contact_num']
