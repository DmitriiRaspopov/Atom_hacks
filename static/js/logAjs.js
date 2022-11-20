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

function onloadlog(){chkval()}