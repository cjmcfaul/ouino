from django import forms


class FeedbackForm(forms.Form):

    full_name = forms.CharField(
        max_length=150,
        label='Full Name'
    )
    email_address = forms.EmailField(
        label='E-mail Address'
    )
    email_2 = forms.CharField(
        max_length=500,
        label='',
        widget=forms.TextInput(attrs={'class': 'dispnon'}),
        required=False,
    )
    message = forms.CharField(
        label='Feedback',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 5})
    )