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

$(".colorbox_delete2, .colorbox_delete2, #sure, #close").bind("click",function(){
    //$("#mask").hide();
    $(".colorbox2, .colorbox3").hide();
});

// 单位查询一键导出员工, 导出项提示框
$(".company_export").click(function(){
    $(".colorbox3").show();
    $("#export_company_id").val($(this).attr('value'));
});

$("#company_export_sure").click(function(){
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
      $("#select_id").val('all');
      $("#select_form").submit();
  }
});

// 解除劳务合同
$("#cancel_contract").click(function(){
  var all_person = ''
  $("input[name=all_person]").each(function() {
    if($(this).attr("checked")){
      all_person = all_person + "," + $(this).val();
    }
  });
  if(all_person.length == 0){
      $("#error").html("请选择要解除合同的人员").show();
  }else{
    var b = confirm('确认解除合同?');
    if(b){
        _data = {};
        _data['employees_id'] = all_person;
        $.ajax({
            type: 'post',
            dataType: "json",
            data: _data,
            url: '/labour/employee/cancel_contract/',
            success: function(Data) {
              if(Data['result']){
                alert('已解除成功');
                location.reload();
              }else{
                alert('解除失败');
              }
            }
        });
    }
  }
});

// 批量删除员工信息
$("#delete_select").click(function(){
  var all_person = '';
  $("input[name=all_person]").each(function() {
    if($(this).attr("checked")){
      all_person = all_person + "," + $(this).val();
    }
  });
  if(all_person.length == 0){
      $("#error").html("请选择要删除的人员").show();
  }else{
    var b = confirm('确认删除?');
    if(b){
        _data = {};
        _data['employees_id'] = all_person;
        $.ajax({
            type: 'post',
            dataType: "json",
            data: _data,
            url: '/manager/company/employees/delete/',
            success: function(Data) {
              if(Data['result']){
                alert(Data['msg']);
                location.reload();
              }else{
                alert(Data['msg']);
              }
            }
        });
    }
  }
});


// 删除单个员工信息
$(".delete").click(function(){
  var all_person = "," + $(this).attr("name");
  var b = confirm('确认删除?');
  if(b){
      _data = {};
      _data['employees_id'] = all_person;
      $.ajax({
          type: 'post',
          dataType: "json",
          data: _data,
          url: '/manager/company/employees/delete/',
          success: function(Data) {
            if(Data['result']){
              alert(Data['msg']);
              location.reload();
            }else{
              alert(Data['msg']);
            }
          }
      });
  }
});


// 删除单个公司信息
$(".company_delete").click(function(){
  var company_id = $(this).attr("value");
  var b = confirm('确认删除?');
  if(b){
      _data = {};
      _data['company_id'] = company_id;
      $.ajax({
          type: 'post',
          dataType: "json",
          data: _data,
          url: '/manager/companys/',
          success: function(Data) {
            if(Data['result']){
              alert(Data['msg']);
              location.reload();
            }else{
              alert(Data['msg']);
            }
          }
      });
  }
});