from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import TicketType


class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = [
            "name",
            "description_long",
            "sale_start",
            "sale_end",
            "quota",
            "price_net",
            "tax",
        ]

        # Custom to work with DateTimePicker, needs customized "_clean_fields(self)" beyond
        widgets = {
            "sale_start": forms.widgets.DateTimeInput(format="%d-%m-%Y %H:%M %z",
                                                      attrs={"type": "text",
                                                             "id": "datetimepicker-start",
                                                             "class": "datetimepicker",
                                                             }),
            "sale_end": forms.widgets.DateTimeInput(format="%d-%m-%Y %H:%M %z",
                                                    attrs={"type": "text",
                                                           "id": "datetimepicker-end",
                                                           "class": "datetimepicker",
                                                           }),
        }

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
