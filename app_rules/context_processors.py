from .models import RulesModel, PrivacyPolicyModel


def render_rules_list(request):
    rules_list = RulesModel.objects.all()
    privacy = PrivacyPolicyModel.objects.all()
    return {'rules_list': rules_list, 'privacy': privacy}
