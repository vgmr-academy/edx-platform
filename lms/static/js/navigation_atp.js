function toggleNav() {
  $('#logo_atp_redirect').click(function(){
    window.location.href = '/';
  })
 $('.sub_menu').click(function(){
  var This = $(this);
  var data = This.data('location');
  var other_location = $('.sub_menu').not(this).data('location');
  $('#'+other_location).attr('style','');
  $('#'+data).toggle();
 })

 $(document).bind('click', function(e) {
   if(!$(e.target).is('.sub_menu')) {
     $('.sub_menu').each(function(){
       var This = $(this);
       var data = This.data('location');
       $('#'+data).attr('style','');
     })
   }
 });

 $('#menu_module_apt').find('button').click(function(){
  var This = $(this);
  var data = This.data('location');
  var speed = 750;
  This.parent().toggle();
  $('html, body').animate( { scrollTop: $('#'+data).offset().top -= 148 }, speed );
  return false;
 })

 $('#menu_cat_apt').find('button').click(function(){
   var This = $(this);
   This.parent().hide();
   var data = This.data('location');
   if(data != 'all') {
     $('#menu_cat_apt').find('button').each(function(){
       var data_button = $(this).data('location');
       if(data_button != 'all') {
         $(this).hide();
       }
     })
     $('.atp_course_item').each(function(){
       var data_li = $(this).data('categ');
       if(data_li == data) {
         $(this).show();
       }else{
         $(this).hide();
       }

       $('.atp_dashboard_active_course').hide();
       if(data == 'fundamental' && data_li == 'fundamentals') {
         $(this).show();
       }
     })
     $('html, body').animate( { scrollTop: $('#dashboard_course_in_progress_atp').offset().top -= 148 }, 750 );
     return false;
   }else{
     $('.atp_course_item').attr('style','');
     $('.atp_dashboard_active_course').attr('style','');
     $('#menu_cat_apt').find('button').attr('style','');
     $('html, body').animate( { scrollTop: $('#dashboard_course_in_progress_atp').offset().top -= 148 }, 750 );
     return false;
   }
   var width = $(window).width();
   width = parseInt(width);
   if(width > 583) {
   var covers_length = $('#dashboard_course_in_progress_atp').find('li').length;
   for (var i = 0; i<covers_length;i++) {
    if(i%3 == 0) {
     $('#dashboard_course_in_progress_atp').find('li:eq('+i+')').css('margin-left','0px');
     $('#dashboard_course_in_progress_atp').find('li:eq('+i+')').css('margin-right','3%');
    }else if( i == 0 || i%3 == 1){
     $('#dashboard_course_in_progress_atp').find('li:eq('+i+')').css('margin-right','0px');
     $('#dashboard_course_in_progress_atp').find('li:eq('+i+')').css('margin-left','3%');
    }else{
     $('#dashboard_course_in_progress_atp').find('li:eq('+i+')').css('margin-left','6%');
     $('#dashboard_course_in_progress_atp').find('li:eq('+i+')').css('margin-right','6%');
    }
   }
   var invite_length = $('#dashboard_course_to_do').find('li').length;
   for (var i = 0; i<invite_length;i++) {
    if(i%3 == 0) {
     $('#dashboard_course_to_do').find('li:eq('+i+')').css('margin-left','0px');
     $('#dashboard_course_to_do').find('li:eq('+i+')').css('margin-right','3%');
    }else if( i == 0 || i%3 == 1){
     $('#dashboard_course_to_do').find('li:eq('+i+')').css('margin-right','0px');
     $('#dashboard_course_to_do').find('li:eq('+i+')').css('margin-left','3%');
    }else{
     $('#dashboard_course_to_do').find('li:eq('+i+')').css('margin-left','6%');
     $('#dashboard_course_to_do').find('li:eq('+i+')').css('margin-right','6%');
    }
   }
   var finish_length = $('#dashboard_course_finished').find('li').length;
   for (var i = 0; i<finish_length;i++) {
    if(i%3 == 0) {
     $('#dashboard_course_finished').find('li:eq('+i+')').css('margin-left','0px');
     $('#dashboard_course_finished').find('li:eq('+i+')').css('margin-right','3%');
    }else if( i == 0 || i%3 == 1){
     $('#dashboard_course_finished').find('li:eq('+i+')').css('margin-left','3%');
     $('#dashboard_course_finished').find('li:eq('+i+')').css('margin-right','0px');
    }else{
     $('#dashboard_course_finished').find('li:eq('+i+')').css('margin-left','6%');
     $('#dashboard_course_finished').find('li:eq('+i+')').css('margin-right','6%');
    }
   }
   }else{
    $('#dashboard_course_in_progress_atp').find('li').attr('style','');
    $('#dashboard_course_to_do').find('li').attr('style','');
    $('#dashboard_course_finished').find('li').attr('style','');
   }
 })
}

function navChange() {
 var width = $(window).width();
 width = parseInt(width);
 if(width <= 1022) {
  $('#atp_menu_mobile').click(function(){
    $('#sub_menu').toggle();
  })
 }else{
  $('#sub_menu').attr('style','');
 }
}
function replace_log() {
  var width = $(window).width();
  if(width < 1022) {
    $( "#atp_menu_mobile" ).before( $("#log_user_action") );
  }
}
$(document).ready(function(){
 toggleNav();
 navChange();
 //replace_log();
})

$(window).resize(function(){
 navChange();
 //replace_log();
})
