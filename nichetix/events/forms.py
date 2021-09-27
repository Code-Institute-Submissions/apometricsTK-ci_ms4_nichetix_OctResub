from django import forms

from .models import Event, Location
from .widgets import CustomClearableFileInput


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description_short",
            "description_long",
            "description_host",
            "location",
            "date_start",
            "date_end",
            "foreign_url",
            "image",
            "image_url",
        ]

        widgets = {
            "date_start": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"}),
            "date_end": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    image = forms.ImageField(label="Image", required=False, widget=CustomClearableFileInput)

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["location"].queryset = Location.objects.filter(owner=user)

        # todo: datetime-local has only ~86% global coverage!
        """
        https://caniuse.com/?search=datetime.local
        global coverage of input type datetime-local >86%
        chrome doesn't populate fields correctly
        
        Since v93 Firefox datetime-local with date picker, time picker still missing       
        datetime-local has no firefox implementation! 
        https://bugzilla.mozilla.org/show_bug.cgi?id=1283388
        They are working on it (nightly)
        https://bugzilla.mozilla.org/show_bug.cgi?id=1726108
        
        Bootstrap5 compatibility?
        https://github.com/monim67/django-bootstrap-datepicker-plus/pull/62
        
        Javascript ? maybe;
        https://github.com/Eonasdan/tempus-dominus / https://getdatepicker.com/

        https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#splitdatetimewidget
                
        "date_end": {forms.SplitDateTimeWidget(date_attrs={"type": "date"},
                                                   time_attrs={"type": "time"},
                                                   )},
        
        Must be used with SplitDateTimeField rather than DateTimeField!
        """


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            "name",
            "google_places_id",
            "street_address1",
            "street_address2",
            "town_or_city",
            "county",
            "postcode",
            "country",
            "foreign_url",
            "phone_number",
            "email",
        ]
