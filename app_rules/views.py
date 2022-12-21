from django.shortcuts import render


def our_values_page(request):
    return render(request, 'app_rules/our_values.html')


def rules_page(request):
    content = open('documents/content.txt', 'r', encoding='utf-8')
    lines = content.readlines()
    return render(request, 'app_rules/rules.html', {'lines': lines})


def privacy_policy_page(request):
    return render(request, 'app_rules/privacy_policy.html')
