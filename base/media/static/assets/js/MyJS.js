
//Generating Table for reuslts on REsutls screen
var table;
$(document).ready( function () {
    table=$('#myTable').DataTable();
       toastr.options = {
          "closeButton": true,
          "debug": false,
          "newestOnTop": true,
          "progressBar": true,
          "positionClass": "toast-bottom-center",
          "preventDuplicates": false,
          "onclick": null,
          "showDuration": "300",
          "hideDuration": "1000",
          "timeOut": "5000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
    }

} );


//Index page resources button
$("#resourcesBtn").click(function() {
    GetResources(1);
});


//Stoping Bot
$("#StopBtn").click(function() {
//    GetResources(1);
  $.ajax({
      type: "GET",
      contentType: "application/json; charset=utf-8",
      url: "/StopBot",
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





});

//Starting Bot
$("#StartBtn").click(function() {
    $('#Bot_Status').text("Running");
    $('#Bot_Status_Stat').text("Bot is Now Running....!!");
  $.ajax({
      type: "GET",
      contentType: "application/json; charset=utf-8",
      url: "/StartBot",
      beforeSend: function() {
      },
      success: function (result) {
           // do something here
      },
      error: function(err) {
      }
 });
});



//Need to code not called yet and not working yet, function for creating or updating URL file from UI
$("#saveConfigBot").click(function() {
     $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      data:$("#BotValues").val(),
      url: "/SaveBotValues",
      success: function (result) {
        $('#Bot_Config_sucess').text("Successfully Saved New URL's")
        $('#Total_Scanning_stats').text(result.Header_Stats["New_Website_Count"]);
      },
      error: function(err) {
      $('#Bot_Config_sucess').css('color', 'Red');
      $('#Bot_Config_sucess').text("Error: Not Saved...!!")
      }
 });
});



//Call/Function for getting trusted copies in cache
$("#getTrustedConfigBtn").click(function() {

var selectedValue=$('#trustedCopies').find(":selected").text();

debugger;

  $.ajax({
          type: "GET",
          contentType: "application/json; charset=utf-8",
          url: "/GetTrustedConfig",
          data:{url:selectedValue},
          beforeSend: function() {

          },
          success: function (result) {
               debugger;
               $("#textareaforoutput").val(result.Urls)
               $("#dateTimeForLastConfig").html(GetCurrentDate()+" "+GetCurrentTime());

          },
          error: function(err) {

          }
    });
});


function GetUrls(){
    $.ajax({
          type: "GET",
          contentType: "application/json; charset=utf-8",
          url: "/GetUrls",
          beforeSend: function() {
          },
          success: function (result) {
          debugger;
               var ks = result.Urls.split("\n");
                for(var i=0;i<ks.length;i++){
                    var o = new Option(ks[i],ks[i]);
                    //$(o).html("option text");
                    $("#trustedCopies").append(o);

                }

               $("#textareaforoutput").val(result.Urls)
               $("#dateTimeForLastConfig").html(GetCurrentDate()+" "+GetCurrentTime());
          },
          error: function(err) {
          }
     });
}


//Getting for getting current date
function GetCurrentDate(){
  var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
    var dateObj = new Date();
    var month = monthNames[dateObj.getMonth()];
    var day = String(dateObj.getDate()).padStart(2, '0');
    var year = dateObj.getFullYear();
    var output = month  + ' / '+ day  + ' / ' + year;

    return output;
}
//Getting for getting current time
function GetCurrentTime(){
    var dt = new Date();
    var h =  dt.getHours(), m = dt.getMinutes();
    var _time = (h > 12) ? (h-12 + ':' + m +' PM') : (h + ':' + m +' AM');
    return _time;
    }

//Pupolating Result table on result page, Iteratively adding pages
function GetLogs(){
  $.ajax({
          type: "GET",
          contentType: "application/json; charset=utf-8",
          url: "/GetLogs",
          beforeSend: function() {
          },
          success: function (result) {
              $.each(result.Result, function(index, value) {

                    AddRows(value);
            });
          },
          error: function(err) {
          }
    });}

$("#Get_Logs_Try").click(function() {
//    $('#example').DataTable({});
//    $('#exampletry').DataTable({});
    GetLogs();
    GetLogsTry();
});

