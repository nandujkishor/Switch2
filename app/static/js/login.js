function init(){
    // console.log("loading gapi");
    gapi.load('auth2', function () {
      // console.log("gapi loaded");
      auth2 = gapi.auth2.init({
          client_id: '727153101463-709hp9lcjelc2ps4evtb4ojutbq1sotl.apps.googleusercontent.com'
      });
    });
  }

  function changeheader(color){
    $('.menuVidyut').toggleClass('color-change');
    $('.menu-button').toggleClass('change');
    $('.login').toggleClass('color-change');
    $('.login').toggleClass('border-change');
    if(color == "b")
      $('.header').css('background-color', '#000');
    else
      $('.header').css('background-color', '#fff');
  }

  function userChanged(user){
    console.log("USER CHANGED");
    $.ajax({
      type: "POST",
      url: "/farer/tokensignin/",
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      data: {idtoken: user.getAuthResponse().id_token},
      success: function(data){
        checkLogin();
      }
    });
  }

  function login() {
    console.log("onLogin");
    $.getJSON("/data/farer/user/", function(data){
      console.log(data);
      // auth2.currentUser.listen(userChanged);
      // auth2.signIn();
    }
  }

  function checkLogin(){

    var fName, lName;
    
    $.getJSON("/data/farer/user/", function(data){

      console.log("Details completed? " + data['detailscomp']);
      console.log("Educational details completed? " + data['educomp']);

      id = data['id'];

      if(data['detailscomp'] == null){

        $('.header').css('display', 'none');

        fName = data['fname'];
        lName = data['lname'];
        email = data['email'];

        $('.container').css('opacity','0');
        $('.loading').css('visibility', 'hidden');

        $('.container').load('/forms/details/', function(){

          $('#fname').val(fName);
          $('#lname').val(lName);

          window.history.pushState('/farer/details',null, '/farer/details');

          window.setTimeout(function(){
            $('.container').css('opacity', '1');
          },500)

        });

      }
      else if(data['educomp'] == null){

        $('.header').css('display', 'none');

        $('.container').css('opacity','0');
        $('.loading').css('visibility', 'hidden');
        
        // $('.container').load('/forms/education/', function(){

        //   window.history.pushState('/farer/education',null, '/farer/education');

        //   window.setTimeout(function(){
        //     $('.container').css('opacity', '1');
        //   },500)

        // });

      }
      else{

        console.log(origin);

        if(origin == null){

          $('.header').css('display', 'block');
          
          $('.login').html("Logout");
          $('.login').addClass('out-button').removeClass('in-button');
          console.log($('.in-button'));
        }
        else{
            window.setTimeout(function(){

            window.history.pushState(origin,null,origin);

            $('.container').load(origin, function(){
                window.setTimeout(function(){
                $('.container').css('opacity', '1');
                },600)
            });

            },500)
        }

      }

    });

  }