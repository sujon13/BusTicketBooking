from django import forms


class NameForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)


class SearchBus(forms.Form):
    start_station = forms.CharField(
        label='From',
        max_length=15,
        widget=forms.TextInput(
            attrs={'placeholder': 'From'}
        )
    )
    destination = forms.CharField(
        label='To',
        max_length=15,
        widget=forms.TextInput(
            attrs={'placeholder': 'To'}
        )
    )
    # date_of_journey = forms.DateField(
    #    label='Date of Journey',
    #    widget=forms.widgets.DateInput(
    #        attrs={'type': 'date'}
    #    )
    # )
    date_of_journey = forms.CharField(
        label='Date of Journey',
        max_length=15,
        widget=forms.TextInput(
            attrs={'placeholder': 'Pick a date'}
        )
    )



