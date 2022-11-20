#!/usr/bin/python3
# -*- coding: utf-8 -*

import pickle, os, sys, json, time, hashlib;
import compress_pickle as cpk
import pandas as pd

import plotly.express as px
from dash import Dash, dcc, html

from flask import Flask, session, request, redirect;
from datetime import datetime;

from PSQL_api.admin_queries import add_user, get_userinfo, block_user;
from PSQL_api.acc_queries import get_accounts, add_account, add_money, out_money, buy_curr;
from PSQL_api.get_currency import get_currency, get_curr_rates;

app=Flask(__name__, static_folder='static');
app.config.from_pyfile('config.py');

headerMenu = '<div class="toppanel">'+\
                '<table width="100%">'+\
                    '<tr>'+\
                        '<td width="10%"><a href="/" class="border-button">Главная</a></td>'+\
                        '<td width="10%"><a href="/profile" class="border-button">Профиль</button></a></td>'+\
                        '<td width="10%"><a href="/unlog" class="border-button">Выйти</a></td>'+\
                        '<td width="60%"></td>'+\
                        '<td><p class="LableTop">AtomBank<p></td>'+\
                    '</tr>'+\
                '</table>'+\
             '</div>'

styleHeader = '.toppanel{margin:auto; width:90%; height:70px; padding: 2px; border: 3px solid transparent; border-top:ridge blue; border-bottom:ridge blue}'+\
                '.border-button {text-decoration: none;display: inline-block;padding: 10px 20px;margin: 10px 20px;position: relative;color: white;border: 1px solid rgba(255, 255, 255, .4);background: none;font-weight: 300;font-family: "Montserrat", sans-serif;text-transform: uppercase;letter-spacing: 2px;}'+\
                '.border-button:before, .border-button:after {content: "";position: absolute;width: 0;height: 0;opacity: 0; box-sizing: border-box;}'+\
                '.border-button:before {bottom: 0;left: 0;border-left: 1px solid white;border-top: 1px solid white;transition: 0s ease opacity .8s, .2s ease width .4s, .2s ease height .6s}'+\
                '.border-button:after {top: 0;right: 0;border-right: 1px solid white;border-bottom: 1px solid white;transition: 0s ease opacity .4s, .2s ease width, .2s ease height .2s}'+\
                '.border-button:hover:before, '+\
                '.border-button:hover:after {height: 100%;width: 100%;opacity: 1;}'+\
                '.border-button:hover:before {transition: 0s ease opacity 0s, .2s ease height, .2s ease width .2s;}'+\
                '.border-button:hover:after {transition: 0s ease opacity .4s, .2s ease height .4s, .2s ease width .6s;}'+\
                '.border-button:hover {background: rgba(255, 255, 255, .2);}'+\
                '.body{background: linear-gradient(to top, #55EFCB 0%, #5BCAFF 100%); min-height: 100vh;}'+\
                '.LableTop{font-weight: 300;font-family: "Montserrat", sans-serif;text-transform: uppercase;letter-spacing: 2px;}'

#Сбор логов работы приложения
def logger(text: str):
    t = str(datetime.today())
    with open('AppLogs.txt','a') as g: g.write(t + ' ||| ' + text+'\n');

#Проверка авторизации пользователя
def chk_auth_user():
    if 'AuthSuc' in session: return True;
    else: return False;

#Проверка авторизации админа
def chk_auth_admin():
    if 'AuthSucAdmin' in session: return True;
    else: return False;

#Кодирование текста (пароля)
def prep_hash(txt: str):
    snd5 = hashlib.md5(txt.encode('utf-8')).hexdigest();
    return snd5;

#Поиск логина в хранилище
def find_login(l:str):
    with open(app.config['PATH_TO_LP']+'LPusers.txt','r') as g:
        for line in g:
            ls = line.split('*%*');
            if len(ls)>1:
                if l==ls[0]: return True;
    return False;

