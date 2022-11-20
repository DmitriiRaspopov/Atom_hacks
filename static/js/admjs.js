function searchL(){
    let logS = document.getElementById('findid');

    let data = {'log':logS.value};
    const result = JSON.stringify(data,null,4);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/searchLL');
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type','application/json')
    xhr.send(result);
    xhr.onload = function() {
        let rdata = xhr.response;

        let divAdm = document.getElementById('findLid');

        if (document.getElementById('tabUserFind')){document.getElementById('tabUserFind').remove()};
        if (document.getElementById('textI')){document.getElementById('textI').remove()};

        if ('false' in rdata){
            divAdm.innerHTML = '<p id="textI">Пользователь не найден!</p>';
        } else {
            let tab = document.createElement('table');
            tab.id = 'tabUserFind';
            tab.style.width = '100%';

            divAdm.appendChild(tab);

            create_tabsearch(rdata);
        }
    }
}

function blocUnblock(data){
    const result = JSON.stringify(data,null,4);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/blocUnblockL');
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type','application/json')
    xhr.send(result);
}

function create_tabsearch(line){
    let tabM = document.getElementById('tabUserFind');
    let trVar = document.createElement('tr');
    let tdVar1 = document.createElement('td');
    let tdVar2 = document.createElement('td');
    let tdVar3 = document.createElement('td');
    let tdVar5 = document.createElement('td');
    let tdVar6 = document.createElement('td');
    let tdVar7 = document.createElement('td');
    let tdVar4 = document.createElement('td');
    let ButBlock = document.createElement('button');
    let ButUnblock = document.createElement('button');

    tdVar4.appendChild(ButBlock);
    tdVar4.appendChild(ButUnblock);
    trVar.appendChild(tdVar1);
    trVar.appendChild(tdVar2);
    trVar.appendChild(tdVar3);
    trVar.appendChild(tdVar5);
    trVar.appendChild(tdVar6);
    trVar.appendChild(tdVar7);
    trVar.appendChild(tdVar4);

    tabM.appendChild(trVar);

    trVar.style.background = '#D3D3D3';

    tdVar1.style.border = '1px solid';
    tdVar2.style.border = '1px solid';
    tdVar3.style.border = '1px solid';
    tdVar4.style.border = '1px solid';
    tdVar5.style.border = '1px solid';
    tdVar6.style.border = '1px solid';
    tdVar7.style.border = '1px solid';

    tdVar1.style.width = '20%';
    tdVar2.style.width = '30%';
    tdVar3.style.width = '10%';
    tdVar5.style.width = '10%';
    tdVar6.style.width = '10%';
    tdVar7.style.width = '10%';

    tdVar1.style.overflowX = 'auto';
    tdVar2.style.overflowX = 'auto';
    tdVar3.style.overflowX = 'auto';

    tdVar1.innerHTML = line['log'];
    tdVar2.innerHTML = line['e-mail'];
    tdVar3.innerHTML = line['phone'];
    tdVar5.innerHTML = line['fn'];
    tdVar6.innerHTML = line['ln'];
    tdVar7.innerHTML = line['block'];

    ButBlock.innerHTML = 'Бан';
    ButUnblock.innerHTML = 'Разбан';

    ButBlock.onclick = function(){
        data={};
        data['how'] = 'ban';
        data['login'] = line['log'];
        blocUnblock(data);
    }

    ButUnblock.onclick = function(){
        data={};
        data['how'] = 'noban';
        data['login'] = line['log'];
        blocUnblock(data);
    }
}



function addNewUsers(data){
    let divAdm = document.getElementById('NewUsers');
    let tabAdm = document.createElement('table');

    divAdm.appendChild(tabAdm);

    tabAdm.style.width = '100%';
    tabAdm.id = 'tabUsersId';
    
    for (x in data){
        create_td(data[x]);
    }
}

function create_td(line){
    let tabM = document.getElementById('tabUsersId');
    let trVar = document.createElement('tr');
    let tdVar1 = document.createElement('td');
    let tdVar2 = document.createElement('td');
    let tdVar3 = document.createElement('td');
    let tdVar5 = document.createElement('td');
    let tdVar6 = document.createElement('td');
    let tdVar4 = document.createElement('td');
    let ButYes = document.createElement('button');
    let ButNo = document.createElement('button');

    tdVar4.appendChild(ButYes);
    tdVar4.appendChild(ButNo);
    trVar.appendChild(tdVar1);
    trVar.appendChild(tdVar2);
    trVar.appendChild(tdVar3);
    trVar.appendChild(tdVar5);
    trVar.appendChild(tdVar6);
    trVar.appendChild(tdVar4);

    tabM.appendChild(trVar);

    trVar.style.background = '#D3D3D3';

    tdVar1.style.border = '1px solid';
    tdVar2.style.border = '1px solid';
    tdVar3.style.border = '1px solid';
    tdVar4.style.border = '1px solid';
    tdVar5.style.border = '1px solid';
    tdVar6.style.border = '1px solid';

    tdVar1.style.width = '20%';
    tdVar2.style.width = '30%';
    tdVar3.style.width = '10%';
    tdVar5.style.width = '10%';
    tdVar6.style.width = '10%';

    tdVar1.style.overflowX = 'auto';
    tdVar2.style.overflowX = 'auto';
    tdVar3.style.overflowX = 'auto';

    tdVar1.innerHTML = line['login'];
    tdVar2.innerHTML = line['e-mail'];
    tdVar3.innerHTML = line['phone'];
    tdVar5.innerHTML = line['fn'];
    tdVar6.innerHTML = line['ln'];

    if (line['TBL']=='Red'){
        tdVar3.style.background = "#CD5C5C";
    }

    ButYes.innerHTML = 'Добавить';
    ButNo.innerHTML = 'Удалить';


    let data = {'login':line['login'],
                'e-mail':line['e-mail'],
                'phone':line['phone'],
                'fn':line['fn'],
                'ln':line['ln'],
                'p':line['p'],
                'how':''}

    ButNo.onclick = function(){
        data['how'] = 'del';
        updateNewUsers(data);
        tabM.remove();
        LoadNewUsers();
    }

    ButYes.onclick = function(){
        data['how'] = 'add';
        updateNewUsers(data);
        tabM.remove();
        LoadNewUsers();
    }
}

function updateNewUsers(data){
    const result = JSON.stringify(data,null,4);
    let xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.open('POST', '/updateNewUsers');
    xhr.setRequestHeader('Content-Type','application/json')
    xhr.send(result);
}

function LoadNewUsers(){
    let request = new XMLHttpRequest();
    request.open('POST', '/UploadUsers');
    request.responseType = 'json';
    request.send();
    request.onload = function() {
        let data = request.response;
        if ('Error' in data){
            let sadas = false;
        } else {
            addNewUsers(request.response);
        }
    }
}

function LoadWeb() {
    LoadNewUsers();
}