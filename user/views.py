from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from reservation.models import Reservation,Customer
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.

#personalized form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class VRegister(View):

    def get(self,request):
        form= CustomUserCreationForm()
        return render(request,'users/authentication.html',{"form":form})
    def post(self,request):
        form= CustomUserCreationForm(request.POST)
        if form.is_valid():
            
            user= form.save()
            login(request,user)
            return redirect('Home')
        else:
            for error in form.error_messages:
                messages.error(request,form.error_messages[error])

            return render(request,'users/authentication.html',{"form":form})    


def log_out(request):
        logout(request)
        return redirect('Home')

def log_in(request):
    if request.method== "POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('Home')
            else:
                messages.error(request,"User and password do not match")
        else:
            messages.error(request,"User or password no valid")            
    form=AuthenticationForm()
    return render(request,'users/login_form.html',{"form":form})

@login_required
def customer_profile(request):
    customer = get_object_or_404(Customer, user=request.user)
    reservations = Reservation.objects.filter(customer=customer).order_by('-created')

    context = {
        'customer': customer,
        'reservations': reservations,
    }
    return render(request, 'users/customer_profile.html', context)

@login_required
def customer_reservations(request):
    customer = get_object_or_404(Customer, user=request.user)
    reservations = Reservation.objects.filter(customer=customer).order_by('-created')

    context = {
        'customer': customer,
        'reservations': reservations,
        'today':date.today(),
    }
    return render(request, 'users/customer_reservations.html', context)
