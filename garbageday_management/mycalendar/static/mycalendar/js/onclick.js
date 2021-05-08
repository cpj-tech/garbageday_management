
$('#clickTarget').on("click", function (event) {
    //クリック時のイベントを記述
    document.getElementById("clickDay").innerHTML = "";
    document.getElementById("clickType").innerHTML = "";
    document.getElementById("clickTime").innerHTML = "";
  
    var year_month = document.getElementById("year_month").value;
    var targetChildren = event.target.childNodes;
    var day = targetChildren[0].textContent;
    var clickday = year_month + '/' + day;
    
    // --- 結果表示 ------------------------------
    if( event.target.className == "all" || event.target.className == "table-success" ){
      document.getElementById("clickDay").innerHTML = clickday;
      if (targetChildren.length > 3) {
        var type = event.target.childNodes[3].textContent;
        document.getElementById("clickType").innerHTML = type;  
      }
      for (var i = 0; i < targetChildren.length; i++ ) {
        if (targetChildren[i].id != undefined) {
          if (targetChildren[i].id == 'id_alarmtime') {
            var alarm_time = targetChildren[i].innerHTML;
            document.getElementById("clickTime").innerHTML = alarm_time;
          } 
        }
      }
    } else {
      document.getElementById("noData").innerHTML = ''
    }
  });
  