#Поиск пары логин\пароль пользователя в хранилище
def chk_PS_user(log: str, pas: str):
    hpas = prep_hash(pas);
    with open(app.config['PATH_TO_LP']+'LPusers.txt','r') as g:
        for line in g:
            ls = line.split('*%*');
            if len(ls)>1:
                if log==ls[0] and ls[1].strip('\n')==hpas:
                    logger('Пользователь '+log+' успешно зашел!');
                    session['id'] = get_userinfo(log)[0][0];
                    return True;
    logger('Неудачная попытка входа: ' + log + ' ' + pas);
    return False;

#Поиск пары логин\пароль администратора в хранилище
def chk_PS_admin(log: str, pas: str):
    hpas = prep_hash(pas);
    with open(app.config['PATH_TO_LP']+'LPadmins.txt','r') as g:
        for line in g:
            ls = line.split('*%*');
            if len(ls)==2:
                if log==ls[0] and ls[1].strip('\n')==hpas:
                    logger('Администратор '+log+' успешно зашел!');
                    return True;
    logger('Неудачная попытка входа администратора: ' + log + ' ' + pas);
    return False;


#Главная страница торговли
@app.route('/', methods=['POST','GET'])
def mainTraide():
    if not chk_auth_user(): return redirect('/login');
    style='<style>'+styleHeader+\
        '.mainDiv{overflow-x:auto; margin:auto; width:90%; padding: 2px; border: 3px solid transparent; border-top:ridge blue; border-bottom:ridge blue}'+\
        '.plotTab{width:100%; height:400px padding:10px; border: 4px double blue; border-top: 4px outset blue; border-bottom: 4px inset blue}'+\
        '.traideTab{width:100%; overflow-x: auto;  padding:10px; border: 4px double blue; border-top: 4px outset blue; border-bottom: 4px inset blue}'+\
        '.predTab{width:100%;  padding:10px}'+\
        '.tdPred{border: 2px solid;}'+\
        '.tdOnce{width: 100%}'+\
        '.tdOnce1{width: 100%; height:400px}'+\
        '.tdTraid{width: 50%; overflow-x: auto;}'+\
        '.pressed-button {text-decoration: none;display: inline-block;padding: 5px 40px;margin: 10px 20px;border-radius: 30px;background-image: linear-gradient(45deg, #6ab1d7 0%, #33d9de 50%, #002878 100%);background-position: 100% 0;background-size: 200% 200%;font-family: "Montserrat", sans-serif;font-size: 14px;font-weight: 100;color: white;box-shadow: 0 16px 32px 0 rgba(0, 40, 120, .35);transition: .5s;}'+\
        '.pressed-button:hover {box-shadow: 0 0 0 0 rgba(0, 40, 120, 0);background-position: 0 0;}'+\
        '</style>';

    tophead='<!DOCTYPE html><html><head>'+\
                '<title>Главная</title>'+\
            '<meta charset="utf-8">'+style+'</head>';

    body='<body class="body" onload="LoadWeb()">'+headerMenu+\
        '<p></p>'+\
        '<div class="mainDiv">'+\
            '<table class="plotTab">'+\
                '<tr>'+\
                    '<td class="tdOnce1"><div id="plotVal"></div></td>'+\
                '</tr>'+\
                '<tr>'+\
                    '<td class="tdOnce">'+\
                        '<select id="selval[]" size="2" multiple="multiple" class="pressed-button">'+\
                            '<option value="2">USD</option>'+\
                            '<option value="3">CNY</option>'+\
                            '<option value="4">EUR</option>'+\
                            '<option value="5">GBP</option>'+\
                            '<option value="6">JPY</option>'+\
                        '</select>'+\
                        '<button class="pressed-button" onclick="ref()">Показать</button>'+\
                    '</td>'+\
                '</tr>'+\
            '</table>'+\
            '<table class="traideTab">'+\
                '<tr>'+\
                    '<td class="tdTraid">'+\
                        '<form id="buyFormId" method="post" action="/buyTs">'+\
                            '<table class="traideTab"><tr>'+\
                            '<td width="10%"><input name="hm" type="number" value="0" step="0.01" class="pressed-button"></td>'+\
                            '<td width="10%"><select name="buyT" id="buyT" class="pressed-button">'+\
                            '</select></td>'+\
                            '<td width="10%"><input type="submit" value="Купить" class="pressed-button"></td>'+\
                            '<td></td>'+\
                            '</tr></table>'+\
                        '</form>'+\
                    '</td>'+\
                '<tr>'+\
                '</tr>'+\
                    '<td class="tdTraid">'+\
                        '<form id="sellFormId" method="post" action="/sellTs">'+\
                            '<table class="traideTab"><tr>'+\
                            '<td width="10%"><input name="hm" type="number" value="0" step="0.01" class="pressed-button"></td>'+\
                            '<td width="10%"><select name="sellT" id="sellT" class="pressed-button">'+\
                            '</select></td>'+\
                            '<td width="10%"><input type="submit" value="Продать" class="pressed-button"></td>'+\
                            '<td></td>'+\
                            '</tr></table>'+\
                        '</form>'+\
                    '</td>'+\
                '</tr>'+\
            '</table>'+\
            '<table class="plotTab">'+\
                '<tr>'+\
                    '<td class="tdOnce">График Предсказания</td>'+\
                '</tr>'+\
                '<tr>'+\
                    '<td class="tdOnce">График Предсказания управление</td>'+\
                '</tr>'+\
            '</table>'+\
        '</div>'

    script='<script type="text/javascript" src="static/js/main.js"></script>';

    return tophead+body+script+"</body></html>";

