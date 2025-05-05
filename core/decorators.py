from django.shortcuts import redirect

#decorator checks if the user's role is ADMIN
def admin_required(view_func):
    def wrapper(request, *args, **kwargs): # func wraps the view_func and takes whatever arguments the view_func takes
        if request.user.role == 'ADMIN':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapper

#decorator checks if the user's role is STAFF
def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'STAFF':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper

#decorator checks if the user's role is DRIVER
def driver_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'DRIVER':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper
