/**
 * 
 * 操作逻辑
 * 
 */

$(document).ready(function() {

  // 产生验证码
  var code = createCode();

  /**
  * 提交表单，验证验证码是否正确
  * 
  * return false or true
  */
    
  $('form').submit(function(){
    var b = true;
    $("#verify").css("display", "none");
    $(".alert").css("display", "none");
    if($( "#password").val().length == 0 ){
      $("#verify").html('<div class="alert alert-error">请输入密码!</div>').show();
      b = false;
    }else if( $("#vali").val() != code ){
      $("#verify").html('<div class="alert alert-error">验证码输入错误!</div>').show();
      b = false;
    }else{
      b = true;
    }
      return b;
  });
  
  /**
   * 点击刷新验证码
   *
   * @return null
   */
  $("#code").click(function() {
    code = createCode();
  });

});

/**
 * 删除药物：如果点击删除药物，从table中删除该行，重新计算总价
 *
 * @param <Obj> obj
 * @return null
 */
function removeMedicine(obj){
  // console.log($(obj).parent());

  // 删除该行
  $(obj).parent().parent().remove();

  // 重新计算总价
  calculatePrice();
}
  

/**
 * 生成验证码
 *
 * @return <String> code
 */
function createCode() {
  var character = new Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z');
  var code = "";
  var code_length = 4;
  var char_length = character.length;
  for (var i = 0; i < code_length; i++) {
    code += character[parseInt(Math.random() * char_length)];
  };
  $("#code").html(code);
  //$("#vali").css('background': code);
  return code;
}


/**
 * 只能输入字母。
 * 
 * @param <String> value
 * @return <boolean> 
 */
function checkChar(value) {
  var pattern = new RegExp(/^[a-zA-Z]+$/);
  if (value.match(pattern))
    return true;
  else
    return false;  
}

/**
 * 只能输入数字，可带小数。
 * 
 * @param <String> value
 * @return <boolean> 
 */
function checkNum(value) {
  var pattern = new RegExp(/^\d+[.]?\d*$/);
  if (value.match(pattern))
    return true;
  else
    return false;
}

/**
 * 数字大于等于0。
 * 
 * @param <Number> value
 * @return <boolean> 
 */
function checkSize(value) {
  var pattern = new RegExp(/^\d+[.]?\d*$/);
  if (value.match(pattern))
    return (parseFloat(value) >= 0);
  else
    return false;
}
/**
 * 只能输入中文。
 * 
 * @param <String> value
 * @return <boolean> 
 */
function checkCN(value) {
  var pattern = new RegExp(/^[\u4E00-\u9FA5]+$/);
  if (value.match(pattern)){
    return true;
  }else{
    return false;  
  }
}



