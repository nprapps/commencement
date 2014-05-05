var $speeches = null;
var $adviceFilter = {};
var $search = null;
var $body = null;

var searchIndex = null;

var filterSpeeches = function() {
    $speeches.hide();

    var $visibleSpeeches = $speeches;
    var query = $search.val();
    var advice = $adviceFilter.val();

    if (query) {
        var results = searchIndex.search(query);
        var slugs = _.pluck(results, 'ref');
        var ids = _.map(slugs, function(s) { return '#' + s });

        $visibleSpeeches = $(ids.join(','));
    }

    if (advice) {
        $visibleSpeeches = $visibleSpeeches.filter('.advice-' + advice)
    }

    $visibleSpeeches.show();
}

$(function() {
    $speeches = $('.speeches li');
    $adviceFilter = $('#advice-filter');
    $search = $('#search');
    $body = $('body');

    if ($body.hasClass('homepage')){
        searchIndex = lunr(function () {
            this.field('name', {boost: 10})
            this.field('mood')
            this.field('school')
            this.field('year')
            this.ref('slug')
        })

        _.each(SPEECHES, function(speech) {
            searchIndex.add(speech);
        });

        $adviceFilter.on('change', filterSpeeches);
        $search.on('keyup', filterSpeeches);
    }
});
