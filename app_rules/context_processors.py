from .models import RulesModel


def render_rules_list(request):
    rules_list = RulesModel.objects.all()
    return {'rules_list': rules_list}
