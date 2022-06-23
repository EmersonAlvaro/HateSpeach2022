
myData = sessionStorage.getItem("myData");
myData = JSON.parse(myData);


function addToTable(tag, el) {

    let description_text = document.createTextNode(`${myData[`${tag}`]}`);
    el.appendChild(description_text);
   
}

window.onload = function () {

    const prediction = document.querySelector("#prediction");
    const source = document.querySelector("#source");
    const Link = document.querySelector("#Link");
    const videoID =document.querySelector("#videoID");
    const video_transcript =document.querySelector("#video_transcript");

    addToTable('transcript_Video', video_transcript);
    addToTable('videoID', videoID);
    addToTable('video_Source', source);
    addToTable('link', Link);
    addToTable('prediction', prediction);


};