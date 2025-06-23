from nxt.security.forms import UserCompanyForm


def company_form(request):
    if request.user.is_authenticated:
        return {
            'company_form': UserCompanyForm(instance=request.user),
        }
    return {}
