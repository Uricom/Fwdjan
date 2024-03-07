from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from shop.forms import Shop_form
from .models import Shop_goods, kategory_name

global last_page
goods_query_gl = None


def shop_start(request):
    context = {'nam_kat': kategory_name()}
    return render(request, 'shop/index_shop.html', context)


def shop_start_new(request, kat_id):
    if 'q_5' in request.GET:
        print('працює кнопка !')
    else:
        print('працює ршввут !')
    # Обробка для другої кнопки

    global goods_query_gl
    step_page = ""
    query = request.GET.get('q_1')
    query_1 = request.GET.get('q_5')
    print('Вибір:', query_1)

    match query_1:
        case '- за назвою товару':
            sort_id = 'good_name'
        case '- за цiною зростання':
            sort_id = 'good_price'
        case '- за цiною спадання':
            sort_id = '-good_price'
        case '- за датою оновлення':
            sort_id = 'good_price'
        case _:
            sort_id = 'good_name'

    if query and 'search_type' in request.GET:
        opys_kat = 'За результататами пошуку'
        goods_query = Shop_goods.objects.all().order_by('good_name')
        if request.GET.get('q_4') == 'on':
            goods_query = goods_query.filter(good_kat=kat_id)

        if request.GET.get('q_3'):
            if request.GET.get('q_3') == 'visible':
                goods_query = goods_query.filter(Q(good_name__icontains=request.GET.get('q_1')))
            else:
                goods_query = goods_query.filter(good_price__gte=float(request.GET.get('q_1')),
                                                 good_price__lte=float(request.GET.get('q_2')))
    else:
        if query_1:
            goods_query = goods_query_gl.order_by(sort_id)
            opys_kat = 'За результататами сортування'
        else:
            goods_query = Shop_goods.objects.filter(good_kat=kat_id).order_by('good_name')
            opys_kat = dict(kategory_name())[str(kat_id)]

    for i in range(1, 6):
        k = 'q_' + str(i)
        step_page = step_page + (k + '=' + (request.GET.get(k) + '&') if request.GET.get(k) else "")

    print('Step:', step_page)
    paginator = Paginator(goods_query, 7)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    numerator = (page_obj.number - 1) * paginator.per_page
    context = {'nam_kat': kategory_name(), 'title': (str(kat_id), opys_kat),
               'goods': page_obj, 'numerator': numerator, 'step_pag': step_page}
    goods_query_gl = goods_query
    return render(request, 'shop/shop_new.html', context)


def show_detail(request, good_id):
    last_page = request.META['HTTP_REFERER']
    good = get_object_or_404(Shop_goods, id=good_id)
    nam_kat = dict(kategory_name())[good.good_kat]
    # last_page = '/shop/kat/' + good.good_kat + '/'
    context = {'title': 'Деталізація товару', 'nam_kat': nam_kat, 'item': good, 'last_page': last_page}
    return render(request, 'shop/index_detail.html', context)


def shop_k1(request, kat_id):
    last_page = '/shop'
    goods = Shop_goods.objects.filter(good_kat=kat_id)
    paginator = Paginator(goods, 7)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    numerator = (page_obj.number - 1) * paginator.per_page
    context = {'title': dict(kategory_name())[str(kat_id)], 'goods': page_obj, 'numerator': numerator,
               'last_page': last_page}
    return render(request, 'shop/index_k1.html', context)


def shop_create(request):
    last_page = request.META['HTTP_REFERER']
    lefty = sign_in(request, 'user_1', 1)
    if lefty[0]:
        # last_page = ''
        form = Shop_form(request.POST or None, request.FILES or None)
        instance = form.save(commit=False)
        if form.is_valid():
            instance.save()
            messages.success(request, lefty[1])
            return HttpResponseRedirect(instance.get_absolute_url(1))
        # last_page = '/shop/kat/' + instance.good_kat + '/'
        context = {'title': 'Shop create', 'form': form, 'last_page': last_page,
                   'head': 'Редагування даних нового товару'}
        return render(request, 'shop/index_create.html', context)
    else:
        return redirect(last_page)


def shop_update(request, good_id=None):
    last_page = request.META['HTTP_REFERER']
    lefty = sign_in(request, 'user_2', 2)
    if lefty[0]:
        page = 'shop/index_create.html' if ('new' in request.META['HTTP_REFERER']) else 'shop/index_update.html'
        # last_page = ''
        instance = get_object_or_404(Shop_goods, id=good_id)
        form = Shop_form(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, lefty[1])
            return HttpResponseRedirect(instance.get_absolute_url(1))
        # last_page = '/shop/kat/' + instance.good_kat + '/'
        context = {'title': 'Shop update', 'form': form, 'last_page': last_page, 'head': 'Редагування даних'}
        return render(request, page, context)
    else:
        return redirect(last_page)


def shop_delete(request, good_id):
    last_page = request.META['HTTP_REFERER']
    lefty = sign_in(request, 'user_3', 3)
    if lefty[0]:
        good = get_object_or_404(Shop_goods, id=good_id)
        good.delete()
        messages.success(request, lefty[1])
    return redirect(last_page)


def sign_in(request, usser, tp):
    match tp:
        case 1:
            mess = 'Дані успішно збережено !'
        case 2:
            mess = 'Дані успішно оновлено !'
        case 3:
            mess = 'Дані успішно знищено !'

    if request.user.is_superuser or (request.user.is_staff and (request.user.username == usser)):
        rez = True
    else:
        k = request.user.get_full_name() if request.user.get_full_name() else request.user.username
        messages.error(request, 'Користувач ' + k + ' не має прав на здійснення цієї операції !')
        rez = False
    return rez, mess


def usr_login(request):
    global last_page
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Авторизація користувача успішна !')
            return redirect(last_page)
        else:
            messages.error(request, 'Помилка авторизації користувача !')
    else:
        last_page = request.META['HTTP_REFERER']
        form = AuthenticationForm()
    return render(request, 'shop/usr_login.html', {"form": form})


def usr_logout(request):
    global last_page
    last_page = request.META['HTTP_REFERER']
    logout(request)
    return redirect(last_page)


def home_page(request):
    return render(request, 'index.html')
