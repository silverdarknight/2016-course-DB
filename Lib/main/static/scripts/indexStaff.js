function initUserScan(userName,Page){
	$('#startPage').val(Page);
	var userHtml = '',pageHtml = '';
	var username = userName;
	var offset = $('#offset').val(),startPage = Page;
	$.get('/staffViewUser',
		{'username':username,
		'offset':offset,
		'startPage':startPage},
		function(data) {
		//console.log(data);
		for(var i=0;i<data.userList.length;i++){
			userItem = data.userList[i];
			//console.log(userItem.userid);
			userHtml += '<a href="/staffViewUserDetail/?userid='+userItem.userid+'" class="userItem">'+
						'<div><span>'+userItem.userid+'</span>&nbsp;&nbsp;&nbsp;<span>'+userItem.username+'</span></div>'
						+'<div><span>'+userItem.userage+'</span></div>'
						+'</a>';
		}
		$('.templateUserContainer').html(userHtml);

		if(startPage!=1){pageHtml = '<button class="prev pageBtn"><<</button>';}
		for(var i=0;i<data.pageList.length;i++){
			pageItem = data.pageList[i];
			//console.log(pageItem);
			if(pageItem == data.currentPage) pageHtml += '<button class="active pageBtn">'+pageItem+'</button>';
			else pageHtml += '<button class="pageBtn">'+pageItem+'</button>';
		}
		if(startPage != data.pageList[data.pageList.length-1]) pageHtml += '<button class="next pageBtn">>></button>';
		$('.pageList').html(pageHtml);
		$('.pageBtn').click(function(event) {
			//var targetPage = $(this).text();
			//startPage = $('#startPage').val(targetPage);
			if($(this).hasClass('next')){
				targetPage = parseInt($('#startPage').val())+1;
			}
			else if($(this).hasClass('prev')){
				targetPage = parseInt($('#startPage').val())-1;
			}
			else{
				targetPage = $(this).text();
			}
			initUserScan($('#changeUserName').val(),targetPage);
		});
	});
}
initUserScan('',1);
$(document).ready(function(){
	var typeOptions = [];
	$.get('/getTypeOptions', function(data) {
		typeOptions = data;
		//console.log(typeOptions);
	});
	$('.changeUserBtnCheck').click(function(event) {
		initUserScan($('#changeUserName').val(),1);
	});
	$('.returnBtnCheck').click(function(event) {
		var bookid=$('#returnBookid').val();
		var userid=$('#returnUserid').val();
		$.get('/staffReturnUserBook',{"bookid":bookid,"userid":userid},function(data) {
			$('.returnBookMsg').removeClass('success').removeClass('fail').text("");
			bookid=$('#returnBookid').val("");
			userid=$('#returnUserid').val("");
			if(data.end){
				$('.returnBookMsg').addClass('success').text("还书成功！");
			}
			else{
				$('.returnBookMsg').addClass('fail').text("还书失败！请重新操作");
			}
		});
	});
	$('.borrowBtnCheck').click(function(event) {
		var bookid=$('#borrowBookid').val();
		var userid=$('#borrowUserid').val();
		console.log(bookid+userid);
		$.get('/staffBorrowUserBook',{"bookid":bookid,"userid":userid},function(data) {
			$('.borrowBookMsg').removeClass('success').removeClass('fail').text("");
			$('#borrowBookid').val("");
			$('#borrowUserid').val("");
			if(data.end){
				$('.borrowBookMsg').addClass('success').text("借书成功！");
			}
			else{
				$('.borrowBookMsg').addClass('fail').text("借书失败！请重新操作");
			}
		});
	});
	$('.createBtnCheck').click(function(event){
		var bookid = $('#createBookId').val();
		var bookname = $('#createBookName').val();
		var booktype = $('#createBookType').val();
		var bookpub = $('#createBookPub').val();
		var bookauthor = $('#createBookAuthor').val();
		var bookintro = $('#createBookIntro').val();
		var bookprice = $('#createBookPrice').val();
		var booknum = $('#createBookNum').val();
		$.get('/staffCreateBook',
			{"bookid":bookid,
			"bookname":bookname,
			"booktype":booktype,
			"bookpublisher":bookpub,
			"bookauthor":bookauthor,
			"bookintroduction":bookintro,
			"bookprice":bookprice,
			"booknum":booknum},function(data) {
			console.log(data);
		});
	});
	$('.addBtnCheck').click(function(event) {
		var bookid = $('#addBookId').val();
		var addnum = $('#addBookNum').val();
		$.get('/staffAddBookNum',{"bookid":bookid,"addBookNum":addnum},function(data) {
			console.log(data);
		});
	});
	$('.changeBookBtnCheck').click(function(event) {
		var template ='';
		var bookid = $('#changeBookId').val();
		$.get('/viewBook',{"mode":"Detail","startPage":0,"offset":10,"bookLikeName":bookid},function(data) {
			optionTemplate = '';
			for(var i=0;i<typeOptions.length;i++){
				option = typeOptions[i];
				console.log(option);
				if(option.optionName == data.bookType){
					optionTemplate+='<option value="'+option.num+'" selected="true">'+option.optionName+'</option>'
				}
				else optionTemplate+='<option value="'+option.num+'">'+option.optionName+'</option>'
			}
			console.log(data);
			template+=  '<input class="changeBookId" value="'+data.bookId+'" type="hidden"/>'+
						'<div class="line">'+
							'<span>图书名称：</span><input type="text" class="changeBookName" value="'+data.bookName+'"/>'+
						'</div>'+
						'<div class="line">'+
							'<span>图书类型：</span>'+
							'<select class="changeBookType">'+
							optionTemplate+
							'</select>'+
						'</div>'+
						'<div class="line">'+
							'<span>作者：</span><input type="text" class="changeBookAuthor" value="'+data.bookAuthor+'"/>'+
						'</div>'+
						'<div class="line">'+
							'<span>出版社：</span><input type="text" class="changeBookPublisher" value="'+data.bookPublisher+'"/>'+
						'</div>'+
						'<div class="line">'+
							'<span>简介：</span><input type="text" class="changeBookIntro" value="'+data.bookIntroduction+'"/>'+
						'</div>'+
						'<div class="line">'+
							'<span>价格：</span><input type="text" class="changeBookPrice" value="'+data.bookPrice+'"/>'+
						'</div>'+
						'<div class="line">'+
							'<span>库存：</span><input type="text" class="changeBookNum" value="'+data.bookNum+'"/>'+
						'</div>';
			$('.templateBookContainer').html(template);
			$('.changeBookBtnSubmit').removeClass('hid');
		});
	});
	$('.changeBookBtnSubmit').click(function(event) {
		var bookid = $('.changeBookId').val();
		var bookname = $('.changeBookName').val();
		var booktype = $('.changeBookType').val();
		var bookauthor = $('.changeBookAuthor').val();
		var bookpublisher = $('.changeBookPublisher').val();
		var bookintro = $('.changeBookIntro').val();
		var bookprice = $('.changeBookPrice').val();
		var booknum = $('.changeBookNum').val();
		$.get('/staffChangeBookInfo',
			{"bookid":bookid,
			"bookname":bookname,
			"booktype":booktype,
			"bookauthor":bookauthor,
			"bookpublisher":bookpublisher,
			"bookintroduction":bookintro,
			"bookprice":bookprice,
			"booknum":booknum},
			function(data) {
			console.log(data);
		});
	});
});
	