from django.http import HttpResponseForbidden

from django.shortcuts import redirect
from functools import wraps


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # 1. Если вообще не залогинен — на страницу входа
        if not request.user.is_authenticated:
            # Убедись, что в urls.py у тебя name='user_login'
            return redirect('user_login')

        # 2. Если залогинен, но НЕ админ (не staff) — на главную
        if not request.user.is_staff:
            # Убедись, что в urls.py у главной страницы name='main' (или 'home')
            return redirect('main')

            # 3. Если всё ок (залогинен и админ) — пускаем во вьюху
        return view_func(request, *args, **kwargs)

    return _wrapped_view