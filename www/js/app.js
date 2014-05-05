var $speeches = null;
var $adviceFilter = {};

var filterSpeeches = function() {
    /*
     * Only show speeches whose slugs are `visibleSlugs`.
     */
    $speeches.hide();

    var advice = $adviceFilter.val();

    var selector = '';

    if (advice) {
        selector += ('.advice-' + advice);
    }

    if (!selector) {
        $speeches.show();
    } else {
        $speeches.filter(selector).show();
    }
}

$(function() {
    $speeches = $('.speeches li');
    $adviceFilter = $('#advice-filter');

    $adviceFilter.on('change', filterSpeeches);
});
