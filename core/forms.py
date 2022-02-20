from django import forms 
from .models import Item
 
class EmployeeRegistration(forms.ModelForm):
    class Meta:
        model = Item
        fields =[ 'sid', 'testname', 'testcode', 'price'] 