function loadComment(url){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
            var txt = xhttp.responseText;
            if (window.DOMParser)
            {
                var parser = new DOMParser();
                var xmlDoc = parser.parseFromString(txt,"text/xml");
            }
            else // Internet Explorer
            {
                var xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
                xmlDoc.async = false;
                xmlDoc.loadXML(txt);
            }
            var comms = document.getElementById('comms');
            if (comms){

            var rcomms = comms.parentNode;
            rcomms.removeChild(comms);
            comms = document.createElement('ul');
            comms.setAttribute('id', 'comms');
            comms.setAttribute('class', 'list-group');

            var nodes = xmlDoc.getElementsByTagName('node');
            for (var i = 0; i<nodes.length; i++){
                node = nodes[i];
                var name = node.getElementsByTagName('name')[0].childNodes[0].nodeValue;
                var email = node.getElementsByTagName('email')[0].childNodes[0].nodeValue;
                var text = node.getElementsByTagName('text')[0].childNodes[0].nodeValue;
                var a = document.createElement('a');
                a.setAttribute('class', 'list-group-item container');
                a.setAttribute('href', '#');
                a.setAttribute('style', 'overflow:hidden;');
                var p1 = document.createElement('p');
                var p2 = document.createElement('p');
                p1.setAttribute('class', 'list-group-item-heading');
                p1.setAttribute('style', 'text-align:left; max-height:150px;overflow:hidden;');
                p2.setAttribute('style', 'max-height:400px;overflow:hidden;');
                p1.innerHTML = name + ' (' + email + ')';
                p2.setAttribute('class', 'list-group-item-text textmess');
                p2.innerHTML = text;
                a.appendChild(p1);
                a.appendChild(p2);
                comms.appendChild(a);
            }
            rcomms.appendChild(comms);
            }

        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
    setTimeout("loadComment('comments.xml')", 5000);
}

function loadLikes(url){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var txt = xhttp.responseText;
            if (window.DOMParser)
            {
                var parser = new DOMParser();
                var xmlDoc = parser.parseFromString(txt,"text/xml");
            }
            else // Internet Explorer
            {
                var xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
                xmlDoc.async = false;
                xmlDoc.loadXML(txt);
            }
            var nodes = xmlDoc.getElementsByTagName('image');
            for (var i = 0; i<nodes.length; i++){
                node = nodes[i];
                src = node.getAttribute('path');
                likes_count = node.getAttribute('likes');
                elem = document.getElementById(src);
                elem.innerHTML = parseInt(likes_count);
            }
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
    setTimeout("loadLikes('images.xml')", 100);
}
