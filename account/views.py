from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect
from .forms import *
from .models import User, Address, Customer, Admin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from order.models import OrderItem, Order
from django.db.models import Q
from book.models import Book, Category
from .mixins import SuperUserRequiredMixin
import jdatetime


# Create your views here.


class EmailToken(PasswordResetTokenGenerator):
    """
    This class returns a token consist of user's information and timestamp.
    For returning token in unicode format we use text_type function.
    """
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.id) + text_type(timestamp)


email_generator = EmailToken()


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(password=data['password_2'], email=data['email'],
                                            phone_number=data['phone_number'])
            user.is_active = False  # We will activate the user with email.
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))  # for encoding user's id.
            url = reverse('account:active', kwargs={'uidb64': uidb64, 'token': email_generator.make_token(user)})
            link = 'http://' + domain + url
            email = EmailMessage(
                'Active User',  # Email's subject
                link,  # Email's body
                'test<zgholami.22@gmail.com>',
                [data['email']]  # Email recipient
            )
            email.send(fail_silently=False)  # fail_silently() will raise an exception from smtplib.
            # messages.success(request, 'ثبت نام شما با موفقیت انجام شد', 'success')
            messages.warning(request, ' لطفا برای فعالسازی حساب کاربری به ایمیل خود مراجعه کنید.', 'warning')
            return redirect('book:home')
    else:
        form = UserRegisterForm()
    parent_categories = Category.objects.filter(is_sub_category=False)
    context = {'form': form, 'parent_categories': parent_categories}
    return render(request, 'account/register.html', context)


class RegisterEmail(View):
    """
    Activating user with email.
    uidb64 and token are created during the user's registration.
    """
    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('account:login')


def user_login(request):
    print('user_login_form')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            """
            To check if the user has already registered or not.
            """
            user = authenticate(request, email=data['email'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'ورود با موفقیت انجام شد', 'success')
                return redirect('book:home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است', 'danger')
        # else:
        #     print('form is not valid')
    else:
        form = UserLoginForm()
    parent_categories = Category.objects.filter(is_sub_category=False)
    return render(request, 'account/login.html', {'form': form, 'parent_categories': parent_categories})


def user_logout(request):
    logout(request)
    messages.success(request, 'خروج با موفقیت انجام شد', 'warning')
    return redirect('book:home')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # updating the session after changing password.
            messages.success(request, 'پسورد با موفقیت تفییر کرد', 'success')
            return redirect('account:profile')
        else:
            messages.error(request, 'پسورد درستی انتخاب نشده است.', 'danger')
            return redirect('account:change')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change.html', {'form': form})


class ForgetPassword(auth_views.PasswordResetView):
    """
    In this class, an email containing a link is send to user for reset the password.
    """
    template_name = 'account/forget.html'
    success_url = reverse_lazy('account:message_send_email')
    email_template_name = 'account/link_new_password.html'


class MessageSendEmail(auth_views.PasswordResetDoneView):
    template_name = 'account/message_send_email.html'


class ConfirmNewPassword(auth_views.PasswordResetConfirmView):
    template_name = 'account/confirm.html'
    success_url = reverse_lazy('account:complete_new_password')


class Complete_new_password(auth_views.PasswordResetCompleteView):
    template_name = 'account/complete_new_password.html'


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'account/edit_profile.html'
    success_url = reverse_lazy('book:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context


class CreateAddressView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = CreateAddressForm
    template_name = 'account/create_address.html'
    # success_url = reverse_lazy('account:edit_profile')

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('account:edit_profile', kwargs={'pk': user.pk})

    def form_valid(self, form):
        """
        This function handles the default address of the user.
        Each user can have only and only one default address.
        """
        form = form.save(commit=False)
        form.user = self.request.user
        if form.is_default:
            if Address.objects.filter(user=form.user).count() > 0:
                previous_default_address = Address.objects.get(user=form.user, is_default=True)
                previous_default_address.is_default = False
                previous_default_address.save()
        elif not form.is_default and Address.objects.filter(user=form.user, is_default=True).count() == 0:
            form.is_default = True
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context


def AvailableAddressesView(request, id):
    addresses = Address.objects.filter(user_id=id)
    parent_categories = Category.objects.filter(is_sub_category=False)
    return render(request, 'account/available_addresses.html', {'addresses': addresses,
                                                                'parent_categories': parent_categories})


@login_required()
def remove_address_view(request, id):
    url = request.META.get('HTTP_REFERER')  # for redirecting user to the current page
    user_addresses = Address.objects.filter(user_id=request.user.id).count()
    if user_addresses > 1:
        Address.objects.get(id=id).delete()
        return redirect(url)

    elif user_addresses == 1:
        user_address = Address.objects.get(user_id=request.user.id)
        user_address.is_default = True
        messages.warning(request, '.داشتن حداقل یک آدرس برای حساب کاربری شما الزامی است', 'warning')
        return redirect(url)


class EditAddressView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = EditAddressForm
    template_name = 'account/edit_address.html'
    # success_url = reverse_lazy('account:available_addresses')

    def get_success_url(self):
        # return reverse_lazy('account:available_addresses', kwargs={'pk': self.request.user.pk})
        return reverse_lazy('account:available_addresses', args=(self.request.user.pk,))
        # return reverse('account:available_addresses', args=(self.request.user.pk,))

    def form_valid(self, form):
        """
        This function handles the default address of the user.
        Each user can have only and only one default address.
        """
        form = form.save()
        if form.is_default and Address.objects.filter(user=form.user).count() > 0:
            try:
                previous_default_address = Address.objects.exclude(id=form.id).get(user=form.user, is_default=True)
                previous_default_address.is_default = False
                previous_default_address.save()
            except:
                pass
        elif not form.is_default and Address.objects.filter(user=form.user, is_default=True) == 0:
            form.is_default = True
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context


def history_orders(request):
    orders = Order.objects.filter(user=request.user)
    parent_categories = Category.objects.filter(is_sub_category=False)
    return render(request, 'account/history.html', {'orders': orders, 'parent_categories': parent_categories})


class Report(SuperUserRequiredMixin, View):
    """
    Reporting class for admin.
    """
    def get(self, request, *args, **kwargs):
        income = 0
        orders = Order.objects.all()
        for order in orders:
            income += order.total_price
        now = jdatetime.datetime.today()
        context = {
            'number_of_customers':  Customer.objects.filter(is_staff=False).count(),
            'number_of_staffs': Customer.objects.filter(is_staff=True, is_superuser=False).count(),
            'number_of_admins': Customer.objects.filter(is_superuser=True).count(),
            'num_with_discount': Book.objects.filter(Q(percent_discount__isnull=False) |
                                                Q(cash_discount__isnull=False)).count(),
            'num_without_discount': Book.objects.filter(percent_discount__isnull=True,
                                                cash_discount__isnull=True).count(),
            'income': income,
            'number_of_orders': Order.objects.all().count(),
            'now': now,

        }
        return render(request, 'account/report.html', context)


def create_staff(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(password=data['password_2'], email=data['email'],
                                            phone_number=data['phone_number'], is_staff=True)
            user.save()
            messages.success(request, 'ایجاد کارمند با موفقیت انجام شد', 'success')
            return redirect('book:home')
    else:
        form = UserRegisterForm()
    parent_categories = Category.objects.filter(is_sub_category=False)
    context = {'form': form, 'parent_categories': parent_categories}
    return render(request, 'account/register.html', context)

