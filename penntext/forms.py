from django import forms
from penntext.models import FlatPrice, UserProfile
from django.contrib.auth.models import User


class FlatPriceForm(forms.ModelForm):
    title = forms.CharField(help_text="Enter a title for the job")
    contact = forms.CharField(help_text="Enter 0 if you do not wish phone number to be revealed until job is accepted. Leave blank if you wish your number to be entered.", required=False)
    location = forms.CharField(help_text="Enter the location you wish to recieve the job-doer to end the transaction. Leave blank if you wish your address initially provided to be used.", required=False)
    description = forms.CharField(widget=forms.Textarea, help_text="Please describe the job.")
    costofjob = forms.IntegerField(help_text="Please enter the approximate cost of the job (ex: buying 1 can soda as job costs 75c, so put down 1")
    timeofjob = forms.IntegerField(help_text="Please enter approximate time the job might take (in minutes)")
    pricepaid = forms.DecimalField(help_text="Price you will pay for the job.")
    typeofpay = forms.IntegerField(help_text="Please enter 1 if you entered per hour payment, else leave blank (for flat price)", required=False)
    nopaymentafter = forms.CharField(help_text="Please enter time and date by when the job must be done (else payment void). Ex: September 5th, 14.30)")
    picture = forms.ImageField(help_text="Please upload a picture if you wish (Optional)", required=False)
    acceptedby = forms.CharField(widget=forms.HiddenInput(), required=False)
    completioncode = forms.IntegerField(widget= forms.HiddenInput(), required=False)
    class Meta:
        model = FlatPrice
        fields = ('title', 'contact', 'location', 'description', 'costofjob', 'timeofjob', 'pricepaid', 'typeofpay', 'nopaymentafter', 'picture')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text="Alphanumeric Only.")
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


    def clean_email(self):
        User.email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(("This email address is already in use. Please supply a different email address."))

        User.username = self.cleaned_data["username"]
        if not User.username.isalnum():
            raise forms.ValidationError(("Contains non-alphanumberic characters."))
     #   if not User.email.endswith(".upenn.edu"):
      #    raise forms.ValidationError(("Not a valid Penn email"))
        
        return self.cleaned_data['email']

class UserProfileForm(forms.ModelForm):
    phone =forms.IntegerField(help_text="Enter your phone number. This number will not be shown till job is accepted.")
    location = forms.CharField(help_text="This will be used as default if you do not mention where to meet you after your job is completed during job post")
    activation_key = forms.CharField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = UserProfile
        fields = ('activation_key', 'phone', 'location')
