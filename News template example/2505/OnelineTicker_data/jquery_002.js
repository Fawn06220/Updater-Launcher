/**
 * jQuery.serialScroll
 * Copyright (c) 2008 Ariel Flesler - aflesler(at)gmail(dot)com
 * Licensed under GPL license (http://www.opensource.org/licenses/gpl-license.php).
 * Date: 2/18/2008
 *
 * @projectDescription Animated scrolling of series.
 * @author Ariel Flesler
 * @version 1.0.1
 *
 * @id jQuery.serialScroll
 * @id jQuery.fn.serialScroll
 * @param {Object} settings Hash of settings, it is passed in to jQuery.ScrollTo, none is required.
 * @return {jQuery} Returns the same jQuery object, for chaining.
 *
 * Notes:
 *	- The plugin requires jQuery.ScrollTo.
 *	- The hash of settings, is passed to jQuery.ScrollTo, so its settings can be used as well.
 **/
;(function( $ ){

	var $serialScroll = $.serialScroll = function( settings ){
		$.scrollTo.window().serialScroll( settings );
	};

	//Many of these defaults, belong to jQuery.ScrollTo, check it's demo for an example of each option.
	//@see http://www.freewebs.com/flesler/jQuery.ScrollTo/
	$serialScroll.defaults = {//the defaults are public and can be overriden.
		duration:1000, //how long to animate.
		axis:'x', //which of top and left should be scrolled
		event:'click', //on which event to react.
		start:0, //first element (zero-based index)
		step:1, //how many elements to scroll on each action
		lock:true,//ignore events if already animating
		cycle:true //cycle endlessly ( constant velocity )
		/*
		lazy:false,//go find the elements each time (allows AJAX or JS content, or reordering)
		stop:false, //stop any previous animations to avoid queueing
		force:false,//force the scroll to the first element on start ?
		jump: false,//if true, when the event is triggered on an element, the pane scrolls to it
		items:null, //selector to the items (relative to the matched elements)
		prev:null, //selector to the 'prev' button
		next:null, //selector to the 'next' button
		*/		
	};

	$.fn.serialScroll = function( settings ){
		settings = $.extend( {}, $serialScroll.defaults, settings );
		var event = settings.event, //this one is just to get shorter code when compressed
			step = settings.step, // idem
			duration = settings.duration / step; //save it, we'll need it

		return this.each(function(){
			var 
				$pane = $(this),
				items = settings.lazy ? settings.items : $( settings.items, $pane ),
				actual = settings.start;

			if( settings.force )
				jump({ data: actual });

			$(settings.prev||[]).bind( event, -step, move );
			$(settings.next||[]).bind( event, step, move );

			if( !settings.lazy && settings.jump )
				items.bind( event, function( e ){
					e.data = items.index(this);
					jump( e, this );
				});

			function move( e ){
				e.data += actual;
				jump( e, this );
			};			
			function jump( e, button ){
				var 
					pos = e.data,
					$items = $(items,$pane),
					limit = $items.length;

				if( button )
					e.preventDefault();

				pos %= limit; //keep it under the limit
				if( pos < 0 )
					pos += limit;

				var elem = $items[pos];
				if( settings.lock && $pane.is(':animated') || //no animations while busy
					!settings.cycle && !$items[e.data] || //no cycling
					button && settings.onBefore && //callback returns false
				 	settings.onBefore.call(button, e, elem, $pane) === false ) return;

				if( settings.stop )
					$pane.queue('fx',[]).stop();//remove all its animations

				var 
					duration = duration*(4/5)

				settings.duration = duration * Math.abs( actual - pos );//keep constant velocity
				$pane.scrollTo( elem, settings );
				actual = pos;
			};
		});
	};

})( jQuery );