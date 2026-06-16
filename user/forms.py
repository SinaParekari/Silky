from django import forms
from user.models import User, Address
from phonenumber_field.formfields import PhoneNumberField as PhoneNumberFormField

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-blue-300 focus:shadow-[0_0_0_4px_rgba(59,130,246,0.1)] transition-all duration-500 placeholder:text-slate-400',
            'placeholder': 'مثال: 09123456789',
        }))
    
    password = forms.CharField(
                widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-blue-300 focus:shadow-[0_0_0_4px_rgba(59,130,246,0.1)] transition-all duration-500 placeholder:text-slate-400',
            'placeholder': '••••••••',
        }))
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':"w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-purple-300 focus:shadow-[0_0_0_4px_rgba(168,85,247,0.1)] transition-all duration-500 placeholder:text-slate-400",
            'placeholder':"رمز عبور"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':"w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-purple-300 focus:shadow-[0_0_0_4px_rgba(168,85,247,0.1)] transition-all duration-500 placeholder:text-slate-400",
            'placeholder':"تکرار رمز عبور"})
    )
    phone_number = PhoneNumberFormField(
        region='IR',
        error_messages = {                
            'required': 'این شماره الزامی است',
            'unique': 'این شماره قبلاً ثبت شده است',
            'invalid': 'شماره معتبر نیست',},

        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-purple-300 focus:shadow-[0_0_0_4px_rgba(168,85,247,0.1)] transition-all duration-500 placeholder:text-slate-400',
            'placeholder': 'شماره موبایل',
    }))

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email']
        error_messages = {
            'username': {
                'required': 'نام کاربری الزامی است',
                'unique': 'این نام کاربری قبلاً ثبت شده است',
            },
            'email': {
                'required': 'ایمیل الزامی است',
                'unique': 'این ایمیل قبلاً ثبت شده است',
                'invalid': 'ایمیل معتبر نیست',
            },
            'phone_number': {
                'unique': 'این شماره موبایل قبلاً ثبت شده است',
            },
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-purple-300 focus:shadow-[0_0_0_4px_rgba(168,85,247,0.1)] transition-all duration-500 placeholder:text-slate-400',
                'placeholder': 'نام کاربری',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-purple-300 focus:shadow-[0_0_0_4px_rgba(168,85,247,0.1)] transition-all duration-500 placeholder:text-slate-400',
                'placeholder': 'ایمیل',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند')
        
        return cleaned_data

class ProfileForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        error_messages={'required': 'رمز عبور الزامی است'},
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
            'placeholder': 'رمز جدید (اختیاری)',
        })
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
            'placeholder': 'تکرار رمز جدید',
        })
    )

    phone_number = PhoneNumberFormField(
        region='IR',
        widget=forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'national_code', 'birth_date','avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'placeholder': 'نام',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'placeholder': 'نام خانوادگی',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
            }),
            'national_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'type': 'date',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password != password2:
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند')

        return cleaned_data
    
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['province', 'city', 'address', 'building_number', 'unit', 'postal_code', 'is_default']

        widgets = {
            'province': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm',
                'id': 'province-select'
            }),
            'city': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm',
                'id': 'city-select'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'placeholder': 'آدرس کامل'
            }),
            'building_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'placeholder': 'پلاک'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'placeholder': 'واحد (اختیاری)'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'placeholder': 'کد پستی'
            }),
        }