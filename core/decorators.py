from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'ADMIN':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Or show error page
    return wrapper

def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'STAFF':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper

def driver_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'DRIVER':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper
