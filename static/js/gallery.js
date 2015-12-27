
function clear_url(){
    var re = /(.*)\?/;
    var url = window.location.href.toString();
    var news = url.match(re)[1];
    // window.history.replaceState({}, document.title, news);
    return;
};

function del_loader(){
    var ldr = document.getElementById('loader');
    ldr.setAttribute('style', 'display:none;');
    var par = ldr.parentNode;
    var img = document.getElementById('tmp_image');
    img.removeAttribute('style');
    add_button(img);
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
    remove_button();
    var img = document.createElement('img');
    img.setAttribute('id', 'tmp_image');
    img.setAttribute('onload', 'javascript:del_loader();');
    img.setAttribute('src', '/static/' + images[pos]);
    img.setAttribute('alt', '/static/' + images[pos]);
    img.setAttribute('style', 'display:none;')
    current = '/static/' + images[pos];
    document.location = '?current='+images[pos];
    par.appendChild(img);
    insert_loader(img);
};

function set_cookie(){
    document.cookie = 'bgimage=' + current;
    set_main_image(current);
    return;
};

function unset_cookie(){
    document.cookie = 'bgimage=';
    remove_main_image();
    return;
};

function set_main_image(src){
    var maind = document.getElementById('main_image');
    var imgd = document.getElementById('main');
    var par = maind.parentNode;
    if (imgd){
        var par2 = imgd.parentNode;
        par2.removeChild(imgd);
    }
    par.removeAttribute('style');
    var img = document.createElement('img');
    img.setAttribute('src', src);
    img.setAttribute('id', 'main');
    img.setAttribute('alt', src);
    //img.setAttribute('style', 'width:auto; height:auto; max-width:200px;max-height:200px;margin:10px;');
    maind.appendChild(img);
    //document.body.setAttribute('style', 'background-image:url('+src+')!important;');
};

function remove_main_image(){
    var maind = document.getElementById('main_image');
    var imgd = document.getElementById('main');
    var par = maind.parentNode;
    par.setAttribute('style', 'display:none;');
    var par1 = imgd.parentNode;
    par1.removeChild(imgd);
}

function add_button(){
    var neigh = document.getElementById('navmenu');
    var li = document.createElement('li');
    var btn = document.createElement('a');
    btn.setAttribute('id', 'cook');
    btn.setAttribute('onclick', 'javascript:set_cookie();');
    btn.setAttribute('href', '#');
    btn.innerHTML = '<b>Make default</b>';
    li.appendChild(btn);
    neigh.appendChild(li);
};
/*
<a href="#" class="myButton">green</a>

*/
function remove_button(){
    var btn = document.getElementById('cook');
    if (btn){
        var par = btn.parentNode;
        par.removeChild(btn);
    };
    return;
};

function prevent_event(evt){
    if (evt.stopPropagation){
        evt.stopPropagation();
    }else{
        if (window.event.cancelBubble){
            window.event.cancelBubble = true;
        }
    }
    if (evt.preventDefault) {
        evt.preventDefault();
    } else {
        evt.returnValue = false;
    };
    return evt;
};

document.onkeyup = function(evt) {
    evt = evt || window.event;
    var code = evt.keyCode;
    if (evt.charCode && code == 0)
        code = evt.charCode;
    if (code == 27) {
        evt = prevent_event(evt);
        var el = document.getElementById('tmp_div');
        if (el){
            var par = el.parentNode;
            par.removeChild(el);
            current = '';
            clear_url();
            remove_button();
        }
        var el = document.getElementById('help');
        if (el) {
            var par = el.parentNode;
            par.removeChild(el);
        }
    }
    else if (code == 112) {
        evt = prevent_event(evt);
        help();
    }
    else if (code == 37){
        evt = prevent_event(evt);
        if (current != ''){
            change_image('left');
        }
    }
    else if (code == 39){
        evt = prevent_event(evt);
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
    remove_button();
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
    img.setAttribute('style', 'display:none;')
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
    /*if (el2 === null){
        var src = el.getAttribute('src');
        current = src;
        define_image(src);
    };*/
    if (el2 != null){
        var el2 = document.getElementById('tmp_div');
        var par = el2.parentNode;
        par.removeChild(el2);
        remove_button();
        current = '';
        };
};

function liked(img){
    like(img);
}

function like(){

}
