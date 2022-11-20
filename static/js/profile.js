function LoadWeb(){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/getload');
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type','application/json')
    xhr.send();
    xhr.onload = function(){
        data = xhr.response;
        fillinfo(data);
        fillac(data);
        fillradio(data);
    }
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
        let opt = document.createElement('option');
        let spt= document.createElement('option');

        opt.value= spt.value =rad[x];
        opt.innerHTML= spt.innerHTML= rad[x];

        buyT.appendChild(opt);
        sellT.appendChild(spt);
    }
}

function fillinfo(data){
    let divuser = document.getElementById('userinfo');
    let fn = document.createElement('p');
    let ln = document.createElement('p');
    let phone = document.createElement('p');
    let mail = document.createElement('p');

    divuser.appendChild(fn);
    divuser.appendChild(ln);
    divuser.appendChild(phone);
    divuser.appendChild(mail);

    fn.innerHTML = 'Имя '+data['fn'];
    ln.innerHTML = 'Фамилия '+data['ln'];
    phone.innerHTML = 'Телефон '+data['phone'];
    mail.innerHTML = 'E-mail '+data['e-mail'];

}

function fillac(data){
    let divuser = document.getElementById('acinfo');

    for (x in data['acc']){
        let ar = document.createElement('p');
        divuser.appendChild(ar);
        let sss = ''
        if(x=='1'){sss = 'RUB'};
        if(x=='2'){sss = 'USD'};
        if(x=='3'){sss = 'CNY'};
        if(x=='4'){sss = 'EUR'};
        if(x=='5'){sss = 'GBP'};
        if(x=='6'){sss = 'JPY'};

        ar.innerHTML = 'Cчет '+ data['acc'][x]['num'] + ': '+ data['acc'][x]['sum']+' '+sss;
        
    }
}

function fillradio(data){
    let divsel = document.getElementById('radioac');
        let rad = {'2':'USD',
                    '3':'CNY',
                    '4':'EUR',
                    '5':'GBP',
                    '6':'JPY'}
        for (x in data['acc']){
            if (x in rad){delete rad[x]};
        }

        for (x in rad){
            let s = document.createElement('option');
            divsel.appendChild(s);

            s.value=rad[x];
            s.innerHTML=rad[x];
        }
}