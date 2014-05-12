var $speeches = null;
var $tags = null;
var $tagButtons = null;
var $resetTagsButton = null;
var $search = null;
var $body = null;
var $leadQuote = null;
var $refreshQuoteButton = null;
var $noResults = null;

var searchIndex = null;

var filterSpeeches = function() {
    $speeches.hide();

    var $visibleSpeeches = $speeches;
    var query = $search.val();
    var tags = $tags.find('.active').first().data('tag');

    if (query) {
        var results = searchIndex.search(query);
        var slugs = _.pluck(results, 'ref');
        var ids = _.map(slugs, function(s) { return '#' + s });

        $visibleSpeeches = $(ids.join(','));
    }

    if (tags) {
        $visibleSpeeches = $visibleSpeeches.filter('.tag-' + tags)
    }

    $visibleSpeeches.show();

    if ($visibleSpeeches.length > 0){
        $noResults.hide();
    } else {
        $noResults.show();
    }
}

var renderLeadQuote = function() {
    var featured = _.where(SPEECHES, {'featured': 'y'});
    var context = _.shuffle(featured)[0];
    var html = JST.quote(context);

    $leadQuote.html(html);

    _.defer(function(){
        $leadQuote.find('blockquote').addClass('fadein');
    });
}

var onTagButtonClick = function() {
    var $this = $(this);

    $tagButtons.not($this).removeClass('active');
    $this.toggleClass('active');

    if ($this.hasClass('active')){
        $resetTagsButton.show();
    } else {
        $resetTagsButton.hide();
    }

    filterSpeeches();
    $.scrollTo('.tags', { duration: 250, offset: { top: -10, left:0 } });
}

var onResetTagsButtonClick = function() {
    $tagButtons.removeClass('active');
    $(this).hide();

    filterSpeeches();
    $.scrollTo('.tags', { duration: 250, offset: { top: -10, left:0 } });
}

var onRefreshQuoteButtonClick = function() {
    renderLeadQuote();
    $.scrollTo('.big-quote', { duration: 250 });
}

$(function() {
    $speeches = $('.speeches li');
    $tags = $('.tags');
    $tagButtons = $('.tags .btn').not('.reset-tags');
    $resetTagsButton = $('.reset-tags');
    $search = $('#search');
    $body = $('body');
    $refreshQuoteButton = $('#refresh-quote');

    if ($body.hasClass('homepage')){
        $leadQuote = $('#lead-quote');
        $noResults = $('#no-results');
        searchIndex = lunr(function () {
            this.field('name', {boost: 10})
            this.field('mood')
            this.field('school')
            this.field('year')
            this.ref('slug')
        })

        renderLeadQuote();

        _.each(SPEECHES, function(speech) {
            searchIndex.add(speech);
        });

        $tagButtons.on('click', onTagButtonClick);
        $resetTagsButton.on('click', onResetTagsButtonClick);
        $search.on('keyup', filterSpeeches);
        $refreshQuoteButton.on('click', onRefreshQuoteButtonClick);
    }
});
