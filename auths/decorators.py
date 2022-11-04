from django.shortcuts import HttpResponseRedirect, reverse


def anonymous_required(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard'))
        return func(request, *args, **kwargs)
    return wrap
