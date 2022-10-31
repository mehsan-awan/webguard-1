function SaveTest() {
   $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      data:$("#BotValues").val(),

      url: "/SaveBotValues/",
      dataType: "json",

      success: function (result) {
        $('#Bot_Config_sucess').text("Successfully Saved New URL's");
        $('#Total_Scanning_stats').text(result.Header_Stats["New_Website_Count"]);
      },
      error: function(err) {
      $('#Bot_Config_sucess').css('color', 'Red');
      $('#Bot_Config_sucess').text("Error: Not Saved...!!");
      }
  });
}


function getTrustedConfigBtn() {
    var selectedValue=$('#trustedCopies').find(":selected").text();
  $.ajax({
          type: "GET",
          contentType: "application/json; charset=utf-8",
          url: "/GetTrustedConfig",
          dataType: "json",

          data:{url:selectedValue},
          beforeSend: function() {

          },
          success: function (result) {
               //debugger;
               $("#textareaforoutput").val(result.Urls)
               $("#dateTimeForLastConfig").html(GetCurrentDate()+" "+GetCurrentTime());
          },
          error: function(err) {
          }
    });
}


function StartBtn() {
    console.log("Start Button")

    $('#Bot_Status').text("Running");
    $('#Bot_Status_Stat').text("Bot is Now Running....!!");

    $.ajax({
      type: "GET",
      contentType: "application/json; charset=utf-8",
      url: "/StartBot",
      dataType: "json",
      beforeSend: function() {
      },
      success: function (result) {
           // do something here
      },
      error: function(err) {
      }


 });
}


function StopBtn() {
    console.log("StopBtn Button")
     $.ajax({
      type: "GET",
      contentType: "application/json; charset=utf-8",
      url: "/StopBot",
      dataType: "json",
      beforeSend: function() {
      },
      success: function (result) {
           // do something here
      $('#Bot_Status').text("Stopped");
    $('#Bot_Status_Stat').text("Bot is Stopped....!!");
    },
      error: function(err) {
      $('#Bot_Status').text("Stopped");
    $('#Bot_Status_Stat').text("Bot is Stopped....!!");
      }
 });

}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function revert_back_changes() {
    console.log("Btn Clicked")

    var back_website = document.getElementById("back_website").value;
    var ftp_backend_server = document.getElementById("ftp_backend_server").value;
    var ftp_backend_user = document.getElementById("ftp_backend_user").value;
    var ftp_backend_pass = document.getElementById("ftp_backend_pass").value;


    var csrftoken = getCookie('csrftoken');

    $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    headers: {
       'X-CSRFToken': csrftoken
    },

    data: JSON.stringify({
                back_website : back_website,
                ftp_backend_server : ftp_backend_server,
                ftp_backend_user : ftp_backend_user,
                ftp_backend_pass : ftp_backend_pass,
            }),

    url: "/revertBackChanges/",
    dataType: "json",

    success: function (result) {
      alert("Successfully restored website!!");
//      window.location.replace("/admin/products/edit/"+result.id);

    },
    error: function(err) {
      alert("Failed to restore website. Please try again.");
    }
    });
}


function revert_front_changes() {
    console.log("Btn Clicked")

    var front_website = document.getElementById("front_website").value;
    var ftp_frontend_server = document.getElementById("ftp_frontend_server").value;
    var ftp_frontend_user = document.getElementById("ftp_frontend_user").value;
    var ftp_frontend_pass = document.getElementById("ftp_frontend_pass").value;


    var csrftoken = getCookie('csrftoken');

    $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    headers: {
       'X-CSRFToken': csrftoken
    },

    data: JSON.stringify({
                front_website : front_website,
                ftp_frontend_server : ftp_frontend_server,
                ftp_frontend_user : ftp_frontend_user,
                ftp_frontend_pass : ftp_frontend_pass,
            }),

    url: "/revertFrontChanges/",
    dataType: "json",

    success: function (result) {
      alert("Successfully restored website!!");
//      window.location.replace("/admin/products/edit/"+result.id);

    },
    error: function(err) {
      alert("Failed to restore website. Please try again.");
    }
    });
}


