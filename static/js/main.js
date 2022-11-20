function LoadWeb(){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/getload');
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type','application/json')
    xhr.send();
    xhr.onload = function(){
        data = xhr.response;
        filltraideradio(data)
    }
    let rad = {'2':'USD',
               '3':'CNY',
                '4':'EUR',
                '5':'GBP',
                '6':'JPY'}
    loadplot(rad);
}

function filltraideradio(data){
    let buyT = document.getElementById('buyT');
    let sellT = document.getElementById('sellT');

    let rad = {'1':'RUB',
                '2':'USD',
               '3':'CNY',
                '4':'EUR',
                '5':'GBP',
                '6':'JPY'}

    for (x in data['acc']){
        if (x!='1'){
            let opt = document.createElement('option');
            let spt= document.createElement('option');

            opt.value= spt.value =rad[x]+'|'+data['acc'][x]['num']+'|'+data['acc']['1']['num']
            opt.innerHTML= spt.innerHTML= rad[x];

            buyT.appendChild(opt);
            sellT.appendChild(spt);
        }
    }
}

function loadplot(curr){
    const result = JSON.stringify(curr,null,4);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/getplot');
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type','application/json')
    xhr.send(result);
    xhr.onload = function(){
        data = xhr.response;
        if (data['plot']=='true'){
            if (document.getElementById('nop')){document.getElementById('nop').remove()};
            let dvp = document.getElementById('plotVal');
            let ifr = document.createElement('iframe');
            dvp.appendChild(ifr);
            ifr.src = "static/fig.html";
            ifr.id = 'nop'
            ifr.style.width="100%";
            ifr.style.height="400px";
            dvp.style.height=400;
        }
    }
}

function ref(){
    let elm = document.getElementById('selval[]');
    //в этот массив будем отбирать выбранные значения
    values =[elm.value];

    //случай мульти-режима
    if (elm.multiple) {
    //перебираем массив опций
    for (var i = 0; i < elm.options.length; i ++) {
    //если опция выбрана - добавим её в массив
        if (elm.options[i].selected) 
        values.push(elm.options[i].value);
    }
    //случай одиночного выбора в select
    } else {
        values =[elm.value];
    }
     var jval = {}
     for (x in values){
        jval[x]=x;
     }
    if (jval!={}){
        loadplot(jval);
    }
}
