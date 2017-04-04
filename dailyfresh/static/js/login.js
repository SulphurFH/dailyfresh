 $(function(){
   name_error = false
   pwd_error = false
   
   if ({{user_error}} == 2){
     $('.user_error').html('用户名不存在').show();
   };

   if ({{user_error}} == 1){
     $('.pwd_error').html('密码错误').show();
   };

   $('#username').blur(function(){
     if($('#username').val().length == 0){
       $('.user_error').html('请输入用户名').show();
       name_error = true;
     }
     else{
       $('.user_error').hide();
       name_error = false;
     }
   });

   $('#pwd').blur(function(){
     if($('#pwd').val().length == 0){
       $('.pwd_error').html('请输入密码').show();
       pwd_error = true;
     }
     else{
       $('.pwd_error').hide();
       pwd_error = false;
     }
   });

   $('#reg_form').submit(function(){
     $('#username').blur();
     $('#pwd').blur();

     return !name_error && !pwd_error
   })
 })
