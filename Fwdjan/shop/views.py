from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from shop.forms import Shop_form
from .models import Shop_goods, kategory_name

goods_query_gl = None
last_page = None

# shop_start_new- основна функція проекту, забезпечує вивід даних по категоріях, пошук та сортування даних,
# їх вивід у різних представленнях, пагінацію сторінок


def shop_start_new (request, kat_id):
    global goods_query_gl
    step_page = ""
    query = request.GET.get('q_1')
    query_1 = request.GET.get('q_5')
    query_2 = request.GET.get('q_6')
    match query_1:
        case '0':
            sort_id = 'good_name'
        case '1':
            sort_id = 'good_price'
        case '2':
            sort_id = '-good_price'
        case '3':
            sort_id = '-date_update'
        case _:
            sort_id = 'good_name'

    if query and 'search_type' in request.GET:
        opys_kat = 'За результататами пошуку'
        goods_query = Shop_goods.objects.all().order_by(sort_id)
        if request.GET.get('q_4') == 'on':
            goods_query = goods_query.filter(good_kat=kat_id).order_by(sort_id)

        if request.GET.get('q_3'):
            if request.GET.get('q_3') == 'visible':
                goods_query = goods_query.filter(Q(good_name__icontains=request.GET.get('q_1'))).order_by(sort_id)
            else:
                goods_query = goods_query.filter(good_price__gte=float(request.GET.get('q_1')),
                                                 good_price__lte=float(request.GET.get('q_2'))).order_by(sort_id)
    else:
        if query_1:
            goods_query = goods_query_gl.order_by(sort_id)
            opys_kat = 'За результататами сортування'
        else:
            goods_query = Shop_goods.objects.filter(good_kat=kat_id).order_by(sort_id)
            opys_kat = dict(kategory_name())[kat_id]

    for i in range(1, 7):
        k = 'q_' + str(i)
        step_page = step_page + (k + '=' + (request.GET.get(k) + '&') if request.GET.get(k) else "")

    templ_name = 'shop/shop_tbl.html' if (query_2 == '6') else 'shop/shop_plt.html'
    paginator = Paginator(goods_query, 8)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    numerator = (page_obj.number - 1) * paginator.per_page
    context = {'nam_kat': kategory_name(), 'title': (kat_id, opys_kat), 'templ_name': templ_name,
               'goods': page_obj, 'numerator': numerator, 'step_pag': step_page}

    goods_query_gl = goods_query
    return render(request, 'shop/shop_new.html', context)

#show_detail -забезпечує деталізований вивід інформації про товар
def show_detail(request, good_id):
    last_page = request.META['HTTP_REFERER']
    good = get_object_or_404(Shop_goods, id=good_id)
    context = {'title': 'Деталізація товару', 'item': good, 'last_page': last_page}
    return render(request, 'shop/index_detail.html', context)

#shop_create -забезпечує внесення інформації про новий товар
def shop_create(request):
    global last_page
    last_page = request.META['HTTP_REFERER'] if (not last_page) else last_page
    lefty = sign_in(request, 'user_1', 1)
    if lefty[0]:
        # last_page = ''
        form = Shop_form(request.POST or None, request.FILES or None)
        instance = form.save(commit=False)
        if form.is_valid():
            instance.save()
            messages.success(request, lefty[1])
            k = last_page
            last_page = None
            return redirect(k)
            # return HttpResponseRedirect(instance.get_absolute_url(1))
        else:
            context = {'title': 'Shop create', 'form': form, 'last_page': last_page,
                       'head': 'Внесення даних нового товару'}
            return render(request, 'shop/index_create.html', context)

#shop_update -забезпечує редагування раніше внесеної інформації про товар
def shop_update(request, good_id=None):
    global last_page
    last_page = request.META['HTTP_REFERER'] if (not last_page) else last_page
    lefty = sign_in(request, 'user_2', 2)
    if lefty[0]:
        page = 'shop/index_create.html'
        instance = get_object_or_404(Shop_goods, id=good_id)
        form = Shop_form(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, lefty[1])
            # return HttpResponseRedirect(instance.get_absolute_url(last_page))
            k = last_page
            last_page = None
            return redirect(k)
        else:
            context = {'form': form, 'last_page': last_page, 'head': 'Редагування даних'}
            return render(request, page, context)
    # else:
    #    return redirect(last_page)

#shop_delete -забезпечує вилучення інформації про товар
def shop_delete(request, good_id):
    last_page = request.META['HTTP_REFERER']
    lefty = sign_in(request, 'user_3', 3)
    if lefty[0]:
        good = get_object_or_404(Shop_goods, id=good_id)
        good.delete()
        messages.success(request, lefty[1])
    return redirect(last_page)

#sign_in - універсальна функція, яка забезпечує вивід інформаційних повідомлень
#про виконання певних операції та перевірку прав користувача в системі
def sign_in(request, usser, tp):
    match tp:
        case 1:
            mess = 'Дані успішно збережено !'
        case 2:
            mess = 'Дані успішно оновлено !'
        case 3:
            mess = 'Дані успішно видалено !'

    if request.user.is_superuser or (request.user.is_staff and (request.user.username == usser)):
        rez = True
    else:
        k = request.user.get_full_name() if request.user.get_full_name() else request.user.username
        messages.error(request, 'Користувач ' + k + ' не має прав на здійснення цієї операції !')
        rez = False
    return rez, mess

#usr_login -забезпечує авторизацію користувача в системі
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

#usr_login -забезпечує вихід користувача з системи
def usr_logout(request):
    global last_page
    last_page = request.META['HTTP_REFERER']
    logout(request)
    return redirect(last_page)

#home_page -забезпечує переадресацію на головну сторінку
def home_page(request):
    return render(request, 'index.html')
