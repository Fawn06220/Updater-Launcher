jQuery(function( $ ){
			
			var $newsTicker = $('#news-ticker');
			$newsTicker.serialScroll({
				items:'div',
				next: $newsTicker,//odd huh, the container itself will get bound
				duration:700,
				force:true,
				axis:'y',
				lazy:true,//NOTE: it's set to true, meaning you can/remove/reorder the items and the changes are taken into account.
				step:1, //scroll 2 news each time
				start:0, 
				event:'showNext' //just a random event name
			});
			setInterval(function(){//scroll each 5 seconds
				$newsTicker.trigger('showNext');
			}, 4500 );
						
		});