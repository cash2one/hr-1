var height = document.documentElement.clientHeight;
//var mask = document.getElementById("mask");
//mask.style.height = height +
$(".colorbox_delete,#sure,#close").bind("click",function(){
    //$("#mask").hide();
    $(".colorbox").hide();
});
  $('#export_b').click(function(){
    $("#export_sign").val('yes');
    $("#ff").submit();
  });
  $("#all").click(function(){
    var count = parseInt($(this).val());
    $("input[name=ids]").each(function(){
      if(count%2 == 0){
        $(this).attr('checked', 'on');
      }else{
        $(this).attr('checked', '');
      }
      $("#all").attr('value', count+1);
    });
  });

  $("#salary_all").click(function(){
    var count = 0;
    var ids = ',';
    $("input[name=ids]").each(function(){
      if($(this).attr('checked') == true){
        count = count + 1;
        ids = ids + $(this).val();
      }
    });
    if (count == 0){
      $("#error").html("请先选择要修改的人员").show();
    }else{
        $(".colorbox").show();
    }
  });

  $("button").click(function(){
    if($(this).parent().attr('tagName') == 'TD'){
        $(".colorbox").show();
        $(this).parent().parent().find("td input").attr('checked', true);
    }
  });

  $("#sure").click(function(){
    if($("#startDate").val().length == 0){
        $("#error").html("请选择时间").show();
    }else{
        var ids = '';
        $("input[name=ids]").each(function(){
          if($(this).attr('checked') == true){
            ids = ids + "," + $(this).val();
          }
        });
        $("#select_vals").val(ids);
        $("#f_change").submit();
    }
  });
