from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from home.models import MyUser, Database, Conversation, Message


def index(request):
    if request.user.is_authenticated:
        database = Database(request.user.id)
        context = {
            'profile': database.lay_thong_tin_all_user(),
            'da_tung_chat': database.da_tung_chat(),
        }
        return render(request, 'home/base.html', context)
    else:
        return render(request, 'home/login.html')


class Login_user(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return render(request, 'home/login.html')

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home:login')
                else:
                    return render(request, 'home/login.html', {'message': 'Tài khoản đã bị vô hiệu hóa'})
            else:
                return render(request, 'home/login.html', {'message': 'Sai  tài khoản hoặc mật khẩu'})


def logout_user(request):
    try:
        logout(request)
    except:
        pass
    return redirect('home:login')


class Register_user(View):
    def get(self, request):
        return render(request, 'home/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        if password != password1:
            return render(request, 'home/register.html', {'message': 'Mật khẩu không trùng nhau'})
        else:
            new_user = MyUser()
            new_user.username = username
            new_user.email = email
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.set_password(password)
            new_user.namSinh = birthday
            new_user.gioiTinh = gender
            new_user.diaChi = address
            new_user.save()
            newuser = MyUser.objects.filter(username=username)
            if newuser:
                return redirect('home:login')
            else:
                return render(request, 'home/register.html', {'message': 'Mật khẩu cần có cả chữ và sô'})


class Profile(View):
    def get(self, request, username):
        database = Database(request.user.id)
        context = {
            'profile': database.lay_thong_tin_voi_username(username),
            'da_tung_chat': database.da_tung_chat(),
        }
        return render(request, 'home/profile.html', context)

    def post(self, request):
        return redirect('home:login')


class Timkiem(View):
    def post(self, request):
        gender = request.POST.get('gender')
        tuoi_tu = request.POST.get('tuoi_tu')
        tuoi_den = request.POST.get('tuoi_den')
        diachi = request.POST.get('diachi')
        # sothich = request.POST.get('sothich')
        if tuoi_tu != '':
            today = date.today()
            x = today.year - int(tuoi_tu)
            y = today.year - int(tuoi_den)
            if x < y:
                sql_year = "AND DATE(namSinh) BETWEEN '" + str(x) + "' AND '" + str(y) + "'"
            else:
                sql_year = "AND DATE(namSinh) BETWEEN '" + str(y) + "' AND '" + str(x) + "'"
        else:
            sql_year = ""

        if diachi != '':
            sqldc = "AND diaChi like  '%" + str(diachi) + "%' "
        else:
            sqldc = ''

        sql = "SELECT * FROM home_myuser WHERE gioiTinh like '%" + str(gender) + "%'" + sql_year + sqldc
        results = MyUser.objects.raw(sql)
        database = Database(request.user.id)
        context = {
            'profile': results,
            'da_tung_chat': database.da_tung_chat(),
        }
        return render(request, 'home/return_user.html', context)


# class box_chat(View):
#     def get(self, request, user_2_id):
#         if request.user.is_authenticated:
#             database = Database(request.user.id)
#             id_room = database.id_room(request.user.id, user_2_id)
#             if not id_room:
#                 try:
#                     Conv = Conversation()
#                     Conv.user_1 = MyUser.objects.get(id=request.user.id)
#                     Conv.user_2 = MyUser.objects.get(id=user_2_id)
#                     Conv.save()
#                 except:
#                     return redirect('home:login')
#             context = {
#                 'profile': database.lay_thong_tin_voi_username(user_2_id),
#                 'da_tung_chat': database.da_tung_chat(),
#             }
#             return render(request, 'home/chat.html', context)
#         else:
#             return redirect('home:login')

class api_ajax(View):
    def get(self, request, user_2_id):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            id_room = database.id_room(request.user.id, user_2_id)
            if not id_room:
                try:
                    Conv = Conversation()
                    Conv.user_1 = MyUser.objects.get(id=request.user.id)
                    Conv.user_2 = MyUser.objects.get(id=user_2_id)
                    Conv.save()
                except:
                    return redirect('home:login')
            ketqua = database.context_room_chat(id_room)
            profile = database.lay_thong_tin_voi_username(user_2_id)
            context = {
                'ketqua': ketqua,
                'profile': profile,
            }
            return render(request, 'home/return_chat.html', context)

        else:
            return redirect('home:login')

    def post(self, request, user_2_id):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            id_room = database.id_room(request.user.id, user_2_id)
            # lưu tin nhắn
            if request.POST.get('content') != '':
                Mess = Message()
                Mess.from_user = MyUser.objects.get(id=request.user.id)
                Mess.conversation = Conversation.objects.get(c_id=id_room)
                Mess.content = request.POST.get('content')
                Mess.save()
            # in ra kết quả
            ketqua = database.context_room_chat(id_room)
            profile = database.lay_thong_tin_voi_username(user_2_id)
            context = {
                'ketqua': ketqua,
                'profile': profile
            }
            return render(request, 'home/return_chat.html', context)

        else:
            return redirect('home:login')


class Update(View):
    def post(self, request):
        if request.user.is_authenticated:
            get_user = MyUser.objects.get(id=request.user.id)
            a = request.POST.get('intro')
            avatar = request.FILES['avatar']
            print(a)
            get_user.intro = a
            get_user.avatar = avatar
            get_user.save()

            return redirect('home:home')
        else:
            return redirect('home:login')
