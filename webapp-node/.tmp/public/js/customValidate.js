$(document).ready(function(){


  $('.form-horizontal').validate({

    rules:{

      name:{
        required:true,
      },
      username:{
        required:true,
      },
      email:{
        required:true,
        email:true,
      },
      password:{
        required:true,
        minlength:6,
      },
      passcnf:{
        required:true,
        minlength:6,
        equalTo:"#password",
      },
      sex:{},
      level:{},

    },
    success:function(element){
      element
      .text('OK!').addClass('valid')
    }
  });

});
