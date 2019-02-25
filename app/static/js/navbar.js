var MenuOpen = false;
var normal_scroll = true;
var header_color;

function isMobile(){
    if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
        || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) { 
        return true;
    }
    return false;
}

function openNav() {
    header_color = $('.header').css('background-color');
    $('.header').css('background-color','transparent');
    $('.login').toggleClass('loginDisable');
    $('.sideNav').width("100%");
    $(".nav, .social").css("animation-name", "fadeIn");
    window.setTimeout(function(){
      $('body').addClass('noscroll');
      $('.sideNavContents').css('pointer-events','auto');
    },500);
}

function closeNav() {
    $('.login').toggleClass('loginDisable');
    $('.sideNavContents').css('pointer-events','none');
    $(".nav, .social").css("animation-name", "fadeOut");
    window.setTimeout(function(){
      $('.sideNav').width(0);
    },200);
    window.setTimeout(function(){
        $('body').removeClass('noscroll');
        $('.header').css('background-color', header_color);
    }, 700);
}

function openLoad(){
    $('.load-d').css('width', '100vw');
    window.setTimeout(function(){
        $('.load').css('width', '100vw');
    }, 400);
}

function closeLoad(){
    window.setTimeout(function(){
        $('.load').css('width', '0');
        setTimeout(function(){
            // console.log('Testing');
            $('.load-d').css('width', '0');
        }, 400);
    }, 1000);
}
function hover(){
    if(isMobile() == false){
        var active = false, timer, that = null;
        $("li").hover(function(){
            
            var cls = $(this).attr('id');

            function doHover(){

                $("." + cls + "BG").css('display','block');
                $('.nav a, .social a').css('color','#6c6c6c');
                window.setTimeout(function(){
                    $("." + cls).css('color','#000');
                    $("." + cls + "BG").css('margin-left','40%');
                    active = true;
                },100);

                that = cls;
            }

            timer = setTimeout(doHover,500);
        
        }, function(){
            if(that != null){
                $('.nav a, .social a').css('color','#000');
                $("." + that + "BG").css('margin-left','100%');
                window.setTimeout(function(){
                    $("." + that + "BG").css('display','none');
                    active = false;
                },400);
            }
            clearTimeout(timer);

        });

    }
}

function preload(arrayOfImages) {
    $(arrayOfImages).each(function(){
        $('<img/>')[0].src = this;
    });
}

preload([
    '/static/images/menu/talks.jpg',
    '/static/images/menu/concerts.jpg',
    '/static/images/menu/masterclass.jpg',
    '/static/images/menu/workshops.jpg',
    '/static/images/menu/contests.jpg',
    '/static/images/menu/sponsors.jpg',
]);

function scroll(){
    
    var didScroll;
    var lastScrollTop = 0;
    var delta = 5;
    var navbarHeight = $('.header').outerHeight();

    $(window).scroll(function(event){
        didScroll = true;
    });

    setInterval(function() {
        if (didScroll) {
            hasScrolled();
            didScroll = false;
        }
    }, 250);

    function hasScrolled() {
        var st = $(this).scrollTop();
        
        if(Math.abs(lastScrollTop - st) <= delta)
            return;
        
        if(st > lastScrollTop && st > navbarHeight){
            $('.header').addClass('header-up');
        }else{
            if(st + $(window).height() < $(document).height()) {
                console.log("SCROLLED UP");
                $('.header').removeClass('header-up');
            }
        }
        
        lastScrollTop = st;
    }
}

$(document).ready(function(){

    $.getScript("https://apis.google.com/js/client:platform.js", function () {
        init();
        $('.in-button').click(function(){
          console.log("Login clicked");
          login();
        });
    });

    $('.dashboard-button').click(function(){
        window.location.href="/dash/"
    });

    scroll();

    if(isMobile() == false){
        $('.nav').toggleClass("no-touch");
    }

    $('.menuVidyut').click(function(){
        window.location.href="/";
    });

    /* Menu-Button */
    $('.menu-button').click(function(){

        if(normal_scroll){
            $('.menu-button').toggleClass("change");
            $('.menuVidyut').toggleClass("color-change");
        }

        if(MenuOpen){
            closeNav();
            MenuOpen = false;
        } 
        else{
            openNav();
            MenuOpen = true;
        }
    });

    hover();

    $(document).on('keyup',function(evt) {
        if (evt.keyCode == 27) {
           if(MenuOpen){
                if(normal_scroll){
                    $('.menu-button').toggleClass("change");
                    $('.menuVidyut').toggleClass("color-change");
                }
                closeNav();
                MenuOpen = false;
            } 
        }
    });

    //Redirecting
    // $('#workshops').click(function(){
    //     console.log("TESTING");
    //     $('.content-wrapper').load('workshops.html');
    //     url = $(this).attr('id');
    //     console.log(url);
    //     window.history.pushState(url,null,url);
    // });

});