from django.contrib.auth.models import AbstractUser
from django.db import models


#
#
# # Create your models here.


class MyUser(AbstractUser):
    avatar = models.FileField(blank=True, null=True)
    diaChi = models.CharField(max_length=1000, blank=True, null=True)
    namSinh = models.DateField(blank=True, null=True)
    gioiTinh = models.CharField(max_length=100, blank=True, null=True)
    intro = models.TextField(blank=True, null=True)


class SoThich(models.Model):
    sothichId = models.AutoField(primary_key=True)
    ten = models.CharField(max_length=100, blank=True, null=True)


class SoThich_User(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=False)
    SoThich = models.ForeignKey(SoThich, on_delete=models.CASCADE, blank=True, null=False)


class Conversation(models.Model):
    c_id = models.AutoField(primary_key=True)
    user_1 = models.ForeignKey(MyUser, related_name='user_1', on_delete=models.CASCADE, null=False)
    user_2 = models.ForeignKey(MyUser, related_name='user_2', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    m_id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Database:
    def __init__(self, user_id):
        self.userid = str(user_id)

    def lay_thong_tin_voi_username(self, username):
        sql = "SELECT * FROM home_myuser WHERE username = '" + str(username) + "'OR id = '" + str(username) + "'"
        results = MyUser.objects.raw(sql)
        return results

    def lay_thong_tin_all_user(self):
        sql = "SELECT * FROM home_myuser"
        results = MyUser.objects.raw(sql)
        return results

    def id_room(self, user_1, user_2):
        sql = "SELECT c_id FROM home_conversation WHERE user_1_id = '" + str(user_1) + "' AND user_2_id = '" + str(
            user_2) + "' OR user_2_id =  '" + str(user_1) + "' AND user_1_id = '" + str(user_2) + "'"
        kt = Conversation.objects.raw(sql)[:1]
        if kt:
            a = kt[0].c_id
            return a
        else:
            return False

    def context_room_chat(self, id_room):
        sql = "SELECT * FROM home_message WHERE conversation_id = " + str(id_room)
        ketqua = Conversation.objects.raw(sql)
        return ketqua

    def da_tung_chat(self):
        sql = "SELECT * FROM home_myuser WHERE EXISTS (SELECT * FROM home_conversation WHERE user_1_id = " + self.userid + " OR user_2_id  =" + self.userid + ") AND id != " + self.userid
        ketqua = Conversation.objects.raw(sql)
        return ketqua