function GetLogsTry(){
  $.ajax({
          type: "GET",
          contentType: "application/json; charset=utf-8",
          url: "/GetLogsTry",
          beforeSend: function() {
          },
          success: function (result) {
            debugger;
              $.each(result.Result, function(index, value) {
                    AddRowsTry(value,index);

             $('#Earlier_Results_Status').css('color', 'Green');
             $('#Earlier_Results_Status').text("Sucess...!!")

            });
          },
          error: function(err) {
          $('#Earlier_Results_Status').css('color', 'Red');
             $('#Earlier_Results_Status').text("Error...!!")
          }
    });
}

function AddRowsTry(data,index) {
//    <img  style='height:50px;width:50px;' src='/Images/"+Image_Name[0].toString()+"' />
//    "<img style='height:30px;' src='"+result.results[index]["Country Flag"]+"'/>"



    console.log(data);



    if(data.FileData["Line Test"] == "Secure"){
        Line_Test = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"
        Hack_Words = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"

    }else{
        Line_Test = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png'/>"

        if(data.FileData["Hack Words"] == "Secure"){
            Hack_Words = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"
        }else{
            Hack_Words = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png' />"
        }
    }

    if(data.FileData["Hash"] == "Secure"){
        Hash = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"
    }else{
        Hash = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png'/>"
    }
    if(data.FileData["DOM"] == "Secure"){
        DOM = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"
    }else{
        DOM = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png'/>"
    }
    if(data.FileData["Tag Count"] == "Secure"){
        Tag_Count = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"
    }else{
        Tag_Count = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png'/>"
    }
    if(data.FileData["Image Comparison"] == "Secure"){
        Image_Comparison = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"
    }else{
        Image_Comparison = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png'/>"
    }
    if(data.FileData["SSL"] == "Secure"){
        SSL = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"
    }else{
        SSL = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png'/>"
    }
    if(data.FileData["AI 1"] == "Secure"){
        AI1 = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"
    }else{
        AI1 = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png'/>"
    }
    if(data.FileData["AI 2"] == "Secure"){
        AI2 = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Red.png' alt='Not Working'/>"
    }else{
        AI2 = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png'/>"
    }
    if(data.FileData["AI 3"] == "Secure"){
        AI3 = "<img  style='height:50px;width:50px;' src='/static/assets/img/brand/Green.png' alt='Not Working'/>"
    }else{
        AI3 = "<img  style='height:50px;width:50px;' alt='Not Working' src='/static/assets/img/brand/Red.png/>"
    }
//    Details = "<a id='Details_for_Results' href=''>Details</a>";
     Details = "<button  data-details='"+data.FileData.Final_Report+"' onclick='ShowDetailedReport(this)'  class='Tablebtn_"+index+" btn btn-primary' >Detail Report</button>";
    //debugger;
    $('#exampletry').dataTable().fnAddData( [
        Details,
//        data.FileName,
         "<a target='_blank' href='" + "/downloadReport?id=" + data.FileName  + "'>" + data.FileName + "</a>",
//        "<a target='_blank' href='" + "/makeReportPage?id=" + data.DateTime  + "'>" + data.DateTime + "</a>",
         data.DateTime,
        Line_Test,
        Hack_Words,
        Hash,
        Tag_Count,
        DOM,
//        Tag_Count,
        Image_Comparison,
        SSL,
//        AI1+"  "+AI2+"  "+AI3,
        data.FileData.Severity,
         ] );




}

function ShowDetailedReport(Obj){

    $('.modal-dialog').css("width","1300px");
    $('.modal-dialog').css("max-width","1300px");

    $("#ImageToZoomIn").remove();
    $("#ModalMainBody").html("<pre>"+$(Obj).data("details")+"</pre>");
    $('#myModal').modal('show');

}

