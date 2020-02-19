from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filters import *

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

def products(request):
    products = Product.objects.all()

    context = {
        'products' : products
    }

    return render(request, 'accounts/products.html', context)
    
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