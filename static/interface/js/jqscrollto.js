        jQuery(function($)
        {
            //zresetuj scrolla
            $.scrollTo(0);
            
            $('#link0').click(function() { $.scrollTo($('#about').offset().top, 700); });
            $('#link1').click(function() { $.scrollTo($('#about').offset().top); });
            $('#link2').click(function() { $.scrollTo($('#howto').offset().top); });
            $('#link3').click(function() { $.scrollTo($('#upload').offset().top); });
            $('#link4').click(function() { $.scrollTo($('#analysis').offset().top); });
            $('#link5').click(function() { $.scrollTo($('#authors').offset().top); });
            $('#link6').click(function() { $.scrollTo($('#main').offset().top + 100000); });

            $('.scrollup').click(function() { $.scrollTo($('body'), 1000); });
        }
        );
        
        //pokaż podczas przewijania
        
        $(window).scroll(function()
        {
            var content = $(".content-div")
            
            if($(this).scrollTop()>300) $('.scrollup').fadeIn();
            else $('.scrollup').fadeOut();
        

            if($(this).scrollTop()>=window.innerHeight - 1){
                $(".nav-main").addClass("nav-fixed")
                content.css("position", "relative")

            }
            else{
                $(".nav-main").removeClass("nav-fixed")
                content.css("position", "unset")
            }

        }
        );
