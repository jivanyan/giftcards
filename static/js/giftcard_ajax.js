$(document).ready(function() {
	
	$('#searchbox').live('click',function(){
		$(this).value = "";
	})
	$('#searchbox').keyup(function(){
        	var q;
        	q = $(this).val();
        	$.get('/giftcards/search/', {query: q}, function(data){
        	$('#gift_card_plans').html(data);
        	});
	});        

});

