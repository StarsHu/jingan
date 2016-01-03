function formAjaxSubmit(child, target){
  var form = child.parents('form');
  var uri = form.attr('action');
  $.post(uri, form.serialize(), function(data, textStatus, jqXHR) {
    if (data.errors) {
      var error = data.errors[0];
      if(error) {
        alert(error.message);
      }
    } else if (data.redirect) {
      $(window.location).attr('href', data.redirect);
    } else {
      location.reload();
    }
  });
}

function formInit(form) {
    var uri = form.attr('action');
    form.attr('method', 'POST');
    var formGroups = form.find('.form-group');
    var submitWidget = form.find('.form-submit');
    var errBlock = form.find('.form-error-block').last();

    function submitForm() {
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
          location.reload();
        }
      });
      return false;
    }

    form.submit(submitForm);
    return false;
}

$(function () {
  $('.form').each(function() {
    formInit($(this));
  });

  $('[data-toggle="popover"]').popover();

  $('.datepicker').datepicker({
    language: 'zh-CN',
    todayBtn: 'linked',
    todayHighlight: 'true',
    autoclose: true
  });
});
