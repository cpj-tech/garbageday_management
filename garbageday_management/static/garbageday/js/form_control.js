
// 初期描画時
function intial_form() {
	$('#id_week2 option[value="0"]').wrap('<span class="everyweek-hide">');

	// 週１のテキスト情報を取得
	var obj_week1 = document.getElementById("id_week1");
	var index_week1 = obj_week1.selectedIndex;
	var txt_week1 = obj_week1.options[index_week1].text;

	// 週２のテキスト情報を取得
	var obj_week2 = document.getElementById("id_week2");
	var index_week2 = obj_week2.selectedIndex;
	var txt_week2 = obj_week2.options[index_week2].text;

	// 週２が未入力の場合, 非活性
	if (txt_week2 == '---------') {
		obj_week2.setAttribute("disabled", true);
		obj_week2.style.color = "White";	
	}

	// 曜日２のテキスト情報を取得
	var obj_dow2 = document.getElementById("id_day_of_week2");
	var index_dow2 = obj_dow2.selectedIndex;
	var txt_dow2 = obj_dow2.options[index_dow2].text;

	// 曜日１の情報取得
	var obj_dow1 = document.getElementById("id_day_of_week1");
	var index_dow1 = obj_dow1.selectedIndex;

	// 曜日２が未入力の場合, 非活性
	if (txt_dow2 == '---------') {
		obj_dow2.setAttribute("disabled", true);
		obj_dow2.style.color = "White";	
	}

	if (txt_dow2 == '---------' && txt_week1 == '毎週') {
		obj_dow2.removeAttribute("disabled");
		obj_dow2.style.color = "black";
		makeDowTwoOptions(index_dow1);
	}

	// アラームの有無をチェック
	var is_alarm = document.getElementById("id_manage_alarm");
	if(is_alarm.checked) {
		activeAlarm();
	} else {
		inactiveAlarm();
	}

}

// アラーム有無の変更時イベント
function onChangeAlarmBox(event) {
	if(this.checked) {
		activeAlarm();
	} else {
		inactiveAlarm();
	}
}

// アラーム有の時
function activeAlarm() {
	document.getElementById("id_alarm_day").removeAttribute("disabled");
	document.getElementById("id_alarm_day").style.color = "black";
	document.getElementById("id_alarm_time").removeAttribute("disabled");
	document.getElementById("id_alarm_time").style.color = "black";
}

// アラーム無の時
function inactiveAlarm() {
	document.getElementById("id_alarm_day").setAttribute("disabled", true);
	document.getElementById("id_alarm_day").style.color = "White";
	document.getElementById("id_alarm_time").setAttribute("disabled", true);
	document.getElementById("id_alarm_time").style.color = "White";
}

// 週１のプルダウン変更時、イベント
function onChangeWeek1() {
	// 週１のテキスト情報を取得
	var index_week1 = this.selectedIndex;
	var txt_week1 = this.options[index_week1].text;
	// 週２の情報取得
	var obj_week2 = document.getElementById("id_week2");

	// 曜日１の情報取得
	var obj_dow1 = document.getElementById("id_day_of_week1");
	var index_dow1 = obj_dow1.selectedIndex;
	var txt_dow1 = obj_dow1.options[index_dow1].text;

	// 曜日２の情報取得
	var obj_dow2 = document.getElementById("id_day_of_week2");

	if (txt_week1 == '---------' ) {
		var week2_option = obj_week2.getElementsByTagName('option');
		week2_option[0].selected = true;
		var dow1_option = obj_dow1.getElementsByTagName('option');
		dow1_option[0].selected = true;
		var dow2_option = obj_dow2.getElementsByTagName('option');
		dow2_option[0].selected = true;
		obj_week2.setAttribute("disabled", true);
		obj_week2.style.color = "White";
		obj_dow2.setAttribute("disabled", true);
		obj_dow2.style.color = "White";
	} else if (txt_week1 == '毎週' ) {
		var week_pulldown_option = obj_week2.getElementsByTagName('option');
		week_pulldown_option[1].selected = true;
		obj_week2.setAttribute("disabled", true);
		obj_week2.style.color = "White";
		if (txt_dow1 != '---------') {
			obj_dow2.removeAttribute("disabled");
			obj_dow2.style.color = "black";
			makeDowTwoOptions(index_dow1);
		}
	} else {
		var dow2_option = obj_dow2.getElementsByTagName('option');
		dow2_option[0].selected = true;
		obj_week2.removeAttribute("disabled");
		obj_week2.style.color = "black";
		obj_dow2.setAttribute("disabled", true);
		obj_dow2.style.color = "White";
		makeWeekTwoOptions(index_week1);
	}
}

// 新しく週２のプルダウンを作成
function makeWeekTwoOptions(index_week1) {	
	var week1_options = document.getElementById("id_week1").getElementsByTagName('option');
	var select = document.getElementById("id_week2");

	for (var i=0;  week1_options.length-1 > i; i++) {
		select.remove(0)
	}
	for (week1_option of week1_options) {
		new_option = document.createElement("option");
		if (week1_option.innerText != '毎週') {
			new_option.text = week1_option.innerText;
			new_option.value = week1_option.index;
			new_option.value
			select.appendChild(new_option);	
		}
	}
	select.remove(index_week1-1)
}

// 曜日１変更時、イベント
function onChangeDow1() {
	// 週１のテキスト情報を取得
	var obj_week1 = document.getElementById("id_week1");
	var index_week1 = obj_week1.selectedIndex;
	var txt_week1 = obj_week1.options[index_week1].text;

	if (txt_week1 == '毎週') {
		var index_dow1 = this.selectedIndex;
		var txt_dow1 = this.options[index_dow1].text;
		var obj_dow2 = document.getElementById("id_day_of_week2");
	
		if (txt_dow1 == '---------') {
			var dow2_option = obj_dow2.getElementsByTagName('option');
			dow2_option[0].selected = true;
			obj_dow2.setAttribute("disabled", true);
			obj_dow2.style.color = "White";
		} else {
			obj_dow2.removeAttribute("disabled");
			obj_dow2.style.color = "black";	
			makeDowTwoOptions(index_dow1);
		}
	}
}

// 新しく曜日2のプルダウンを作成
function makeDowTwoOptions(index_dow1) {

	var dow1_options = document.getElementById("id_day_of_week1").getElementsByTagName('option');
	var select = document.getElementById("id_day_of_week2");
	
		
	for (var i=0;  dow1_options.length > i; i++) {
		select.remove(0)
	}
	for (dow1_option of dow1_options) {
		new_option = document.createElement("option");
		new_option.text = dow1_option.innerText;
		new_option.value = dow1_option.index;
		select.appendChild(new_option);	
	}
	console.log(index_dow1)
	select.remove(index_dow1)
}


intial_form();

// イベントの追加
var is_alarm = document.getElementById("id_manage_alarm");
is_alarm.addEventListener('change', onChangeAlarmBox);

var is_week1 = document.getElementById('id_week1');
is_week1.addEventListener('change', onChangeWeek1);

var is_dow1 = document.getElementById('id_day_of_week1');
is_dow1.addEventListener('change', onChangeDow1);


