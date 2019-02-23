function init(){
    // console.log("loading gapi");
    gapi.load('auth2', function () {
      // console.log("gapi loaded");
      auth2 = gapi.auth2.init({
          client_id: '727153101463-709hp9lcjelc2ps4evtb4ojutbq1sotl.apps.googleusercontent.com'
      });
    });
  }

  function userChanged(user){
    console.log("User changed");
    $.ajax({
      type: "POST",
      url: "/farer/tokensignin/",
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      data: {idtoken: user.getAuthResponse().id_token},
      success: function(data){
        console.log(data);
        checkLogin();
      }
    });
  }

  function login() {
    console.log("onLogin");
    $('.loading-login').css('display', 'inline');
    $.getJSON("/farer/data/user/", function(data){
      console.log(data);
      if(data == false){
        console.log("Passing to Google login");
        auth2.currentUser.listen(userChanged);
        auth2.signIn();
      }
      else
        checkLogin();
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
        origin = sessionStorage.getItem('origin');

        if(origin == null)
          window.location.href="/"
        else
          window.location.href=origin;

      }

    });

  }