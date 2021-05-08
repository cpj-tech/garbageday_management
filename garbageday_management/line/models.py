from django.db import models

class Line(models.Model):
    #Lineでのプッシュ先を表す
    #LINEのid情報取得
    id = models.CharField('ユーザーID', max_length=150, unique=True,primary_key=True)
    def __str__(self):
        return self.id
class LineUserName(models.Model):
    #LINEのユーザー情報取得
    line = models.ForeignKey(Line,on_delete=models.CASCADE)
    display_name = models.CharField('表示名', max_length=255)
    def __str__(self):
        return self.display_name
    
