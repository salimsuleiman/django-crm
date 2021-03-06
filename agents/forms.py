from django import forms
from leads.models import Agent, User


class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','username', 'first_name', 'last_name')

