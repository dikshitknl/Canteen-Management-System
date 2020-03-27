from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, ListView, DeleteView, UpdateView, FormView, RedirectView
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from .models import Person, MenuItem, Order, Bill
from django.urls import reverse_lazy
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import datetime

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(TemplateView):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'login.html')

    @staticmethod
    def post(request):
        form_data = request.POST
        username = form_data.get('username', None)
        password = form_data.get('password', None)
        next_url = form_data.get(
            'next', None) if form_data.get('next') else '/'
        if not username and password:
            return render(request, 'login.html', {'message': "* Invalid User"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'message': "* Invalid Username or password"})


class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(TemplateView):
    template_name = "index.html"

    @staticmethod
    def post(request):
        form_data = request.POST
        phone = form_data.get('phone', None)
        empId = form_data.get('empId', None)
        try:
            person = Person.objects.get(phone=phone, empNum=empId)
            return redirect('create-order', person.id)
        except Person.DoesNotExist:
            return render(request, 'index.html', {'message': "This phone and employee Id has no association. May be ask to register yourself."})


# Person CRUD..................................................
class PersonCreateView(CreateView):
    model = Person
    template_name = 'person/create.html'
    fields = ('empNum', 'name', 'gender', 'designation', 'phone')
    success_url = reverse_lazy('list-person')


class PersonListView(ListView):

    model = Person
    template_name = 'person/list.html'
    context_object_name = 'persons'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        persons = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(persons, self.paginate_by)
        try:
            persons = paginator.page(page)
        except PageNotAnInteger:
            persons = paginator.page(1)
        except EmptyPage:
            persons = paginator.page(paginator.num_pages)
        context['persons'] = persons
        return context


class PersonUpdateView(UpdateView):

    model = Person
    template_name = 'person/update.html'
    context_object_name = 'person'
    fields = ('name', 'gender', 'designation')

    def get_success_url(self):
        return reverse_lazy('list-person')


class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'person/delete.html'
    success_url = reverse_lazy('list-person')


# Menu Item CRUD...............................................

class MenuCreateView(CreateView):
    model = MenuItem
    template_name = 'menuItem/create.html'
    fields = ('name', 'price', 'is_available',
              'preparation_time', 'options')
    success_url = reverse_lazy('list-menu')


class MenuListView(ListView):

    model = MenuItem
    template_name = 'menuItem/list.html'
    context_object_name = 'menus'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(MenuListView, self).get_context_data(**kwargs)
        menus = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(menus, self.paginate_by)
        try:
            menus = paginator.page(page)
        except PageNotAnInteger:
            menus = paginator.page(1)
        except EmptyPage:
            menus = paginator.page(paginator.num_pages)
        context['menus'] = menus
        return context


class MenuUpdateView(UpdateView):

    model = MenuItem
    template_name = 'menuItem/update.html'
    context_object_name = 'menu'
    fields = ('is_available',
              'preparation_time')

    def get_success_url(self):
        return reverse_lazy('list-menu')


class MenuDeleteView(DeleteView):
    model = MenuItem
    template_name = 'menuItem/delete.html'
    success_url = reverse_lazy('list-menu')


# create order
@method_decorator(csrf_exempt, name='dispatch')
class OrderCreateView(TemplateView):
    template_name = 'order/create.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        person = Person.objects.get(id=kwargs.get('id'))
        context['menus'] = MenuItem.objects.filter(is_available=True)
        context['user'] = person
        now = datetime.datetime.now()
        orders = Order.objects.filter(
            user=person, time_issued__date=now.date())
        sumAmt = 0
        for order in orders:
            amount = order.quantity * order.menu_item.price
            sumAmt += amount
            order.billAmount = amount
        context['orders'] = orders
        context['billSum'] = sumAmt
        return context

    @staticmethod
    def post(request):
        form_data = request.POST
        menu_item = MenuItem.objects.get(id=form_data['menu'])
        order = Order.objects.create(
            user=Person.objects.get(empNum=form_data['empId']),
            menu_item=menu_item,
            quantity=form_data['qty'],
            additional=form_data['additional']
        )
        order.save()
        bill = Bill.objects.create(
            order=order,
            total_amount=int(form_data['qty'])*int(menu_item.price)
        )
        bill.save()
        return HttpResponse("Your Order has been Placed. The bill amount for order no. "+str(bill.order.id)+" is Rs. "+str(bill.total_amount))


class OrderListView(ListView):

    model = Order
    template_name = 'order/list.html'
    context_object_name = 'orders'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        orders = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(orders, self.paginate_by)
        try:
            menus = paginator.page(page)
        except PageNotAnInteger:
            menus = paginator.page(1)
        except EmptyPage:
            menus = paginator.page(paginator.num_pages)
        context['orders'] = orders
        return context


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order/delete.html'
    success_url = reverse_lazy('list-order')


class OrderCancelView(DeleteView):
    model = Order
    template_name = 'order/delete.html'
    success_url = reverse_lazy('index')


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order/update.html'
    context_object_name = 'order'
    fields = ('is_fulfilled',)

    def get_success_url(self):
        return reverse_lazy('list-order')
