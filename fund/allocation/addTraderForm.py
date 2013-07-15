from django import forms

class addTraderForm(forms.Form):
    #tdealer = forms.CharField(max_length=30)
    #tState = forms.CharField(max_length=30)
    tID = forms.IntegerField()
    tAccount = forms.CharField(max_length=30)
    consignmentNo = forms.CharField(max_length=30)
    transactionNo = forms.CharField(max_length=30)
    transationAmount = forms.FloatField()
    transationPrice = forms.FloatField()
    tdate = forms.DateField(initial="yyyy-mm-dd")
    customerNumber = forms.IntegerField()