function GetImageLogs(){
  $.ajax({
          type: "GET",
          contentType: "application/json; charset=utf-8",
          url: "/GetImageLogs",
          beforeSend: function() {
          },
          success: function (result) {
          debugger;
              $.each(result.Result, function(index, value ) {
                   var DataTime = value.match(/(\d{4}\-\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)\s*/gi);
                   var URL = value.match(/\s*(.+?)\s/gi);
                   var Image_Name = value.match(/\s*(.+)/gi);
                    if(URL[0] != null || URL[0]!= undefined)
                    {
                         $('#Images_Table').dataTable().fnAddData([
                                URL[0].toString(),
                                DataTime[0].toString(),
                                "<a onclick='ShowImage(this.id)' id='"+index+"' > <img id='Image_"+index+"' style='height:50px;width:50px;' src='/Images/"+Image_Name[0].toString()+"' /> </a>"
                         ]);
                    }
            });
          },
          error: function(err) {
          }
    });
}



function ShowImage(ImageId){
    $("#ImageToZoomIn").attr("src",$('#Image_'+ImageId).attr("src"));
    $('#myModal').modal('show');
}


//Getting live system resources from system, called from index page to get live resources
function GetResources(status){
  $.ajax({
          type: "GET",
          contentType: "application/json; charset=utf-8",
          url: "/GetResources",
          beforeSend: function() {
          },
          success: function (result) {
            GaugeCPU(0,100,result.CPU["Percentage"],status);
            GaugeRAM(0,result.Memory["Total"].toFixed(2),result.Memory["Used"],status);
            GaugeNETWORK(0,result.Network["Total"],result.Network["Active"],status);
            $('#Total_Scanning_stats').text(result.Header_Stats["Total_Files"])
            $('#Last_Config_stats').text('Since ' + result.Header_Stats["Config_Last_Modified"])
            $('#HDD_Stats').text(result.Header_Stats["HDD_Percentage"])
            $('#HDD_Total_Used').text(result.Header_Stats["HDD_Total_Used"])
            if(result.Header_Stats["Bot_Status"] == 1){
                $('#Bot_Status').text("Running")
                $('#Bot_Status_Stat').text("Bot is Now Running.....!!")
                $('#Bot_Status_Stat_again').text("Updating Live Status")
            }else{
                $('#Bot_Status_Stat').text("Bot is waiting for command.....!!")
                $('#Bot_Status').text("Stopped")
                $('#Bot_Status_Stat_again').text("Bot is not Running")
            }
            $('#Scan_per_minutes').text(result.Header_Stats["Scans_per_minutes"])

          },
          error: function(err) {
          }
    });
}

//Gerneral funciton to get all live resources
$(document).ready(function() {
      dropdownAccessLogs();
      $('#example1').DataTable({});
      $('#example').DataTable({});

      $('#Images_Table').DataTable();
      $('#exampletry').DataTable({});

      GetResources(0);
      LoadBotValues();
      GetUrls();


//     var elem = document.querySelector('#Tablebtn');
//     $('Tablebtn').css('background-color','#008CBA');
//     $('Tablebtn').css('font-size','12px');



});

function dropdownAccessLogs(){

          var myOptions = {}
          $.ajax({
          type: "GET",
          contentType: "application/json; charset=utf-8",
          url: "/GetBotValues",
          beforeSend: function() {
          },
          success: function (result) {
//          alert(result);
//            alert("Hello working");
//          var i;
//          for (i = 0; i < result.length; i++) {
////              myOptions.items.push({i: result[i]});
//            }
          },
          error: function(err) {
          alert("Error: Access Log Drop Down List Not Initiallized...!!\n\n                     System Working Properly");
          }});


            //Appending items into the dropdown list
            //Appending items into the dropdown list
//            var myOptions = {
//                val1 : 'Blue',
//                val2 : 'Orange'
//            };
            var mySelect = $('#dropdownMenuButtonAccessLogs');
            $.each(myOptions, function(val, text) {
                mySelect.append(
                    $('<option></option>').val(val).html(text)
                );
            });

}


$("#Get_Images").click(function() {
GetImageLogs();
});

function AddRows(data) {
    $('#example').dataTable().fnAddData( [
        data.FileName,
        data.DateTime,
        data.FileData["Line Test"],
        data.FileData["Hack Words"],
        data.FileData["Hash"],
        data.FileData["DOM"],
        data.FileData["Tag Count"],
        data.FileData["Image Comparison"],
        data.FileData["SSL"],
//        data.FileData["AI 1"]+" / "+data.FileData["AI 2"]+" / "+data.FileData["AI 3"],
        data.FileData["SSL"]
         ] );
}

