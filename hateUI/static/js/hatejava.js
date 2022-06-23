const api_url = 'http://localhost:8080'

function api_request(event, _form) {

    let url = _form.querySelector(`input[name=${'url'}]`);
    let video_srcs = _form.querySelectorAll(`input[name=${'video_src'}]`);

    url = url.value;

    let video_src;

    for (vs of video_srcs) {
        if(vs.checked)
        video_src = vs.value;
    }

    console.log(url)
    console.log(video_src)

    var params = new FormData ();
    params.append ("link", url)
    params.append ('videoSource', video_src)
    
    function success() {

        console.log(this.responseText)
        sessionStorage.setItem("myData", this.responseText);
        window.location.assign('main.html');
    }

    // function to handle error
    function error(err) {
        console.log('Request Failed', err); //error details will be in the "err" object
        sessionStorage.setItem("requesterror", err)
        window.location.assign('404.html');
    }
    
    var xhr = new XMLHttpRequest(); 
    xhr.onload = success; 
    xhr.onerror = error;  
    xhr.open('POST', api_url+'/detect'); 
    xhr.send(params); 
      
    event.preventDefault();

}

window.onload = function () {

    const myForm = document.querySelector("#myForm");
    const loaderdiv = document.querySelector("#loader")
    const searchdiv = document.querySelector("#searchdiv")

    myForm.addEventListener('submit', function (event) {
        console.log("Hello")
        searchdiv.style.display = "none";
        loaderdiv.style.display = "initial";
        api_request(event, myForm)
        event.preventDefault()
     });


};
