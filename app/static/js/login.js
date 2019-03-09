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

function get_data(){
  
}

function data_complete(){

  console.log("Inside data complete");
  var flag = $.Deferred();

  $.getJSON("/farer/data/user/", function(data){

    // console.log("Checking for data");
    // console.log("More details? " + data['detailscomp']);
    // console.log("Education details? " + data['educomp']);

    if(data['detailscomp'] == null){
      console.log("DETAILS COMP");
      flag.reject();
      window.location.href="/farer/details/"
    }
    else if(data['educomp'] == null){
      flag.reject();
      window.location.href="/farer/education/"
    }
    
    flag.resolve();
  
  });

  return flag.promise();
}

function checkLogin(){

  // console.log("Inside check login");

  $.when(data_complete()).done(function(){
    
    console.log("Origin = " + sessionStorage.getItem('origin'))
    origin = sessionStorage.getItem('origin');

    if(origin == null)
      window.location.href="/"
    else
      window.location.href=origin;
  });

}

function updateSigninStatus(isSignedIn) {
  setSigninStatus();
}