@app.route('/sellTs', methods=["POST"])
def sellTs():
    if request.method=="POST":
        tap = get_currency();
        rap = {'USD':'RUBUSD',
                'EUR':'RUBEUR',
                'GBP':'RUBGBP',
                'JPY':'RUBJPY',
                'CNY':'RUBCNY'}
        lval = request.form['sellT'].split('|')
        logger(str(lval));
        logger('')
        HM = float(request.form['hm']);
        qw = float(tap['quotes'][rap[lval[0]]])

        t = buy_curr(user_id=session['id'], accfr_id=lval[1], accto_id=lval[2], value_from=HM*qw, value_to=HM);
        if t: logger('Успешное продажа: ' + lval[0]+' '+str(HM));
        else: logger('Отказ в продаже: ' + str(session['id']) +' '+lval[1]+' '+ lval[2]);
        return redirect('/');

@app.route('/buyTs', methods=["POST"])
def buyTs():
    if request.method=="POST":
        tap = get_currency();
        rap = {'USD':'RUBUSD',
                'EUR':'RUBEUR',
                'GBP':'RUBGBP',
                'JPY':'RUBJPY',
                'CNY':'RUBCNY'}
        lval = request.form['buyT'].split('|')
        logger(str(lval));
        logger('')
        HM = float(request.form['hm']);
        qw = float(tap['quotes'][rap[lval[0]]])

        t = buy_curr(user_id=session['id'], accfr_id=lval[2], accto_id=lval[1], value_from=HM, value_to=HM*qw);
        if t: logger('Успешное покупка: ' + lval[0]+' '+str(HM));
        else: logger('Отказ в покупке: ' + str(session['id']) +' '+lval[2]+' '+ lval[1]);
        return redirect('/');

@app.route('/getplot', methods=["POST"])
def getplot():
    if request.method=="POST":
        content = request.json;
        logger(str(content.keys()))

        fig=get_curr_rates(curr=list(content.keys()))

        fig.write_html("static/fig.html")

        fut = {'plot':'true'}
        return json.dumps(fut);


