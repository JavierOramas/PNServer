function FileExists(url){
    var xhr = new XMLHttpRequest();
    xhr.open('HEAD', url, false);
    xhr.send();

    if (xhr.status = '404'){
        return false;
    }
    return true;
}