function GaugeCPU(min,max,value,status){

if(status==1){
    g1.refresh(value);
}else{
  g1 = new JustGage({
        id: 'gaugeCPU',
        value: value,
        min: min,
        max: max,
        title: "Visitors",
        symbol: '%',
        pointer: true,
        pointerOptions: {
          toplength: -15,
          bottomlength: 10,
          bottomwidth: 12,
          color: '#8e8e93',
          stroke: '#ffffff',
          stroke_width: 3,
          stroke_linecap: 'round'
        },
        gaugeWidthScale: 0.6,
        counter: true,
      });
}
}
function GaugeRAM(min,max,value,status) {
if(status==1){
    g2.refresh(value);
}else{
  g2 = new JustGage({
        id: 'gaugeRAM',
        value: value,
        min: min,
        max: max,
        symbol: ' GB',
        pointer: true,
        pointerOptions: {
          toplength: -15,
          bottomlength: 10,
          bottomwidth: 12,
          color: '#8e8e93',
          stroke: '#ffffff',
          stroke_width: 3,
          stroke_linecap: 'round'
        },
        gaugeWidthScale: 0.6,
        counter: true,

      });
      }
}
function GaugeNETWORK(min,max,value,status){
if(status==1){
    g3.refresh(value);
}else{

  g3 = new JustGage({
        id: 'gaugeNETWORK',
        value: value,
        min: min,
        max: max,
        symbol: '',
        pointer: true,
        pointerOptions: {
          toplength: -15,
          bottomlength: 10,
          bottomwidth: 12,
          color: '#8e8e93',
          stroke: '#ffffff',
          stroke_width: 3,
          stroke_linecap: 'round'
        },
        gaugeWidthScale: 0.6,
        counter: true,

      });
      }
}
function LoadBotValues(){
 $.ajax({
          type: "GET",
          contentType: "application/json; charset=utf-8",
          url: "/GetBotValues",
          beforeSend: function() {
          },
          success: function (result) {

            $("#BotValues").val(result);
          },
          error: function(err) {
          }});
}
$("#GetAccessLogs").click(function() {
    $('#AccessLogStatus').css('color', 'Black');
      $('#AccessLogStatus').text("Getting Logs and Parsing. Please wait...")
     $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      data:$("#BotValues").val(),
      url: "/GetAccessLogs",
      success: function (result) {

        toastr["success"]("Logs Has Been Generated Successfully.");
        $("#GetAccessLogs").attr("disabled",true);
        $.each(result.results, function(index, value ) {
                         $('#example1').dataTable().fnAddData([
                                 result.results[index]["IP"],
                                 "Date Time Here",
                                 result.results[index]["IP"],
                                 result.results[index]["Country Code"],
                                 result.results[index]["Country Name"],
                                 result.results[index]["Longitude"],
                                 result.results[index]["Latitude"],
                                 "<img style='height:30px;' src='"+result.results[index]["Country Flag"]+"'/>"
                         ]);
            });
            $('#AccessLogStatus').css('color', 'Green');
          $('#AccessLogStatus').text("Sucess...!!")
            var interval = setInterval(function() {
                $("#GetAccessLogs").attr("disabled",false);
            }, 3000);
      },
      error: function(err) {
      $('#AccessLogStatus').css('color', 'Red');
      $('#AccessLogStatus').text("Error: Not Getting Logs...!!")
      }
 });
});

$("#GetModLogs").click(function() {

$("#Mode_Log_Picture").attr("src", "");
        debugger;
//Ajax call for getting parse image for mod logs
     $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      data:$("#BotLogs").val(),
      url: "/GetModLogsPicture",
      success: function (result) {

//            toastr["success"]("Logs Has Been Generated Successfully.");
            $("#GetModLogs").attr("disabled",true);

//            $('#Mode_Log_Picture').attr("src", result.results["Pic"]);
            $("#Mode_Log_Picture").attr("src", "http://192.168.1.165/report.png");

            $('#ModLogStatus').css('color', 'Green');
            $('#ModLogStatus').text("Success...!!")
            $("ModLogPicHeading").css("display", "");
            var interval = setInterval(function() {
                $("#GetModLogs").attr("disabled",false);
            }, 3000);
      },
      error: function(err) {
      $('#ModLogStatus').css('color', 'Red');
      $('#ModLogStatus').text("Error: Not Getting Logs...!!")
      alert("Error");
      }
 });