#Страница авторизации пользователя
@app.route('/login', methods=['POST','GET'])
def login():
    mes='';
    if 'mes' in session:
        mes=session['mes'];
        del session['mes'];

    mes2='';
    if 'mes2' in session:
        mes2=session['mes2'];
        del session['mes2'];


    style='<style>'+styleHeader+\
    '.logmendiv{margin: 0 auto; margin-top: 10%;  width: 15%; text-align: center}'+\
    '.logintab{border: 2px solid #555555; padding: 4px 12px}'+\
    '.Newlogmendiv{margin: 0 auto; margin-top: 10%;  width: 15%; text-align: center}'+\
    '.Newlogintab{border: 2px solid #555555; padding: 4px 12px}'+\
    '.inputT{width:90%}'+\
    '.LableTop2{font-weight: 300;font-family: "Montserrat", sans-serif;text-transform: uppercase;letter-spacing: 2px; margin-left: 2%; margin-top: 2%}'+\
    '</style>'

    tophead='<!DOCTYPE html><html><head>'+\
                '<title>Авторизация</title>'+\
            '<meta charset="utf-8">'+style+'</head>'

    body='<body onload="onloadlog()" class="body">'+\
        '<div class="toppanel">'+\
            '<table width="100%">'+\
                '<tr>'+\
                    '<td width="90%"></td>'+\
                    '<td height="65"><p class="LableTop">AtomBank<p></td>'+\
                '</tr>'+\
            '</table>'+\
        '</div>'+\
        '<div class="logmendiv">'+\
            '<table class="logintab">'+\
                '<tr>'+\
                    '<td><p>Авторизация</p></td>'+\
                '</tr>'+\
                '<tr>'+\
                    '<td><form id="loginned" action="/loggd" method=post>'+\
                        '<input class="inputT" id="Logid" name="Log" oninput="chkval()" type="text" placeholder="Логин" style="width:100%">'+\
                        '<input id="Pasid" name="Pas" oninput="chkval()" type="password" placeholder="Пароль" style="width:100%">'+\
                        '<input type="submit" value="Вход" id="butlog">'+\
                    '</form></td>'+\
                '</tr>'+\
            '</table>'+mes+\
        '</div>'+\
        '<div class="Newlogmendiv">'+\
            '<table class="Newlogintab">'+\
                '<tr>'+\
                    '<td><p>Создайте профиль</p></td>'+\
                '</tr>'+\
                '<tr>'+\
                    '<td><form id="newAuthlog" action="/newAuth" method=post>'+\
                        '<input id="NewLogid" name="NewLog" oninput="chkNew()" type="text" placeholder="Установите Логин" style="width:100%">'+\
                        '<input id="NewPasid" name="NewPas" oninput="chkNew(); dublPas()" type="password" placeholder="Придумайте Пароль" style="width:100%">'+\
                        '<input id="NewPasid2" name="NewPas2" oninput="chkNew(); dublPas()" type="password" placeholder="Повторите Пароль" style="width:100%">'+\
                        '<input id="NewMailid" name="NewMail" oninput="chkNew()" type="email" placeholder="E-mail" style="width:100%">'+\
                        '<input id="NewFNameid" name="NewFName" oninput="chkNew()" type="text" placeholder="Имя" style="width:100%">'+\
                        '<input id="NewLNameid" name="NewLName" oninput="chkNew()" type="text" placeholder="Фамилия" style="width:100%">'+\
                        '<input id="NewTelid" name="NewTel" oninput="chkNew()" type="text" placeholder="Телефон" style="width:100%">'+\
                        '<input type="submit" value="Создать" id="Newbutlog">'+\
                    '</form></td>'+\
                '</tr>'+\
            '</table>'+mes2+\
        '</div>'

    script='<script type="text/javascript" src="static/js/logjs.js"></script>'

    return tophead+body+script+"</body></html>";

#Обработка формы авторизации пользователя
@app.route('/loggd', methods=['POST'])
def loggd():

    #Проверка на недопустимые символы для защиты от инсертов
    def chs(d):
        if len(d)==0: return True;
        for c in d:
            if c in '<>?/"}{][\|@#$%^&*()!.,': return True;
        return False;

    if request.method=='POST':
        lg = request.form['Log'];
        ps = request.form['Pas'];

        if chs(lg) or chs(ps):
            logger('Попытка ввести недопустимые символы');
            session['mes']='Использованы недопустимые символы!';
            return redirect('/login');
        
        if chk_PS_user(lg, ps):
            session['AuthSuc']=lg;
            return redirect('/');

        else:
            logger('Введены неверные логин или пароль');
            session['mes']='Неверная пара Логин/Пароль';
            return redirect('/login')

