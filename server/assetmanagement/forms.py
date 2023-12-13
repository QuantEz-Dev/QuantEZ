from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['author', 'subject', 'content', 'bond', 'fund', 'etf', 'etc', 'create_date', 'modify_date']