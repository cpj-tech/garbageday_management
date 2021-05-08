# SS 接続　（EC2インスタンスに入る）

$ ssh -i <任意のディレクトリ>/garbageday-project-ssh-key.pem ec2-user@<インスタンスのIP>　


# cpj_garbageday_management 使い方

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
# ローカル上でcodeを修正し、その動作を確認したい場合

1.一度docker-composeをstopする
~~~
docker-compose stop
~~~
2.再度docker-compose upする
~~~
docker-compose up
~~~
# DB初期化

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

# DB内に値が登録されているか確認したい場合

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

#logの見方

1.docker execコマンドでwebサーバー内に入る

~~~
docker exec -it garbageday_management bash 
~~~

2.以下のディレクトリに移動
~~~
cd /var/log
~~~

3.ディレクトリ内にlogファイルがあるため見たいファイルをcatコマンドで参照