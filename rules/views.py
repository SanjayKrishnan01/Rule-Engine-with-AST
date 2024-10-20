from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseBadRequest
from .models import Rule
from .forms import RuleForm, EvaluationForm, CombineRulesForm
from .rule_engine import create_rule, evaluate_rule
import json
import logging

logger = logging.getLogger(__name__)

class RuleListView(View):
    def get(self, request):
        rules = Rule.objects.all()
        form = RuleForm()
        combine_form = CombineRulesForm()
        return render(request, 'rules/rule_list.html', {'rules': rules, 'form': form, 'combine_form': combine_form})

    def post(self, request):
        form = RuleForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('rule_list')

class CombineRulesView(View):
    def post(self, request):
        form = CombineRulesForm(request.POST)
        if form.is_valid():
            rule_ids = form.cleaned_data['rule_ids']
            operator = form.cleaned_data['operator']
            rules = Rule.objects.filter(id__in=rule_ids)
            
            if len(rules) < 2:
                return HttpResponseBadRequest("Please select at least two rules to combine.")
            
            # Create a nested structure for combined rules
            combined_rule_string = f" {operator} ".join([f"({rule.rule_string})" for rule in rules])
            combined_rule_name = f"Combined Rule ({', '.join([rule.name for rule in rules])})"
            
            new_rule = Rule.objects.create(name=combined_rule_name, rule_string=combined_rule_string)
            
            return redirect('rule_list')
        
        return HttpResponseBadRequest("Invalid form submission.")


class RuleEvaluationView(View):
    def get(self, request):
        form = EvaluationForm()
        return render(request, 'rules/rule_evaluation.html', {'form': form})

    def post(self, request):
        form = EvaluationForm(request.POST)
        result = None
        error_message = None
        if form.is_valid():
            rule = form.cleaned_data['rule']
            data_str = form.cleaned_data['data']
            try:
                logger.debug(f"Rule string: {rule.rule_string}")
                logger.debug(f"Data: {data_str}")
                ast = create_rule(rule.rule_string)
                result = evaluate_rule(ast, data_str)
                logger.debug(f"Final result: {result}")
            except json.JSONDecodeError:
                error_message = "Invalid JSON data. Please check your input."
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                logger.exception("Error during rule evaluation")
        else:
            error_message = "Invalid form submission. Please check your inputs."
        
        context = {
            'form': form,
            'result': result,
            'error_message': error_message
        }
        return render(request, 'rules/rule_evaluation.html', context)