//Ajax call for text area mod logs
     $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      data:$("#BotLogs").val(),
      url: "/GetModLogs",
      success: function (result) {

            toastr["success"]("Logs Has Been Generated Successfully.");

            $("#GetModLogs").attr("disabled",true);
            $('#Text_Area_Logs').text(result);
            $('#ModLogStatus').css('color', 'Green');
            $('#ModLogStatus').text("Sucess...!!")
            var interval = setInterval(function() {
                $("#GetModLogs").attr("disabled",false);
            }, 3000);
      },
      error: function(err) {
      $('#ModLogStatus').css('color', 'Red');
      $('#ModLogStatus').text("Error: Not Getting Logs...!!")
      }
 });
});

$("#GetModLogsDumpIO").click(function() {

        debugger;
//Ajax call for getting parse image for mod logs
     $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      data:$("#BotLogs").val(),
      url: "/GetModLogsPicture",
      success: function (result) {

//            toastr["success"]("Logs Has Been Generated Successfully.");
            $("#GetModLogs").attr("disabled",true);

//            $('#Mode_Log_Picture').attr("src", result.results["Pic"]);
            $("#Mode_Log_Picture").attr("src", "http://192.168.1.165/report.png");
            $('#ModLogStatus').css('color', 'Green');
            $('#ModLogStatus').text("Success...!!")
            $("ModLogPicHeading").css("display", "");
            var interval = setInterval(function() {
                $("#GetModLogs").attr("disabled",false);
            }, 3000);
      },
      error: function(err) {
      $('#ModLogStatus').css('color', 'Red');
      $('#ModLogStatus').text("Error: Not Getting Logs...!!")
      alert("Error");
      }
 });

//Ajax call for text area mod logs
     $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      data:$("#BotLogs").val(),
      url: "/GetModLogsDumpIO",
      success: function (result) {

            toastr["success"]("Logs Has Been Generated Successfully.");

            $("#GetModLogsDumpIO").attr("disabled",true);

            $('#Text_Area_LogsDumpIO').text(result);
            $('#ModLogStatusDumpIO').css('color', 'Green');

            $('#ModLogStatusDumpIO').text("Sucess...!!")
            var interval = setInterval(function() {
                $("#GetModLogsDumpIO").attr("disabled",false);
            }, 3000);

      },
      error: function(err) {
      $('#ModLogStatusDumpIO').css('color', 'Red');
      $('#ModLogStatusDumpIO').text("Error: Not Getting Logs...!!")
      }
 });
});



var TxtType = function(el, toRotate, period) {
        this.toRotate = toRotate;
        this.el = el;
        this.loopNum = 0;
        this.period = parseInt(period, 10) || 2000;
        this.txt = '';
        this.tick();
        this.isDeleting = false;
    };

    TxtType.prototype.tick = function() {
        var i = this.loopNum % this.toRotate.length;
        var fullTxt = this.toRotate[i];

        if (this.isDeleting) {
        this.txt = fullTxt.substring(0, this.txt.length - 1);
        } else {
        this.txt = fullTxt.substring(0, this.txt.length + 1);
        }

        this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';

        var that = this;
        var delta = 200 - Math.random() * 100;

        if (this.isDeleting) { delta /= 2; }

        if (!this.isDeleting && this.txt === fullTxt) {
        delta = this.period;
        this.isDeleting = true;
        } else if (this.isDeleting && this.txt === '') {
        this.isDeleting = false;
        this.loopNum++;
        delta = 500;
        }

        setTimeout(function() {
        that.tick();
        }, delta);
    };

    window.onload = function() {
        var elements = document.getElementsByClassName('typewrite');
        for (var i=0; i<elements.length; i++) {
            var toRotate = elements[i].getAttribute('data-type');
            var period = elements[i].getAttribute('data-period');
            if (toRotate) {
              new TxtType(elements[i], JSON.parse(toRotate), period);
            }
        }
        // INJECT CSS
        var css = document.createElement("style");
        css.type = "text/css";
        css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #fff}";
        document.body.appendChild(css);
    };