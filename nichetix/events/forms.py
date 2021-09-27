from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Event, Location
from .widgets import CustomClearableFileInput


class EventForm(forms.ModelForm):
    """
    Form to create and update events
    """
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

        # Custom to work with DateTimePicker, needs customized "_clean_fields(self)" beyond
        widgets = {
            "date_start": forms.widgets.DateTimeInput(format="%d-%m-%Y %H:%M %z",
                                                      attrs={"type": "text",
                                                             "id": "datetimepicker-start",
                                                             "class": "datetimepicker",
                                                             }),
            "date_end": forms.widgets.DateTimeInput(format="%d-%m-%Y %H:%M %z",
                                                    attrs={"type": "text",
                                                           "id": "datetimepicker-end",
                                                           "class": "datetimepicker",
                                                           }),

        }

    image = forms.ImageField(label="Image", required=False, widget=CustomClearableFileInput)

    def __init__(self, user, *args, **kwargs):
        """
        Let a user only select his own locations
        """
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["location"].queryset = Location.objects.filter(owner=user)

    def _clean_fields(self):
        """
        Customized cleaning of DateTimeField included
        https://cdf.9vo.lt/3.0/django.forms.models/ModelForm.html
        """
        for name, field in self.fields.items():
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, forms.FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)

                # this is custom to work with DateTimePicker, compare "static/js/datetimepicker-init.js"
                elif isinstance(field, forms.DateTimeField):
                    value = datetime.strptime(value, "%d-%m-%Y %H:%M %z")

                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                self.add_error(name, e)


class LocationForm(forms.ModelForm):
    """
    Form to create and update Locations
    """
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