#Обработка формы создания пользователя
@app.route('/newAuth', methods=['POST'])
def newAuth():

    #Проверка на недопустимые символы для защиты от инсертов
    def chs(d):
        if len(d)==0: return True;
        for c in d:
            if c in '<>?/"}{][\|@#$%^&*()!.,': return True;
        return False;

    if request.method=='POST':
        L = request.form['NewLog'];
        P = request.form['NewPas'];
        M = request.form['NewMail'];
        T = request.form['NewTel'];
        FN = request.form['NewFName'];
        LN = request.form['NewLName'];

        PH = prep_hash(P);

        if find_login(L):
            session['mes2'] = 'Пользователь с таким имененм уже существует!'
            return redirect('/login')
        
        ts = 6000
        while ts>0:
            if os.path.exists('SYSTEMmark/STOPwr'): time.sleep(0.1); ts-=1;
            else:
                g=open('SYSTEMmark/STOPwr','w'); g.close();
                with open('MassData/newusers.txt', 'a') as g: g.write('&%&'.join([L,M,T,FN,LN,PH])+'\n');
                os.remove('SYSTEMmark/STOPwr');
                session['mes2']='Запрос на создание аккаунта успешно отправлен!';
                break;
        return redirect('/login')

#Страница профиля
@app.route('/profile', methods=['POST','GET'])
def profile():
    if not chk_auth_user(): return redirect('/login');
    logger('Пользователь '+session['AuthSuc']+' открыл страницу Профиля')

    style='<style>'+styleHeader+\
        '.pressed-button {text-decoration: none;display: inline-block;padding: 5px 40px;margin: 10px 20px;border-radius: 30px;background-image: linear-gradient(45deg, #6ab1d7 0%, #33d9de 50%, #002878 100%);background-position: 100% 0;background-size: 200% 200%;font-family: "Montserrat", sans-serif;font-size: 14px;font-weight: 100;color: white;box-shadow: 0 16px 32px 0 rgba(0, 40, 120, .35);transition: .5s;}'+\
        '.pressed-button:hover {box-shadow: 0 0 0 0 rgba(0, 40, 120, 0);background-position: 0 0;}'+\
        '.mainDiv{overflow-x:auto; margin:auto; width:90%; padding: 2px; border: 3px solid transparent; border-top:ridge blue; border-bottom:ridge blue}'+\
        '</style>'

    tophead='<!DOCTYPE html><html><head>'+\
                '<title>Профиль</title>'+\
            '<meta charset="utf-8">'+style+'</head>'

    body='<body class="body" onload="LoadWeb()">'+headerMenu+\
            '<p></p>'+\
            '<div class="mainDiv">'+\
                '<table width="100%">'+\
                    '<tr>'+\
                        '<td width="15%"><div id="userinfo"></div></td>'+\
                        '<td width="25%"><div id="acinfo"></div></td>'+\
                        '<td width="35%">'+\
                            '<form method="post" action="/createacc">'+\
                                '<table width="100%"><tr>'+\
                                    '<td width="10%"><select name="nradio" id="radioac" class="pressed-button">'+\
                                    '</select></td>'+\
                                    '<td width="10%"><input type="submit" value="Создать счет" class="pressed-button"></td>'+\
                                    '<td></td>'+\
                                '</tr></table>'+\
                            '</form>'+\
                        '</td>'+\
                        '<td>'+\
                            '<form method="post" action="/buydon"><input type="hidden" id="bhid" name="bhidn">'+\
                                '<table width="100%"><tr>'+\
                                    '<td width="10%"><input name="howmuch" type="number" value="0" step="0.01" class="pressed-button"></td>'+\
                                    '<td width="10%"><input type="submit" value="Внести средства" class="pressed-button"></td>'+\
                                    '<td></td>'+\
                                '</tr></table>'+\
                            '</form>'+\
                            '<form method="post" action="/selldon">'+\
                                '<table  width="100%"><tr>'+\
                                    '<td width="10%"><input name="howmuch" type="number" value="0" step="0.01" class="pressed-button"></td>'+\
                                    '<td width="10%"><input type="submit" value="Вывести средства" class="pressed-button"></td>'+\
                                    '<td></td>'+\
                                '</tr></table>'+\
                            '</form>'+\
                        '</td>'+\
                    '</tr>'+\
                '</table>'+\
            '</div>'

    script='<script type="text/javascript" src="static/js/profile.js"></script>'

    return tophead+body+script+"</body></html>";


