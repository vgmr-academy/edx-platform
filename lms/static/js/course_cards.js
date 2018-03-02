/* courses cards generator */
var start_cible = "#start_courses_atp";
var progress_cible = "#progress_courses_atp";
var end_cible = "#end_courses_atp";

function render_course_cards(data,cible,status,action,category) {
  $(cible).html('');
  var rows = data.length;
  if(!status) {
      rows = 4;
    var Width = window.screen.width;
    if(Width <= 1600) {
      rows = 3;
    }
    if(Width <= 1196) {
      rows = 2;
    }
    if(Width <= 814) {
      rows = 1;
    }
    if(rows > data.length) {
      rows = data.length;
    }
  }
  if(category != 'all' && category != '') {
    rows = data.length;
  }
  for(var i=0;i<rows;i++) {
    var _cur = data[i];
    if(category == '') {
      course_card(
        _cur.category,
        _cur.course_id,
        _cur.course_img,
        _cur.course_progression,
        _cur.duration,
        _cur.required,
        _cur.display_name_with_default,
        _cur.content_data,_cur.percent,
        _cur.passed,
        action,
        cible
      );
    }else{
      if(_cur.category.replace(/ /g,'').toLowerCase() == "fundamentals") {
        _cur.category = "fundamental";
      }
      if(category == _cur.category.replace(/ /g,'').toLowerCase()) {
        course_card(
          _cur.category,
          _cur.course_id,
          _cur.course_img,
          _cur.course_progression,
          _cur.duration,
          _cur.required,
          _cur.display_name_with_default,
          _cur.content_data,
          _cur.percent,
          _cur.passed,action,cible
        );
      }
    }
  }
  $(cible).append('<span style="display:block;clear:left"></span>');
  intervalDetectHeight();
}
function button_views() {
  $('.atp_dashboard_active_course').each(function(){

    var Width = window.screen.width;

    var devices = [
      {min_width:0,max_width:814,number:1},
      {min_width:814,max_width:1196,number:2},
      {min_width:1196,max_width:1600,number:3},
      {min_width:1600,max_width:100000,number:4}
    ];

    var _number = $(this).data('number');

    for(i=0;i<3;i++) {

      var min_width = devices[i].min_width;
      var max_width = devices[i].max_width;
      var number = devices[i].number;

      if(Width >= min_width && Width < max_width) {
        if(_number <= number) {
          $(this).addClass('display_button');
        }else{
          $(this).removeClass('display_button');
        }
      }
    };
  });
}

$(document).ready(function(){
  render_course_cards(
    courses_atp.progress_courses,
    progress_cible,
    course_status.progress_courses,
    "cours",
    course_category
  );
  render_course_cards(
    courses_atp.start_courses,
    start_cible,
    course_status.start_courses,
    "invite",
    course_category
  );
  render_course_cards(
    courses_atp.end_courses,
    end_cible,
    course_status.end_courses,
    "finish",
    course_category
  );
  button_views();
})
$(window).resize(function(){
  render_course_cards(
    courses_atp.progress_courses,
    progress_cible,
    course_status.progress_courses,
    "cours",
    course_category
  );
  render_course_cards(
    courses_atp.start_courses,
    start_cible,
    course_status.start_courses,
    "invite",
    course_category
  );
  render_course_cards(
    courses_atp.end_courses,
    end_cible,
    course_status.end_courses,
    "finish",
    course_category
  );
  button_views();
})
