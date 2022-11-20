function chkval(){
    let l = document.getElementById('Logid');
    let p = document.getElementById('Pasid');
    let z = document.getElementById('butlog');
    function apr(l1, p1){
        if (l1.value == ''){return true}
        if (p1.value == ''){return true}
    }
    if (apr(l,p)){z.disabled = true} else {z.disabled = false}
}


function chkNew(){
    let l = document.getElementById('NewLogid');
    let p1 = document.getElementById('NewPasid');
    let p2 = document.getElementById('NewPasid2');
    let m = document.getElementById('NewMailid');
    let t = document.getElementById('NewTelid');
    let fn = document.getElementById('NewFNameid');
    let ln = document.getElementById('NewLNameid');
    let z = document.getElementById('Newbutlog');
    function apr(Nl, Np1, Np2, Nm, Nt, Nfn, Nln){
        if (Nl.value == ''){return true}
        if (Np1.value == ''){return true}
        if (Np2.value == ''){return true}
        if (Nm.value == ''){return true}
        if (Nt.value == ''){return true}
        if (Nfn.value == ''){return true}
        if (Nln.value == ''){return true}
    }
    if (apr(l,p1,p2,m,t,fn,ln)){z.disabled = true} else {z.disabled = false}
}

function onloadlog(){
    chkval();
    chkNew();
}

function dublPas(){
    let p1 = document.getElementById('NewPasid');
    let p2 = document.getElementById('NewPasid2');
    if (p2.value != p1.value){
        p1.style.border = 'solid red';
        p2.style.border = 'solid red';
        document.getElementById('Newbutlog').disabled = true;
    } else {
        p1.style.border = '';
        p2.style.border = '';
    }
}