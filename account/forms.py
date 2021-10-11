from django import forms
from .models import User, Address

error = {
    'required': 'این فیلد اجباری است',
    'invalid': 'ایمیل وارد شده نامعتبر است'
}


class UserRegisterForm(forms.Form):
    email = forms.EmailField(max_length=50, error_messages=error,
                             widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}))
    password_1 = forms.CharField(max_length=50, error_messages=error,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'پسورد'}))
    password_2 = forms.CharField(max_length=50, error_messages=error,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'تکرار پسورد'}))
    phone_number = forms.IntegerField(widget=forms.PasswordInput(attrs={'placeholder': 'تلفن همراه'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('ایمیل تکراری است')
        return email

    def clean_password_2(self):
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']
        if password_1 != password_2:
            raise forms.ValidationError('پسوردها برابر نیستند.')
        elif len(password_2) < 8:
            raise forms.ValidationError('پسورد باید حداقل 9 کاراکتر باشد.')
        elif not any(x.isupper() for x in password_2):  # Checks to have at least one capital letter
            raise forms.ValidationError('پسورد شما باید حداقل شامل یک حرف بزرگ باشد.')
        return password_2


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=50)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'نام',
                                             'class': 'mb-2 text-center'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی',
                                                         'class': 'mb-2 text-center'}),
            'email': forms.TextInput(attrs={'placeholder': 'ایمیل',
                                                     'class': 'mb-2 text-center'}),
            'phone_number': forms.NumberInput(attrs={'placeholder': 'تلفن همراه',
                                                     'class': 'mb-2 text-center'
                                                     }),
        }
        labels = {
            key: '' for key in ['first_name', 'last_name', 'email', 'phone_number']
        }


class CreateAddressForm(forms.ModelForm):
    # is_dafault= forms.BooleanField(widget=forms.CheckboxInput)
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'state': forms.TextInput(attrs={'placeholder': 'استان',
                                                 'class': 'mb-2 text-center'}),
            'city': forms.TextInput(attrs={'placeholder': 'شهر',
                                                'class': 'mb-2 text-center'}),
            'address': forms.Textarea(attrs={'placeholder': 'ادامه آدرس',
                                            'class': 'mb-2 text-center'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'کد پستی',
                                                     'class': 'mb-2 text-center'
                                                     }),
        }
        labels = {
            key: '' for key in ['state', 'city', 'address', 'postal_code']
        }


class EditAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['user']















