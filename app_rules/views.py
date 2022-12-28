from django.shortcuts import render

from .services import rules_service as rs


def our_values_page(request):
    return render(request, 'app_rules/our_values.html')


def rules_page(request):
    rules = rs.RuleService()
    return render(request, 'app_rules/rules.html', {'rules': rules})


def privacy_policy_page(request):
    return render(request, 'app_rules/privacy_policy.html')
