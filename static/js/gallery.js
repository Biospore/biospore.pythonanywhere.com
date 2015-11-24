
function clear_url(){
    var re = /(.*)\?/;
    var url = window.location.href.toString();
    var news = url.match(re)[1];
    window.history.replaceState({}, document.title, news);
    return;
};

function del_loader(){
    var ldr = document.getElementById('loader');
    ldr.setAttribute('style', 'display:none;');
    var par = ldr.parentNode;
    var img = document.getElementById('tmp_image');
    img.setAttribute('style', 'display:block;');
    return;
};

function change_image(direction){
    var len = images.length;
    var pos = search(current, images);
    if (direction == 'left'){
        if (pos == 0){
            pos = len - 1;
        }
        else {
            pos -= 1;
        }
    }
    else if (direction == 'right'){
        if (pos == len - 1){
            pos = 0;
        }
        else {
            pos += 1;
        }
    }
    else {
        return;
    }

    var img = document.getElementById('tmp_image');
    var par = img.parentNode;
    par.removeChild(img);
    var img = document.createElement('img');
    img.setAttribute('id', 'tmp_image');
    img.setAttribute('onload', 'javascript:del_loader();');
    img.setAttribute('src', '/static/' + images[pos]);
    img.setAttribute('alt', '/static/' + images[pos]);
    current = '/static/' + images[pos];
    document.location = '?current='+images[pos];
    par.appendChild(img);
    insert_loader(img);
};

function prevent_event(evt){
    if (evt.stopPropagation){
        evt.stopPropagation();
    }else{
        window.event.cancelBubble = true;
    }
    if (evt.preventDefault) {
        evt.preventDefault();
    } else {
        evt.returnValue = false;
    };
};

document.onkeypress = function(evt) {
    evt = evt || window.event;

    if (evt.keyCode == 27) {
        prevent_event(evt);
        var el = document.getElementById('tmp_div');
        if (el){
            var par = el.parentNode;
            par.removeChild(el);
            current = '';
            clear_url();
        }
        var el = document.getElementById('help');
        if (el) {
            var par = el.parentNode;
            par.removeChild(el);
        }
    }
    else if (evt.keyCode == 112) {
        prevent_event(evt);
        help();
    }
    else if (evt.keyCode == 37){
        prevent_event(evt);
        if (current != ''){
            change_image('left');
        }
    }
    else if (evt.keyCode == 39){
        prevent_event(evt);
        if (current != ''){
            change_image('right');
        }
    }
};

function search(element, array){
    var len = array.length;
    for (var i=0; i<len;i++){
        if ('/static/'+array[i] == element){
            return i;
        }
    }
}

function define_image(src){
    var img = document.createElement('img');
    img.setAttribute('src', src);
    img.setAttribute('alt', src);
    var par = document.body;
    var div = document.createElement('div');
    var div2 = document.createElement('div');
    var divr = document.createElement('div');
    var divc = document.createElement('div');
    img.setAttribute('id', 'tmp_image');
    img.setAttribute('onload', 'javascript:del_loader();');
    div.setAttribute('class', 'container');
    div.setAttribute('id', 'tmp_div');
    div2.setAttribute('id', 'blacken');
    divr.setAttribute('class', 'row');
    divc.setAttribute('class', 'col-md-12 col-xs-12 col-sm-12');
    divc.setAttribute('style', 'padding: 0!important;');
    divc.appendChild(img);
    insert_loader(img);
    divc.appendChild(div2);
    divr.appendChild(divc);
    div.appendChild(divr);
    div.setAttribute('onclick', 'clicked(this)');
    par.appendChild(div);
};

function help(){
    var el = document.getElementById('help');
    if (el){
        var par = el.parentNode;
        par.removeChild(el);
        return;
    }
    var txt = document.createElement('p');
    var title = document.createElement('h4');
    txt.innerHTML = 'ESC - return to gallery & exit help.<br/>';
    txt.innerHTML += 'F1 - open|close this dialog.<br/>';
    txt.innerHTML += 'Left arrow - previous image.<br/>';
    txt.innerHTML += 'Right arrow - next image.<br/>';
    title.innerHTML = 'Help';
    var div = document.createElement('div');
    div.setAttribute('class', 'well container');
    div.setAttribute('id', 'help');
    div.appendChild(title);
    div.appendChild(txt);
    document.body.appendChild(div);
};

function clicked(el){
    var el2 = document.getElementById('tmp_image');
    if (el2 === null){
        var src = el.getAttribute('src');
        current = src;
        define_image(src);
    };
    if (el2 != null){
        var el2 = document.getElementById('tmp_div');
        var par = el2.parentNode;
        par.removeChild(el2);
        current = '';
        clear_url();
        };
};