@app.route('/selldon', methods=['POST'])
def selldon():
    if request.method=="POST":
    
        s = out_money(user_id=session['id'], value=int(request.form['howmuch']), accfr_id='1'); #, accfr_id=int(session['1'])
        if s: logger('Выведены средства '+request.form['howmuch'])
        else: logger('Ошибка выведения средств '+request.form['howmuch'])

        return redirect('/profile')

@app.route('/buydon', methods=['POST'])
def buydon():
    if request.method=="POST":
        s = add_money(user_id=session['id'], value=int(request.form['howmuch']))
        if s: logger('Внесены средства '+request.form['howmuch'])
        else: logger('Ошибка пополнения средства '+request.form['howmuch'])

        return redirect('/profile')


@app.route('/createacc', methods=['POST'])
def createacc():
    if request.method=="POST":
        acs={'USD':'2','CNY':'3','EUR':'4','GBP':'5','JPY':'6'}
        choseac = request.form['nradio']
        if choseac in acs:
            add_account(user_id=session['id'], curr_id=acs[choseac])

        return redirect('/profile')

def getacc():
    return get_accounts(session['id']);

def getinfo():
    return get_userinfo(session['AuthSuc']);

@app.route('/getload', methods=['POST'])
def getload():
    if request.method=="POST":
        info = getinfo();
        accounts = getacc();

        data = {};
        data['fn']=info[0][2]; data['ln']=info[0][4]; data['phone']=info[0][5]; data['e-mail']=info[0][6];
        data['acc']={}
        for x in (accounts):
            val = x[1]
            num = x[0]
            bal = x[3]
            #session[val]=num

            data['acc'][val] = {}
            data['acc'][val]['sum']=bal;
            data['acc'][val]['num']=num;
        
        return json.dumps(data);





#Выход пользователя
@app.route('/unlog', methods=['POST','GET'])
def unlog():
    if 'AuthSuc' in session: del session['AuthSuc'];
    return redirect('/login')


#Страница авторизации администрации
@app.route('/adminauth', methods=['POST','GET'])
def loginadmin():
    session['SameSite']='None';
    mes='';
    if 'mesa' in session:
        mes=session['mesa'];
        del session['mesa'];

    style='<style>'+\
    '.logmendiv{margin: 0 auto; margin-top: 10%;  width: 15%; text-align: center}'+\
    '.logintab{border: 2px solid #555555; padding: 4px 12px;}'+\
    '</style>'

    tophead='<!DOCTYPE html><html><head>'+\
                '<title>Авторизация Администратора</title>'+\
                '<meta charset="utf-8">'+style+'</head>'

    body='<body onload="onloadlog()">'+\
            '<div class="logmendiv">'+\
                '<table class="logintab">'+\
                    '<tr>'+\
                        '<td><p>Авторизация Администратора</p></td>'+\
                    '</tr>'+\
                    '<tr>'+\
                        '<td><form id="loginned" action="/authadm" method=post>'+\
                            '<input id="Logid" name="Log" oninput="chkval()" type="text" placeholder="Логин" style="width:100%">'+\
                            '<input id="Pasid" name="Pas" oninput="chkval()" type="password" placeholder="Пароль" style="width:100%">'+\
                            '<input type="submit" value="Вход" id="butlog">'+\
                        '</form></td>'+\
                    '</tr>'+\
                '</table>'+mes+\
            '</div>'

    script='<script type="text/javascript" src="static/js/logAjs.js"></script>'

    return tophead+body+script+"</body></html>";    

