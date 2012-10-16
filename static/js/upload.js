var xhr = new XMLHttpRequest();
/*var FileBrowserDialogue = {
	init : function () {
		   // Here goes your code for setting your custom things onLoad.
	},
	mySubmit : function (e) {
	   var win = tinyMCEPopup.getWindowArg("window");

	   // insert information now
	   win.document.getElementById(tinyMCEPopup.getWindowArg("input")).value = e;

	   // are we an image browser
	   if (typeof(win.ImageDialog) != "undefined")
	   {
		   // we are, so update image dimensions and preview if necessary
		   if (win.ImageDialog.getImageData) win.ImageDialog.getImageData();
		   if (win.ImageDialog.showPreviewImage) win.ImageDialog.showPreviewImage(URL);
	   }

	   // close popup window
	   tinyMCEPopup.close();
   }
}*/

function callback(e)
{
	var win = tinyMCEPopup.getWindowArg("window");  
	win.document.getElementById(tinyMCEPopup.getWindowArg("input")).value = e;

	tinyMCEPopup.close();
}

function update_file_selected() 
{
	if(window.File && window.FileList)
	{
		var file = document.getElementById("fileToUpload").files[0];

		document.getElementById("fileName").innerHTML = "file name: " + file.name; 
		document.getElementById("fileSize").innerHTML = "file size: " + file.size; 
		document.getElementById("progressNumber").innerHTML= ""; 
	}
}

function upload_file()
{	
	var form = new FormData();
	var file = document.getElementById("fileToUpload").files[0];
	form.append("FileData", file);
	form.append("FileName", file.name);
	form.append("FileSize", file.size);

	xhr.addEventListener("progress", upload_progress, false);
	xhr.addEventListener("load", upload_complete, false);
	xhr.addEventListener("error", upload_failed, false);
	xhr.addEventListener("abort", upload_canceled, false);

	//tinyMCEPopup.onInit.add(FileBrowserDialogue.init, FileBrowserDialogue);
	xhr.open("POST", "/admin/upload");
	xhr.send(form);

	document.getElementById("btnUpload").disabled = true;
	document.getElementById("progressNumber").innerHTML = "uploading...";

}

function upload_complete(evt)
{
	if((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304)
	{
		var r = JSON.parse(xhr.responseText);	
		document.getElementById("progressNumber").innerHTML = "upload status: success";
		document.getElementById("btnUpload").disabled = false;

		callback(r.url);
		
		//FileBrowserDialogue.mySubmit(r.url);
	}
	else
	{
		upload_failed(evt);
	}
}

function upload_progress(evt)
{
	if(evt.lengthComputable) 
	{
		var per = Math.round(evt.loaded * 100 / evt.total);
		document.getElementById("progressNumber").innerHTML = "update status: " + per.toString() + "%";
	}
}

function upload_failed(evt)
{
	document.getElementById("progressNumber").innerHTML = "update status: failed.";
	document.getElementById("btnUpload").disabled = false;
}

function upload_canceled(evt)
{
	document.getElementById("progressNumber").innerHTML = "update status: failed.";
	document.getElementById("btnUpload").disabled = false;
}

