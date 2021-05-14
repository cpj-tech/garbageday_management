# ごみ捨て管理くん

LINEアカウントと連携し、ごみの予定を通知してくれるwebアプリケーション。LINEアカウントと連携することで、LINEログイン、
LINE Messaging APIでのメッセージ送信を実現しています。

# デモ
~~~
https://docs.google.com/spreadsheets/d/1EtkNoh_beJV_XTyqguOChw8IxfY0O3MBdfDjI4CJbB4/edit?usp=sharing
~~~
# 特徴

　LINE画面から遷移し、カレンダーを開くことで、ごみの日の予定を登録でき、登録時刻なると、LINEからの通知を受け取れます。
「1週間」「1ヶ月」ボタンを押下することで、ごみの日の予定を確認できます。

# 動作手順

## ローカルで動作させたい場合

LINEアプリ上で動作するwebアプリケーションなので、基本的にはローカルで動作はしない。ただ「ngrok」というローカル上で稼働しているネットワークを外部公開できるサービスを用いたら簡単にローカル上で確認ができます。
<br>
<br>
<br>
1.ngrokの使用

ngrokをインストール、アカウント作成し、port 8000でポートフォワーディングできるようにします。（以下パス参照）
~~~
https://qiita.com/mininobu/items/b45dbc70faedf30f484e
~~~

2.postgresqlのインストール

DBをインストールし、gabageday_management/settings.pyのデータベース情報を更新する。
<br>
<br>
3.LINE Developersアカウントの使用

LINE Messaging APIとLINE　Login機能を使用するため、「LINE Developers」でアカウントを作成、「LINE Messaging API」「LINE Login」の二種類のチャンネルを作成、以下の設定をします。

・Messagging　APIのチャンネルのWebhook URLの設定

~~~
ngrokのhttps ipアドレス/line/callback
~~~

リッチメニューのURLを設定

~~~
ngrokのhttps ipアドレス/line/linelogin/
~~~

4.requirements.txtを事前にインストール

~~~
pip install -r requirements.txt
~~~

5.ソースコードの修正

gabageday_management/settings.pyの以下のDOMAINをngrokのhttpsアドレスに変更

~~~
ALLOWED_HOSTS = ['<DOMAIN>','<PUBLIC IP>']
~~~

gabageday_management/settings/info_settings.jsonのLINE設定とDOMAINを変更

6.アプリケーション実行

manage.pyの格納されているディレクトリまで遷移、以下のコマンドを実行
~~~
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
~~~

<br>
<br>

## AWSのEC2インスタンスで動作させたい場合


###  SSH接続　（EC2インスタンスに入る）

$ ssh -i <任意のディレクトリ>/garbageday-project-ssh-key.pem ec2-user@<インスタンスのIP>　


### cpj_garbageday_management 使い方

１、gitからpull
~~~
$ git pull
~~~
２、docker/docker-compose.yamlのvolume先を変更(自分の環境に合わせること)

３、dockerディレクトリ内で docker-compose up
~~~
$ docker-compose up
~~~
４、Djangoのコンテナ内に入る
~~~
$ docker exec -it garbageday_management bash
~~~
５、/code配下で以下のコマンドを行う。
~~~
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py collectstatic
~~~
### SSH上でcodeを修正し、その動作を確認したい場合

1.一度docker-composeをstopする
~~~
docker-compose stop
~~~
2.再度docker-compose upする
~~~
docker-compose up
~~~
### DB初期化

１、dbのコンテナ内に入る
~~~
$ docker exec -it db bash
~~~
２、docker-compose.yml に記載したvolume先のファイルを削除
~~~
$ rm -rf <データベース格納ディレクトリ>/*
~~~
１、Djangoのコンテナ内に入る
~~~
$ docker exec -it garbageday_management bash 
~~~
４、migration関連ファイル削除
~~~
$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
$ find . -path "*/migrations/*.pyc"  -delete
~~~
５、migrateを行う
~~~
$ python manage.py makemigrations
$ python manage.py migrate
~~~

### DB内に値が登録されているか確認したい場合

1.docker execコマンドでdbサーバーへ入る

~~~
docker exec -it db bash
~~~

2.psqlコマンドでgarbageday_dbへ接続する
~~~
psql garbageday_db -U ユーザー名
~~~
3.DB接続後、テーブル一覧を表示

~~~
\z
~~~
4.SQLコマンドでデータを表示

~~~
select * from テーブル名;
~~~

5.切断は「exit」コマンドで抜ける

#### logの見方

1.docker execコマンドでwebサーバー内に入る

~~~
docker exec -it garbageday_management bash 
~~~

2.以下のディレクトリに移動
~~~
cd /var/log
~~~

3.ディレクトリ内にlogファイルがあるため見たいファイルをcatコマンドで参照