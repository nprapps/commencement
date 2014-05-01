var $speeches = null;
var $decadeFilter = null;
var $tagFilter = null;

var filterSpeeches = function() {
    /*
     * Only show speeches whose slugs are `visibleSlugs`.
     */
    $speeches.hide();

    var decade = $decadeFilter.val();
    var tag = $tagFilter.val();

    var selector = '';

    if (decade) {
        selector += ('.decade-' + decade); 
    }

    if (tag) {
        selector += ('.tag-' + tag);
    }

    if (!selector) {
        $speeches.show();
    } else {
        $speeches.filter(selector).show();
    }
}

$(function() {
    $speeches = $('.speeches li');
    $decadeFilter = $('#decade-filter');
    $tagFilter = $('#tag-filter');

    $decadeFilter.on('change', filterSpeeches);
    $tagFilter.on('change', filterSpeeches);
});
