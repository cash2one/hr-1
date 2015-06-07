$("#audit").bind("click",function(){
  var all_person = ''
  $("input[name=all_person]").each(function() {
    if($(this).attr("checked")){
      all_person = all_person + "," + $(this).val();
    }
  });
  if(all_person.length == 0){
      $("#error").html("请选择要审核通过的人员").show();
  }else{
    var b = confirm('确认通过审核?');
    if(b){
      $("#select_id").val(all_person);
      _data = {};
      _data['employees_id'] = all_person;
      $.ajax({
          type: 'post',
          dataType: "json",
          data: _data,
          url: '/manager/audit/',
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