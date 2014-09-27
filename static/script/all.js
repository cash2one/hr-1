var foo = {
    mouseover : function(){
        $(this).css({"color":"#ffffff","background-color":"#369"});
	    $(this).find('span.logo_small_one').attr("background","url('/static/image/logo_laowu_one.png') left top no-repeat");
    },
    mouseout : function(){
    	$(this).css({"color":"#222222","background-color":"#ffffff"});
	   	$(this).find('span.logo_small_one').attr("background","url('/static/image/logo_laowu_two.png') left top no-repeat");
	}
}
$(function() {
	   $("a.big_txt").bind("mouseover",foo.mouseover) ;
	   $("a.big_txt").bind("mouseout",foo.mouseout) ;
	   $("a.big_txt").bind("click",function(){
	   	   if($(this).next().is(":hidden")){
              $(this).next().slideDown() ;
              $(this).find("i").attr("class",'off') ;
               foo.mouseover() ;
              $(this).unbind("mouseover mouseout") ;
	   	   }else{
              $(this).next().slideUp() ;
              $(this).find("i").attr("class",'touch') ;
              $(this).bind("mouseover",foo.mouseover) ;
              $(this).bind("mouseout",foo.mouseout) ;
	   	   }
           $(this).parent().siblings().children("a").next().slideUp() ;
           $(this).parent().siblings().children("a").find("i").attr("class",'touch') ;
           return false ;
	   })
	   $('#startDate').calendar({ btnBar:false}); 
     $('#startDate1').calendar({ btnBar:false}); 
     $('#startDate2').calendar({ btnBar:false}); 
     $('#startDate3').calendar({ btnBar:false}); 
     $('#startDate4').calendar({ btnBar:false}); 
     $('#startDate5').calendar({ btnBar:false}); 
     $('#startDate6').calendar({ btnBar:false}); 
     $('#startDate7').calendar({ btnBar:false}); 
	   $('#endDate').calendar({ btnBar:false});   

        $(".w-left li a.small_txt").click(function(){
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
       $("#current_time,#hl1").text(getTime()) ;


    /*获取当前时间*/
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
    /*end*/
    /*三级菜单儿灰色背景的添加*/ 
      $("ul.w-left-inner li.inner_txt").bind("mouseenter",function(){
    	$(this).addClass("inner_on").siblings().removeClass("inner_on") ;
    })
    /*end*/

    /*修改按钮效果*/
    $(".modify_salary").bind('click',function(event){
      var $parent = $(this).parent("td") ;
      var $input = $('<input type="text" name="salary" />') ;
      var $button = $(".modify_salary").clone(true) ;
      var $span = $("<span></span>") ;
      $parent.empty();
      $input.appendTo($parent) ;
      $input.css("width","70px") ;  
    event.stopPropagation() ;
      $("body").click(function(){
      $parent.empty();
      var $value = $span.text($input.val()) ;
      $value.appendTo($parent) ;
      $button.appendTo($parent) ;
    })
      $input.click(function(event){
        event.stopPropagation() ;
      });
    })

    /*全选操作*/
    $(".select_first").click(function(){
      if($("input[name='all_danwei']").attr("checked") == true){
        $(this).closest("tr").nextAll("tr").find("th>input[type='checkbox']").attr("checked",false) ;
      }else{
        $(this).closest("tr").nextAll("tr").find("th>input[type='checkbox']").attr("checked",true) ;
      } 
  })
  $(".select_second").click(function(){
      if($("input[name='all_person']").attr("checked") == true){
        $(this).closest("tr").nextAll("tr").find("th>input[type='checkbox']").attr("checked",false) ;
      }else{
        $(this).closest("tr").nextAll("tr").find("th>input[type='checkbox']").attr("checked",true) ;
      } 
  })
   /*end*/
})