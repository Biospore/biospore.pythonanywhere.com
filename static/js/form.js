function formclicked(){
    var form = document.getElementById('form');
    form.removeAttribute('style');
}

function submit(){
    var form = document.getElementById('form');
    form.setAttribute('style', 'display:none;');
}
