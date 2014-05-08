var $speeches = null;
var $tags = null;
var $tagButtons = null;
var $resetTagsButton = null;
var $search = null;
var $body = null;
var $leadQuote = null;
var $refreshQuoteButton = null;

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
}

var newSpeech = function(key, value) {
    var speech = null;

    return {
        getSpeech: function(){
            this.setSpeech();

            return speech;
        },
        setSpeech: function(key, value) {
            speech = _.chain(SPEECHES)
                      .shuffle()
                      .filter(function(pair){
                          return pair[key] == value;
                      })
                      .reject(function(pair){
                          return speech !== null ? pair['slug'] == speech['slug'] : false;
                      })
                      .value()[0];
        }
    };
}

var renderLeadQuote = function(quote) {
    var context = typeof(quote['data']) !== 'undefined' ? quote['data'].getSpeech() : quote.getSpeech();
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
}

var onResetTagsButtonClick = function() {
    $tagButtons.removeClass('active');
    $(this).hide();

    filterSpeeches();
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
        searchIndex = lunr(function () {
            this.field('name', {boost: 10})
            this.field('mood')
            this.field('school')
            this.field('year')
            this.ref('slug')
        })
        var quote = newSpeech();

        renderLeadQuote(quote);

        _.each(SPEECHES, function(speech) {
            searchIndex.add(speech);
        });

        $tagButtons.on('click', onTagButtonClick);
        $resetTagsButton.on('click', onResetTagsButtonClick);
        $search.on('keyup', filterSpeeches);
        $refreshQuoteButton.on('click', quote, renderLeadQuote);
    }
});
