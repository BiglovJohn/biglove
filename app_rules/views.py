from django.shortcuts import render


def our_values_page(request):
    return render(request, 'app_rules/our_values.html')


def rules_page(request):
    return render(request, 'app_rules/rules.html')


def privacy_policy_page(request):
    return render(request, 'app_rules/privacy_policy.html')
