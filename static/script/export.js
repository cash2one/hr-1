var height = document.documentElement.clientHeight;
//var mask = document.getElementById("mask");
//mask.style.height = height + 'px';
$("#payment").bind("click",function(){
    //$("#mask").show();
    $(".colorbox").show();
});
$(".colorbox_delete,#sure,#close").bind("click",function(){
    //$("#mask").hide();
    $(".colorbox").hide();
});

$("#export").bind("click",function(){
  $("#error").hide();
  var all_person = ''
  $("input[name=all_person]").each(function() {
    if($(this).attr("checked")){
      all_person = all_person + "," + $(this).val();
    }
  });
  if(all_person.length == 0){
      $("#error").html("请选择要导出的人员").show();
  }else{
      $("#select_id").val(all_person);
      $(".colorbox2").show();
  }
});

$("#sure").click(function(){
  $("#error").hide();
  var items_str = ''
  $("input[name=items]").each(function() {
    if($(this).attr("checked")){
      items_str = items_str + "," + $(this).val();
    }
  });
  if(items_str.length == 0){
      $("#error").html("请选择要导出的条目").show();
  }else{
      $("#item_id").val(items_str);
      $("#select_form").submit();
  }
});

$(".colorbox_delete2,#sure,#close").bind("click",function(){
    //$("#mask").hide();
    $(".colorbox2").hide();
});