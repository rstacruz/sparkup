// Usage:
// $($.hashJumpStart);
// $('.whatever').jump();
// $('.whatever').jump('#lol'); // To do jump-highlight
// $.hashJump('#test');

;(function($)
{
    $.hashJumpStart = function()
    {
		$('a[href]').click(function()
		{
			return !($.hashJump($(this).attr('href')));
		});
		if (window.location.hash)
		    { $.hashJump(window.location.hash); }
		return $;
    };
    
	$.hashJump = function(href)
	{
        matches = /^(.*)#/.exec(href);
		url = (matches) ? (matches[1]) : '';
	
		// Rudimentary check to see if we're the URL in question
		if (String(window.location).indexOf(url) == -1) { return; }
	
		matches = /#(.*)$/.exec(href);
		if (!matches) { return false; }

        jumpname = matches[1];
		target = $('a[name='+jumpname+']');
		if (!target) { return false; }
    
        // Do it!
        $(target).jump(jumpname);
		return true;
	};
	
	$.fn.jump = function(jumpname)
	{
	    // Remove jump highlights
        $('.jump-highlight').removeClass('jump-highlight');
        
	    if (this.count == 0) { return this; }
	    offset = this.offset().top - 10;
	    
	    // Do a highlight if asked for
	    if (jumpname) {
            id = '.'+jumpname.split('.').join('-');
    	    $(id).addClass('jump-highlight');
        }
        
        // Jump
		$('html, body').animate
		(
		    { scrollTop: offset },
		    $.hashJump.options.speed,
		    function() { if (jumpname)
		    {
    		    if ($.hashJump.options.highlight_time > 0) {
    		        window.setTimeout(function()
    		            { $(id).removeClass('jump-highlight'); }, $.hashJump.options.highlight_time);
    		    }
		    }}
	    );
	    
	    // Done!
	    return this;
    };

    $.hashJump.options =
    {
        highlight_time: 0,
        speed: 'medium'
    };
})(jQuery);


$($.hashJumpStart);