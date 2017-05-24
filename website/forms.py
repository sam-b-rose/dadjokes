from django import forms

# our new form
class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Subject',
        required=False,
        widget=forms.TextInput(attrs={'class' : 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.TextInput(attrs={'class' : 'form-control'})
    )
    message = forms.CharField(
        label='Message',
        required=True,
        widget=forms.Textarea(attrs={'class' : 'input-lg form-control'})
    )