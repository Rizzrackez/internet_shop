from django import forms
from django.utils import timezone
from ecomapp.models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'buying_type', 'address', 'comments']

    last_name = forms.CharField(required=False)
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(initial='Самовывоз')
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['phone'].label = 'Телефон'
        self.fields['phone'].help_text = 'Пожалуйста указывайте ваш действительный номер телефона!'
        self.fields['buying_type'].label = 'Способ получения'
        self.fields['address'].label = 'Адрес доставки'
        self.fields['address'].help_text = 'Обязательно указывайте город!'
        self.fields['comments'].label = 'Комментарий к заказу'
        self.fields['date'].label = 'Дата доставки'

