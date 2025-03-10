from PIL.ImagePalette import wedge
from django import forms
from .models import Comment,Post,User


class TicketForm(forms.Form):
    SUBJECT_CHOICES=(
        ('پیشنهاد','پیشنهاد'),
        ('انتقاد','انتقاد'),
        ('گزارش','گزارش'),
    )
    message=forms.CharField(widget=forms.Textarea, required=True ,label=" پیام")#تورو بودن یعنی این فیلد اجباری هست
    name=forms.CharField(max_length=250, required=True, label="اسم ")
    email=forms.EmailField(label=" ایمیل")
    phone=forms.CharField(max_length=11, required=True, label="شماره تلفن")
    subject=forms.ChoiceField(choices=SUBJECT_CHOICES, label="موضوع ")

    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عددی نیست!!")
            else:
                return phone


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name=self.cleaned_data['name']
        if name:
            if len(name)<3:
                raise forms.ValidationError("نام کوتاه است.")
            else:
                return name


    class Meta:
        model=Comment
        fields=['name','body']
        widgets={
            'body':forms.TextInput(attrs={
                'placeholder':"متن",
                'class':'cm-body'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': "نام",
                'class': 'cm-name'
            })
        }

class SearchForm(forms.Form):
    query=forms.CharField()


class CreatePostForm(forms.ModelForm):
    image1=forms.ImageField(label="تصویر اول")
    image2 = forms.ImageField(label="تصویر دوم")
    class Meta:
        model= Post
        fields=['title','description','reading_time']

# class LoginForm(forms.Form):
#     username=forms.CharField(max_length=250,required=True)
#     password=forms.CharField(max_length=250,required=True, widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(max_length=20,widget=forms.PasswordInput,label='password')
    password2=forms.CharField(max_length=20,widget=forms.PasswordInput,label='repeat password')

    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('پسورد ها مطابقت ندارند!')
        return cd['password2']


