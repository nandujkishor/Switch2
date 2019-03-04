var SCOPE = 'email profile openid';
function handleClientLoad() {
  gapi.load('client:auth2', initClient);
}

function initClient() {
  gapi.client.init({
      'scope': SCOPE,
      'clientId': '727153101463-709hp9lcjelc2ps4evtb4ojutbq1sotl.apps.googleusercontent.com',
  }).then(function () {
    GoogleAuth = gapi.auth2.getAuthInstance();

    GoogleAuth.isSignedIn.listen(updateSigninStatus);

    var user = GoogleAuth.currentUser.get();
    setSigninStatus();

    $('.in-button').click(function() {
      handleAuthClick();
    });  
  });
}

function handleAuthClick() {
  // console.log(GoogleAuth.isSignedIn.get());
  if (!GoogleAuth.isSignedIn.get()) {
    GoogleAuth.signIn();
  }
  else
    console.log("Not authenticated")
}

function revokeAccess() {
  console.log("Disconnected from Google");
  GoogleAuth.disconnect();
  window.location.href="/farer/logout"
}

function setSigninStatus(isSignedIn) {
  var user = GoogleAuth.currentUser.get();
  $.ajax({
    type: "POST",
    url: "/farer/tokensignin/",
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    data: {idtoken: user.getAuthResponse().id_token},
    success: function(data){
      if(data != "Already authenticated")
        checkLogin();
    }
  });
}

function checkLogin(){

  $.getJSON("/farer/data/user/", function(data){

    console.log("Details completed? " + data['detailscomp']);
    console.log("Educational details completed? " + data['educomp']);

    $('.container').css('opacity','0');
    $('.loading').css('visibility', 'hidden');

    if(data['detailscomp'] == null){

      fName = data['fname'];
      lName = data['lname'];

      window.location.href="/farer/details/"

    }
    else if(data['educomp'] == null){

      console.log("Routing to education form");
      window.location.href="/farer/education/"

    }
    else{
      console.log(sessionStorage.getItem('origin'))
      origin = sessionStorage.getItem('origin');

      if(origin == null)
        window.location.href="/"
      else
        window.location.href=origin;

    }

  });

}

function updateSigninStatus(isSignedIn) {
  setSigninStatus();
}