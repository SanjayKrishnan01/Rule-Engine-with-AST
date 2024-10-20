from django import forms
from .models import Rule

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['name', 'rule_string']

class EvaluationForm(forms.Form):
    rule = forms.ModelChoiceField(queryset=Rule.objects.all())
    data = forms.CharField(widget=forms.Textarea, help_text="Enter JSON data")

    def clean_data(self):
        data = self.cleaned_data['data']
        try:
            import json
            json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON data")
        return data
    
class CombineRulesForm(forms.Form):
    rule_ids = forms.CharField(help_text="Enter comma-separated rule IDs")
    operator = forms.ChoiceField(choices=[('AND', 'AND'), ('OR', 'OR')], initial='AND')

    def clean_rule_ids(self):
        rule_ids = self.cleaned_data['rule_ids']
        ids = [id.strip() for id in rule_ids.split(',')]
        return ids