#Обработка формы авторизации администратора
@app.route('/authadm', methods=['POST'])
def authadm():
    
    #Проверка на недопустимые символы для защиты от инсертов
    def chs(d):
        if len(d)==0: return True;
        for c in d:
            if c in '<>?/"}{][\|@#$%^&*()!.,': return True;
        return False;

    if request.method=='POST':
        lg = request.form['Log'];
        ps = request.form['Pas'];

        if chs(lg) or chs(ps):
            logger('Попытка ввести недопустимые символы');
            session['mesa']='Использованы недопустимые символы!';
            return redirect('/adminauth');

        if chk_PS_admin(lg,ps):
            session['AuthSucAdmin']=lg;
            return redirect('/adminmenu');

        else:
            logger('Введены неверные логин или пароль');
            session['mesa']='Неверная пара Логин/Пароль';
            return redirect('/adminauth')

#Страница администратора
@app.route('/adminmenu', methods=['POST','GET'])
def adminmenu():
    session['SameSite']='None';
    if not chk_auth_admin(): return redirect('/adminauth');

    mesR = '';
    if 'mesR' in session:
        mesR = session['mesR'];
        del session['mesR'];

    style='<style>'+\
    '.mainDiv{margin:auto; border: 2px solid; width: 90%}'+\
    '.HeadNewUsers{width:100%}'+\
    '.headTd{text-align:center}'+\
    '.mainTable{width:100%}'+\
    '.NewUsersClass{width:100%; height: 500px; overflow-x: auto}'+\
    '.tdLogin{width:20%; border: 1px solid}'+\
    '.tdMail{width:30%; border: 1px solid}'+\
    '.tdPhone{width:10%; border: 1px solid}'+\
    '.tdFN{width:10%; border: 1px solid}'+\
    '.tdLN{width:10%; border: 1px solid}'+\
    '.tdblock{width:10%; border: 1px solid}'+\
    '.tdPlus{border: 1px solid}'+\
    '</style>'

    tophead='<!DOCTYPE html><html><head>'+\
                '<title>Страница администратора</title>'+\
            '<meta charset="utf-8">'+style+'</head>'

    body='<body onload="LoadWeb()">'+\
    '<div class="mainDiv">'+\
        '<table class="mainTable">'+\
            '<tr>'+\
                '<td class="headTd"><p>Панель Управления</p><p>'+mesR+'</p></td>'+\
            '</tr>'+\
            '<tr>'+\
                '<td>'+\
                    '<p>Подтверждение регистрации пользователей</p>'+\
                    '<table class="HeadNewUsers">'+\
                        '<tr>'+\
                            '<td class="tdLogin">Логин</td>'+\
                            '<td class="tdMail">E-mail</td>'+\
                            '<td class="tdPhone">Телефон</td>'+\
                            '<td class="tdFN">Имя</td>'+\
                            '<td class="tdLN">Фамилия</td>'+\
                            '<td class="tdPlus">Управление</td>'+\
                        '</tr>'+\
                    '</table>'+\
                '<div id="NewUsers" class="NewUsersClass"></div></td>'+\
            '<tr>'+\
            '</tr>'+\
                '<td><div border="2px solid">'+\
                    '<table>'+\
                        '<tr>'+\
                            '<td>'+\
                                '<div>'+\
                                    '<input type="text" id="findid" placeholder="Введите значение">'+\
                                    '<input type="submit" id="butfindid" value="Поиск" onclick="searchL()">'+\
                                '</div>'+\
                            '</td>'+\
                        '</tr>'+\
                    '</table>'+\
                    '<table class="HeadNewUsers">'+\
                        '<tr>'+\
                            '<td class="tdLogin">Логин</td>'+\
                            '<td class="tdMail">E-mail</td>'+\
                            '<td class="tdPhone">Телефон</td>'+\
                            '<td class="tdFN">Имя</td>'+\
                            '<td class="tdLN">Фамилия</td>'+\
                            '<td class="tdblock">Блок</td>'+\
                            '<td class="tdPlus">Управление</td>'+\
                        '</tr>'+\
                    '</table>'+\
                    '<div id="findLid"></div>'+\
                '</td>'+\
            '</tr>'+\
        '</table>'+\
    '</div>'

    script='<script type="text/javascript" src="static/js/admjs.js"></script>';

    return tophead+body+script+"</body></html>";

