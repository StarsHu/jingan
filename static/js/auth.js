
var checkPasswordSame = function() {
  var newPassword = $('input#newPassword').val();
  var newPasswordAgain = $('input#newPasswordAgain').val();
  if (newPassword == newPasswordAgain) {
    $('#newPasswordGroup').removeClass('has-error');
    $('#newPasswordError').text('');
    $('#newPasswordSubmit').removeAttr('disabled');
  } else {
    $('#newPasswordGroup').addClass('has-error');
    $('#newPasswordError').text('两次输入密码不一致.');
    $('#newPasswordSubmit').attr('disabled', 'disabled');
  }
};
