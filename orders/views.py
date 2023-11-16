from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created

def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # launch asynchronous tasks
            #order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect to payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                      'orders/order/create.html',
                      {'form':form,
                       'cart':cart})

