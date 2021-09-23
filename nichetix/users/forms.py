from django.contrib.auth import get_user_model, forms

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = {
            "company_name",
            "default_full_name",
            "default_street_address1",
            "default_street_address2",
            "default_postcode",
            "default_town_or_city",
            "default_county",
            "default_country",
            "default_email",
            "default_phone_number",
        }


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
