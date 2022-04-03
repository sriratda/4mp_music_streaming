// alert('start')
// Modal form
document.getElementById('create-playlist').addEventListener("click", function() {
	document.querySelector('.bg-modal').style.display = "flex";
});
document.querySelector('.close').addEventListener("click", function() {
	document.querySelector('.bg-modal').style.display = "none";
});


// Cookie
function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }
  
  function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

// Play music
function audioPlayer(){
    var currentSong = 0;
    var currentSong_url = getCookie("currentSong");
    var tillPlayed = getCookie('timePlayed');
    var status = getCookie('statusSong')
    $("#audioPlayer")[0].src = currentSong_url;
    $("#audioPlayer")[0].currentTime = tillPlayed;
    // alert(status)
    if(status == 'true'){
      $("#audioPlayer")[0].play();
    }
    else{
      $("#audioPlayer")[0].pause();
    }
    // alert(currentSong_url)
    let id = "#playlist td #music-play"
    $(id).click(function(e){
       e.preventDefault(); 
       setCookie("currentSong",this)
       $(id).removeClass("current-song");
       currentSong = $(this).parent().index();
      //  alert(currentSong)
       $(this).addClass("current-song");
       $("#audioPlayer")[0].src = this;
       $("#audioPlayer")[0].play();
       
    });

    $("#audioPlayer")[0].addEventListener("ended", function(){
       currentSong++;
        if(currentSong == $(id).length)
            currentSong = 0;
        $(id).removeClass("current-song");
        $("#playlist td:eq("+currentSong+")").addClass("current-song");
        $("#audioPlayer")[0].src = $(id)[currentSong].href;
        $("#audioPlayer")[0].play();
    });
}

function addItem() {
    var a = document.getElementById("list");
    var candidate = document.getElementById("candidate");
    var li = document.createElement("li");
    li.setAttribute('id', candidate.value);
    li.appendChild(document.createTextNode(candidate.value));
    a.appendChild(li);
}

// Creating a function to remove item from list
function removeItem() {
    
    // Declaring a variable to get select element
    var a = document.getElementById("list");
    var candidate = document.getElementById("candidate");
    var item = document.getElementById(candidate.value);
    a.removeChild(item);
}
