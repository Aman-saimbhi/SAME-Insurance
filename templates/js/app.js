var Login = function() {

  var handleLogin = function() {
    $('.login-form').validate({
      errorElement: 'span',
      errorClass: 'help-block',
      focusInvalid: false,
      rules: {
        username: {
          required: true
        },
        password: {
          required: true
        },
        remember: {
          required: false
        }
      },
      messages: {
        username: {
          required: 'Username is required.'
        },
        password: {
          required: 'Password is required.'
        }
      },

      invalidHandler: function(event, validator) {
        $('.alert-danger', $('.login-form')).show();
      },

      highlight: function(element) {
        $(element).closest('.form-group').addClass('has-error');
      },

      success: function(label) {
        label.closest('.form-group').removeClass('has-error');
        label.remove();
      },

      errorPlacement: function(error, element) {
        error.insertAfter(element.closest('.input-icon'));
      },

      submitHandler: function(form) {
        form.submit();
      }
    });

    $('.login-form input').keypress(function (e) {
      if (e.which == 13) {
        if ($('.login-form').validate().form()) {
          $('.login-form').submit();
        }
        return false;
      }
    });

  }

  var handleForgetPassword = function() {

    $('.forget-form').validate({
      errorElement: 'span',
      errorClass: 'help-block',
      focusInvalid: false,
      ignore: "",
      rules: {
        email: {
          required: true,
          email: true
        }
      },
      messages: {
        email: {
          required: "Email field cannot be left blank."
        }
      },
      invalidHandler: function(event, validator) {

      },
      highlight: function(element) {
        $(element).closest('.form-group').addClass('has-error');
      },
      success: function(label) {
        label.closest('.form-group').removeClass('has-error');
        label.remove();
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element.closest('.input-icon'));
      },
      submitHandler: function(form) {
        form.submit();
      }
    });

    $('.forget-form input').keypress(function (e) {
      if (e.which == 13) {
        if ($('.forget-form').validate().form()) {
          $('.forget-form').submit();
        }
        return false;
      }
    })

    jQuery('#forget-password').click(function() {
      jQuery('.login-form').hide();
      jQuery('.forget-form').show();
    });

    jQuery('#back-btn').click(function() {
      jQuery('.login-form').show();
      jQuery('.forget-form').hide();
    });
  }

  var handleRegister = function() {

    function format(state) {
      if (!state.id) return state.text;
      return "<img class='flag' src='img/flags/" + state.id.toLowerCase() + ".png'/>&nbsp;&nbsp;" + state.text;
    }

    $('.register-form input').keypress(function(e) {
      if (e.which == 13) {
        if ($('.register-form').validate().form()) {
          $('.register-form').submit();
        }
        return false;
      }
    });

    jQuery('#register-btn').click(function(){
      jQuery('.login-form').hide();
      jQuery('.register-form').show();
    });

    jQuery('#register-back-btn').click(function(){
      jQuery('.login-form').show();
      jQuery('.register-form').hide();
    });
  }

  return {
    init: function() {
      handleLogin();
      handleForgetPassword();
      handleRegister();
    }
  }
}();
