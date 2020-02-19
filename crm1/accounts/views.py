from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else: 
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {
            'form': form
        }

        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}

        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    totalCustomers = customers.count()
    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'totalCustomers': totalCustomers,
        'totalOrders': totalOrders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()

    context = {
        'products' : products
    }

    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
def customers(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    totalOrders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'totalOrders': totalOrders,
        'myFilter': myFilter
    }

    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login')
def createOrder(request, pk):
    # Pasar modelo padre e hijo
    # Extra indica cuantos forms quieres
    OrderFormSet = inlineformset_factory(Customer, Order, 
    fields=('product', 'status'), extra=2)
    customer = Customer.objects.get(id=pk)
    # Para no poner los valores que ya tienes queryset
    formSet = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # print('printing: ', request.POST)
        # form = OrderForm(request.POST)
        formSet = OrderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('/')

    context = {
        # 'orderForm': form
        'formSet': formSet
    }

    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    # llena tu form con la instancia de la busqueda
    form = OrderForm(instance=order);

    if request.method == 'POST':
        # Modifica la instancia en lugar de crear otra
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'orderForm': form
    }


    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    print(order)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'order': order
    }


    return render(request, 'accounts/delete.html', context)