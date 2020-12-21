        jQuery(function($)
        {
            //zresetuj scrolla
            $.scrollTo(0);
            
            $('#link0').click(function() {  setActiveLink1("1"); $.scrollTo($('#about').offset().top, 700); });
            $('#link1').click(function() {  setActive("1"); $.scrollTo($('#about').offset().top, 700); });
            $('#link2').click(function() {  setActive("2"); $.scrollTo($('#howto').offset().top, 700); });
            $('#link3').click(function() {  setActive("3"); $.scrollTo($('#upload').offset().top, 700); });
            $('#link4').click(function() {  setActive("4"); $.scrollTo($('#analysis').offset().top, 700); });
            $('#link5').click(function() {  setActive("5"); $.scrollTo($('#authors').offset().top, 700); });
            $('#link6').click(function() {  removeActive("0"); $.scrollTo($('#main').offset().top + 100000); });

            $('.scrollup').click(function() { $.scrollTo($('body'), 1000); });
        }
        );

        jQuery.expr[':'].regex = function(elem, index, match) {
            var matchParams = match[3].split(','),
                validLabels = /^(data|css):/,
                attr = {
                    method: matchParams[0].match(validLabels) ? 
                                matchParams[0].split(':')[0] : 'attr',
                    property: matchParams.shift().replace(validLabels,'')
                },
                regexFlags = 'ig',
                regex = new RegExp(matchParams.join('').replace(/^\s+|\s+$/g,''), regexFlags);
            return regex.test(jQuery(elem)[attr.method](attr.property));
        }

        function setActive(val) {
            $('div:regex(id, link[0-9])').removeClass('active');
            $('#link' + val).addClass('active');
        }

        function setActiveLink1(val) {
            $('div:regex(id, link[0-9])').removeClass('active');
            $('#link' + val).addClass('active');
        }

        function removeActive() {
            $('div:regex(id, link[0-9])').removeClass('active');
        }
        
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
