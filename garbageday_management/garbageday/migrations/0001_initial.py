# Generated by Django 3.1.3 on 2021-04-29 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('line', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Garbageday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binary_lineid', models.BinaryField(verbose_name='バイナリ型LineID')),
                ('garbage_type', models.IntegerField(choices=[(0, '燃えるごみ'), (1, '燃えないごみ'), (2, 'カン・ビン'), (3, '粗大ごみ'), (4, '資源ごみ')], verbose_name='ごみの種類')),
                ('week1', models.IntegerField(choices=[(0, '毎週'), (1, '第１'), (2, '第２'), (3, '第３'), (4, '第４')], verbose_name='週1')),
                ('week2', models.IntegerField(blank=True, choices=[(0, '毎週'), (1, '第１'), (2, '第２'), (3, '第３'), (4, '第４')], null=True, verbose_name='週2')),
                ('day_of_week1', models.IntegerField(choices=[(0, '月曜日'), (1, '火曜日'), (2, '水曜日'), (3, '木曜日'), (4, '金曜日'), (5, '土曜日'), (6, '日曜日')], verbose_name='曜日1')),
                ('day_of_week2', models.IntegerField(blank=True, choices=[(0, '月曜日'), (1, '火曜日'), (2, '水曜日'), (3, '木曜日'), (4, '金曜日'), (5, '土曜日'), (6, '日曜日')], null=True, verbose_name='曜日2')),
                ('manage_alarm', models.BooleanField(verbose_name='アラーム ON/OFF')),
                ('alarm_day', models.IntegerField(blank=True, choices=[(0, '当日'), (1, '前日')], null=True, verbose_name='設定日')),
                ('alarm_time', models.IntegerField(blank=True, choices=[(0, '00:00'), (1, '00:30'), (2, '01:00'), (3, '01:30'), (4, '02:10'), (5, '02:30'), (6, '03:00'), (7, '03:30'), (8, '04:00'), (9, '04:30'), (10, '05:00'), (11, '05:30'), (12, '06:00'), (13, '06:30'), (14, '07:00'), (15, '07:30'), (16, '08:00'), (17, '08:30'), (18, '09:00'), (19, '09:30'), (20, '10:00'), (21, '10:57'), (22, '11:00'), (23, '11:30'), (24, '12:00'), (25, '12:15'), (26, '13:00'), (27, '13:30'), (28, '14:00'), (29, '14:30'), (30, '15:00'), (31, '15:30'), (32, '16:00'), (33, '16:30'), (34, '17:00'), (35, '17:30'), (36, '18:00'), (37, '18:30'), (38, '19:00'), (39, '19:30'), (40, '20:00'), (41, '20:30'), (42, '21:00'), (43, '21:30'), (44, '22:00'), (45, '22:30'), (46, '23:00'), (47, '23:30')], null=True, verbose_name='通知時間')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line.line')),
            ],
        ),
    ]
