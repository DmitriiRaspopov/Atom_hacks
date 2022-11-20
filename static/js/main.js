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

        let dvp = document.getElementById('plotVal');
        dvp.innerHTML = data['plot'];
    }
}
