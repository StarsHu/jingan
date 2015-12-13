$(function () {
  $('.form').each(function() {
    var form = $(this);
    var uri = form.attr('action');
    form.attr('method', 'POST');
    var formGroups = form.find('.form-group');
    var submitWidget = form.find('.form-submit');
    var errBlock = form.find('.form-error-block').last();

    var submitForm = function() {
      errBlock.parents('.form-group').removeClass('has-error');
      errBlock.text('');
      $.post(uri, form.serialize(), function(data, textStatus, jqXHR) {
        if (data.errors) {
          var error = data.errors[0];
          errBlock.parents('.form-group').addClass('has-error');
          errBlock.text(error.message);
        } else if (data.redirect) {
          $(window.location).attr('href', data.redirect);
        } else {
          $(window.location).reload();
        }
      });
      return false;
    }

    form.submit(submitForm);
  });

  $('.datepicker').datepicker({
    language: 'zh-CN',
    todayBtn: 'linked',
    todayHighlight: 'true',
    autoclose: true
  });
});
