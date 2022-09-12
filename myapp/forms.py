from pickle import TRUE
from django import forms 

class customerupdateform(forms.Form):
    account=forms.CharField(max_length=30,min_length=5,initial='',label='account',required=True)
    password=forms.CharField(min_length=2,initial='',required=True)
class dishupdateform(forms.Form):
    dish=forms.CharField(max_length=30,min_length=5,initial='',label='dish',required=True)
    price=forms.IntegerField(min_value=0,max_value=9999,required=True,label="price")
