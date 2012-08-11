<!--this should contains in entry.html-->
		<script type="text/javascript" src="/home/wpeng/Ubuntu One/mycode/xwp2/templates/admin/tinymce/tiny_mce.js"></script>
		<script type="text/javascript" src="/home/wpeng/Ubuntu One/mycode/xwp2/templates/admin/tinymce/jquery.tinymce.js"></script>

		<script type="text/javascript">
			$('#content').ready(function() {
				$('.editor-toolbar').show();
				$('#edButtonHTML').click(function(){switchEditors.go('content','html');});
				$('#edButtonPreview').click(function(){switchEditors.go('content','tinymce');});

				$('#content').tinymce({
						// Location of TinyMCE script
						script_url : '/home/wpeng/Ubuntu One/mycode/xwp2/templates/admin/tinymce/tiny_mce.js',
						// General options
						theme : "advanced",

						//plugins : "pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",
						plugins : "safari,pagebreak,save,advhr,advimage,advlink,emotions, inlinepopups,media,directionality,visualchars,nonbreaking,emotions,fullscreen,preview,wordpress,syntaxhl",

						// Theme options
						theme_advanced_buttons1:"bold,italic,strikethrough,|,bullist,numlist,blockquote,|,forecolor,backcolor,|,justifyleft,justifycenter,justifyright,|,link,unlink,image,wp_more,code,preview,|,fullscreen,syntaxhl,wp_adv",
						theme_advanced_buttons2:"styleselect,formatselect,fontselect,fontsizeselect,underline,justifyfull,forecolor,|,pastetext,pasteword,removeformat,|,media,charmap,emotions,|,outdent,indent,|,undo,redo",
						theme_advanced_buttons3:"",
						theme_advanced_buttons4:"",

						theme_advanced_toolbar_location : "top",
						theme_advanced_toolbar_align : "left",
						theme_advanced_statusbar_location : "bottom",
						theme_advanced_resizing : true,
						language : "ch",
						skin :"wp_theme_zh",
						//language : "{{ blog.language|slice:":2" }}",
						skin :'wp_theme',
						// Example content CSS (should be your site CSS)
						content_css : "/home/wpeng/Ubuntu One/mycode/xwp2/templates/admin/tinymce/wordpress.css",
						extended_valid_elements : "textarea[cols|rows|disabled|name|readonly|class]",

						// Drop lists for link/image/media/template dialogs
						//template_external_list_url : "lists/template_list.js",
						//external_link_list_url : "lists/link_list.js",
						//external_image_list_url : "/static/js/image_list.js",
						//media_external_list_url : "/static/js/image_list.js",
						file_browser_callback: 'micolog_file',
						relative_urls: false
				});
			});

			function micolog_file(field_name, url, type, win){
				if (type=='image')
				{
					ext='jpg|png|jpeg|gif';
				}
				else if (type=='mdeia')
				{
					ext='swf|wmv|avi|wma|mp3|mid|asf|rm|rmvb|flv';
				}
				else
				{
					ext="*";
				}

			tinyMCE.activeEditor.windowManager.open({
				file : '/admin/uploadex?ext='+ext,  //上传窗口的路径
				title : '{%trans "Files"%}',
				width : 420,
				height : 200,
				resizable : "no",
				inline : "yes",
				popup_css: false,
				close_previous : "no"
			}, {
				window : win,  //告诉它是被谁弹出来的
				input : field_name  //这个是指生成的图片地址要往哪里填
			});
			return false;
		  }
		</script>


