from django.urls import path
from .views import RuleListView, RuleEvaluationView, CombineRulesView

urlpatterns = [
    path('', RuleListView.as_view(), name='rule_list'),
    path('evaluate/', RuleEvaluationView.as_view(), name='rule_evaluation'),
    path('combine/', CombineRulesView.as_view(), name='combine_rules'),
]