#Загрузка списка новых регистраций
@app.route('/UploadUsers', methods=['POST'])
def UploadUsers():
    if request.method=='POST':

        def find_bl_phone(phone: str):
            with open('MassData/blacklistPhone.txt','r') as g: file=g.read();
            if phone in file.split('\n'): return True;
            else: return False;


        tara = {'Error':'Error'}

        ts = 6000;
        while ts>0:
            if os.path.exists('SYSTEMmark/STOPwr'): time.sleep(0.1); ts-=1;
            else:
                g=open('SYSTEMmark/STOPwr','w'); g.close(); logger('Чтение на загрузку')
                with open('MassData/newusers.txt', 'r') as g:
                    sara=g.read();
                    tara={};
                    for line in sara.split('\n'):
                        if len(line)>2:
                            lines=line.split('&%&');
                            tara[lines[0]]={'login':lines[0],
                                            'e-mail':lines[1],
                                            'phone':lines[2],
                                            'fn':lines[3],
                                            'ln':lines[4],
                                            'p':lines[5]};

                            if find_bl_phone(tara[lines[0]]['phone']):
                                tara[lines[0]]['TBL']='Red';
                            else: tara[lines[0]]['TBL']='None';

                os.remove('SYSTEMmark/STOPwr');
                break;


        return json.dumps(tara);

@app.route('/updateNewUsers', methods=['POST'])
def updateNewUsers():
    if request.method=='POST':
        content = request.json;
        lineJson = '&%&'.join([content['login'], content['e-mail'], content['phone'], content['fn'], content['ln'], content['p']]);

        ts = 6000;
        while ts>0:
            if os.path.exists('SYSTEMmark/STOPwr'): time.sleep(0.1); ts-=1;
            else:
                g=open('SYSTEMmark/STOPwr','w'); g.close();
                with open('MassData/newusers.txt', 'r') as g: tap = g.read()
                taps = tap.split('\n');
                if lineJson in taps:
                    taps.remove(lineJson);
                    if content['how']=='del': logger('Удалена регистрация: '+lineJson);
                    if content['how']=='add': logger('Создан пользователь: '+lineJson);
                with open('MassData/newusers.txt', 'w') as g: g.write('\n'.join(taps));
                os.remove('SYSTEMmark/STOPwr');
                break;

        if content['how']=='add':
            if find_login(content['login']):
                session['mesR']='Пользователь с таким имененм уже существует! Отказано в создании';
                logger('Отказано в создании '+content['login']);
            else:
                if add_user(logname=content['login'], fname=content['fn'], lname=content['ln'], mname='', phone=content['phone'], adress=content['e-mail'], approved=True, blocked=False, description=''):
                    session['mesR']='Пользователь успешно добавлен!';
                    logger('Добавлен в базу пользователь: '+lineJson);
                    with open('LPdir/LPusers.txt','a') as g:
                        g.write('*%*'.join([content['login'], content['p'], '\n']))
                else:
                    session['mesR']='Произошла внутренняя ошибка!';
                    logger('Ошибка добавления в базу пользователя: '+lineJson);


        return redirect('/adminmenu');

@app.route('/searchLL', methods=['POST'])
def searchLL():
    if request.method=="POST":
        content = request.json
        data = get_userinfo(content['log']);
        newdata = {}
        if data:
            newdata['log']=data[0][1];
            newdata['fn']=data[0][2];
            newdata['ln']=data[0][4];
            newdata['phone']=data[0][5];
            newdata['e-mail']=data[0][6];
            newdata['block']=data[0][8];
        if not data:
            newdata['false']='false';

        logger('Отправка поиска пользователя: '+str(newdata))
        return json.dumps(newdata);

@app.route('/blocUnblockL', methods=['POST'])
def blocUnblockL():
    if request.method=="POST":
        content = request.json;
        if content['how'] == 'ban':
            bl=True;
        else:
            bl=False;
        logger('Пользователь: '+str(content))
        a = block_user(user_id=content['login'], blocked=bl)
        if a: logger('Пользователь: '+str(content['how']))
        else: logger('Пользователя не смогло: '+str(content['how']))
        return redirect('/adminmenu')



if __name__ == "__main__":
    logger('Запуск приложения');
    app.run(host=app.config['HOST'], port=app.config['PORT']);
 