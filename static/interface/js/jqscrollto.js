        jQuery(function($)
        {
            //zresetuj scrolla
            $.scrollTo(0);
            
            $('#link1').click(function() { $.scrollTo($('#instruction').offset().top - 100, 500); });
            $('#link2').click(function() { $.scrollTo($('#upload').offset().top - 170, 500); });
            $('#link3').click(function() { $.scrollTo($('#authors'), 500); });
            
            $('.scrollup').click(function() { $.scrollTo($('body'), 1000); });
        }
        );
        
        //pokaż podczas przewijania
        
        $(window).scroll(function()
        {
            
            if($(this).scrollTop()>300) $('.scrollup').fadeIn();
            else $('.scrollup').fadeOut();
        
        }
        );