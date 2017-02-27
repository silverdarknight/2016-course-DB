$('.book').hover(function() {
	/* Stuff to do when the mouse enters the element */
	$(this).find(".hover").removeClass('hid');
}, function() {
	/* Stuff to do when the mouse leaves the element */
	$(this).find(".hover").addClass('hid');
});
$(".bookMain").click(function(event) {
	var textDom = $(this).parent().next();
	var hoverDom = $(this).parent().find(".hover");
	hoverDom.addClass('chosen');
	$(this).parent().siblings().find(".hover").removeClass('chosen').parent().next().html("");
	bookid = $(this).find(".id").val();
	$.get('/viewBook/',{"bookLikeName":bookid,"mode":"Detail","startPage":1,"offset":10},function(data) {
		html = '<div class="bookDetail"><span>编号:</span><span class="bookDetailId">'+data.bookId+'</span><br /><span>书名:</span><span class="bookDetailName">'+data.bookName+'</span><br /><span>类型:</span><span class="bookDetailType">'+data.bookType+'</span><br /><span>作者:</span><span class="bookDetailAuthor">'+data.bookAuthor+'</span><br /><span>出版社:</span><span class="bookDetailPublisher">'+data.bookPublisher+'</span><br /><span>简介:</span><span class="bookDetailIntro">'+data.bookIntroduction+'</span><br /><span>价格:</span><span class="bookDetailPrice">'+data.bookPrice+'$</span><br /><span>库存:</span><span class="bookDetailNum">'+data.bookNum+'</span><br />'
		if(data.bookNum == "0") html += '<span>状态:</span><span class="bookDetailCanBorrow fail">不可借阅</span><br /></div>';
		else html += '<span>状态:</span><span class="bookDetailCanBorrow success">可借阅</span><br /></div>';
		textDom.html(html);
	});
});