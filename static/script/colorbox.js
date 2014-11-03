 var height = document.documentElement.clientHeight;
  var mask = document.getElementById("mask");
  mask.style.height = height + 'px';
  $(".email_recipient").bind("click",function(){
      $("#mask").show();
      $(".email_colorbox").show();
  })
  $(".colorbox_delete").bind("click",function(){
      $("#mask").hide();
      $(".email_colorbox").hide();
  })

  $(".email_sure").bind("click",function(){
      $("#mask").hide();
      $(".email_colorbox").hide();
      var receive_person = $(".receive_person") ;
      var td =  $(".colorbox_send table tr td") ;
      var result = [] ;
      /*receive_person.text()*/
     td.each(function(index,item){
        if($(this).find("input[type='checkbox']").attr("checked") == true){
           result.push($(this).next().text()) ;
        }
     })
     $("#email_person").val(result.join(" ;")) ;
  })