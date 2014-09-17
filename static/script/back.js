$(function() {
    $(".w-left li a").hover(
      function(){
        $(this).addClass('on');
      },
      function(){
        $(this).removeClass('on');
      }
    )
     $('#startDate').calendar({ btnBar:false}); 
     $('#endDate').calendar({ btnBar:false});   

        $(".w-left li a").click(function(){
           if($(this).next().is(":visible")){
             $(this).next().slideUp() ;
             $(this).find("i").attr("class",'touch') ;
           }else{
             $(this).next().slideDown() ;
             $(this).find("i").attr("class",'off') ;
           }
           $(this).parent().siblings().children("a").next().slideUp() ;
           $(this).parent().siblings().children("a").find("i").attr("class",'touch') ;
           return false ;
       })  
        var index = 0;
        var $li = $(".w-left-inner li") ;
        $li.click(function(){
            index = $li.index(this) ;
            $(".w-right>div").eq(index).show().siblings().hide();
        })
        $("[title='操作日志管理']>a").click(function(){
            $("#operate").show().siblings().hide() ;
        });
        $("#hl1").text(getTime()) ;
        function getTime(){
            var date = new Date() ;
            var year = date.getFullYear() ;
            var month = date.getMonth() + 1 ;
            var day = date.getDate() ;
            var hour = date.getHours() ;
            var minute = date.getMinutes() ;
            month = month<10 ? '0'+ month : month ;
            day = day<10 ? '0'+ day : day ;
            hour = hour<10 ? '0'+ hour : hour ;
            minute = minute<10 ? '0'+ minute : minute ;
            return year + '-' + month + '-' + day + ' ' + hour + ':' + minute ;
        }
})