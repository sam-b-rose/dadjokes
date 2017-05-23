from django import forms

# our new form
class ContactForm(forms.Form):
    contact_subject = forms.CharField(label='subject', required=False)
    contact_email = forms.EmailField(label='email', required=True)
    content = forms.CharField(
        label='message',
        required=True,
        widget=forms.Textarea
    )