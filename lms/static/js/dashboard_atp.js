function tma_show_more() {
 $('.tuto_action').click(function(){
  if($('#atp_tuto_arrow_up').hasClass('arrow-right')) {
   $('#atp_tuto_arrow_up').removeClass('arrow-right');
   $('#atp_tuto_arrow_up').addClass('arrow-bottom');
  }else if($('#atp_tuto_arrow_up').hasClass('arrow-bottom')) {
   $('#atp_tuto_arrow_up').removeClass('arrow-bottom');
   $('#atp_tuto_arrow_up').addClass('arrow-right');
  }
  if(!$('#dashboard_header_atp').hasClass('border_atp_head')) {
   $('#dashboard_header_atp').addClass('border_atp_head');
  }else{
   $('#dashboard_header_atp').removeClass('border_atp_head');
  }
  var speed = 1800;
  $('#dashboard_tuto_atp').slideToggle(speed);

  if($(this).find('.arrow-top').length != 0) {
    $('html, body').animate( { scrollTop: $('#dashboard_header_atp').offset().top -= 148 }, speed );
  }
 })
 $('.atp_dashboard_active_course').click(function(){
  var text = $(this).text();
  var cible = $(this).data('cible');
  var key = cible.replace('_atp','');
  var _status = $(this).data('status');
  var _cible = '#'+cible;
  var _courses = courses_atp[key];

  if(text.indexOf('+') != -1) {
    // re render courses
    course_status[key] = true;
    render_course_cards(_courses,_cible,course_status[key],_status,course_category);
    text = text.replace('+','-');
  }else{
    course_status[key] = false;
    render_course_cards(_courses,_cible,course_status[key],_status,course_category);
    text = text.replace('-','+');
  }
  $(this).text(text);
 })
}

$('#menu_cat_apt').find('button').click(function(){
  var This = $(this);
  This.parent().hide();
  var data = This.data('location').replace(/ /g,'').toLowerCase();

  if(data == 'all') {
    course_category = '';
    $('#menu_cat_apt').find('button').removeClass('display_button');
  }else{
    $('#menu_cat_apt').find('button').each(function(){
      var That = $(this);
      if(That.data('location') != 'all') {
        That.addClass('display_button');
      }
    })
    course_category = data;
  }
  render_course_cards(courses_atp.progress_courses,progress_cible,course_status.progress_courses,"cours",course_category);
  render_course_cards(courses_atp.start_courses,start_cible,course_status.start_courses,"invite",course_category);
  render_course_cards(courses_atp.end_courses,end_cible,course_status.end_courses,"finish",course_category);
  $('html, body').animate( { scrollTop: $('#dashboard_course_in_progress_atp').offset().top -= 148 }, 750 );
  return false;
})

function intervalDetectHeight() {
  var height = 0;
  $('.atp_course_title').attr('style','');
  $('.atp_course_title').find('span').each(function(){
   var h = $(this).height();
   h = parseInt(h);
   if(h > height) {
    height = h;
   }
  })
  $('.atp_course_title').css('height',height+'px');
}
$(document).ready(function(){
 tma_show_more();
 intervalDetectHeight();
})
$('.atp_course_listing').on('change',function(){
 intervalDetectHeight();
})
$(window).resize(function(){
 intervalDetectHeight();
})
