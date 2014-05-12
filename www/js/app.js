var $speeches = null;
var $tags = null;
var $tagButtons = null;
var $resetTagsButton = null;
var $search = null;
var $body = null;
var $leadQuote = null;
var $refreshQuoteButton = null;
var $noResults = null;
var $speechCount = null;
var $speechTotal = null;

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
        $speechCount.html($visibleSpeeches.length - 1);
        $speechTotal.html(SPEECHES.length);
        $speechCount.parent('p').show();
    } else {
        $noResults.show();
        $speechCount.html(SPEECHES.length);
        $speechTotal.html(SPEECHES.length);
        $speechCount.parent('p').show();
    }
}

var renderLeadQuote = function() {
    var featured = _.where(SPEECHES, {'featured': 'y'});
    var context = _.shuffle(featured)[0];
    var html = JST.quote(context);

    $leadQuote.html(html);

    _.defer(function(){
        $leadQuote.find('blockquote').addClass('fadein');
        $leadQuote.find('.mug').addClass('fadein');
    });
}

var onTagButtonClick = function() {
    hasher.setHash($(this).data('tag'));
}

var onResetTagsButtonClick = function() {
    hasher.setHash('_');
}

var onRefreshQuoteButtonClick = function() {
    renderLeadQuote();
    $.scrollTo('.big-quote', { duration: 350 });
}

jQuery.fn.animateAuto = function(prop, speed, callback){
    var elem, height, width;
    return this.each(function(i, el){
        el = jQuery(el), elem = el.clone().css({"height":"auto","width":"auto"}).appendTo("body");
        height = elem.css("height"),
        width = elem.css("width"),
        elem.remove();

        if(prop === "height")
            el.animate({"height":height}, speed, callback);
        else if(prop === "width")
            el.animate({"width":width}, speed, callback);
        else if(prop === "both")
            el.animate({"width":width,"height":height}, speed, callback);
    });
}

var onHashChanged = function(new_hash, old_hash) {
    if (new_hash === '_') { new_hash = ''; }

    if (new_hash === '') {
        $tagButtons.removeClass('active');
        $('a.reset-tags').hide();
    } else {
        var $this = $('div.tags li a[data-tag="' + new_hash + '"]');
        $tagButtons.not($this).removeClass('active');
        $this.toggleClass('active');

        if ($this.hasClass('active')){
            $resetTagsButton.show();
        } else {
            $resetTagsButton.hide();
        }
        $.scrollTo('.tags', { duration: 350, offset: { top: -10, left:0 } });
    }

    filterSpeeches();
};

$(function() {
    $speeches = $('.speeches li');
    $tags = $('.tags');
    $tagButtons = $('.tags .btn').not('.reset-tags');
    $resetTagsButton = $('.reset-tags');
    $search = $('#search');
    $body = $('body');
    $refreshQuoteButton = $('#refresh-quote');
    $speechCount = $('.speech-count');
    $speechTotal = $('.speech-total');

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

        _.each(SPEECHES, function(speech) { searchIndex.add(speech); });

        $tagButtons.on('click', onTagButtonClick);
        $resetTagsButton.on('click', onResetTagsButtonClick);
        $search.on('keyup', filterSpeeches);
        $refreshQuoteButton.on('click', onRefreshQuoteButtonClick);

        hasher.changed.add(onHashChanged);
        hasher.initialized.add(onHashChanged);
        hasher.init();
    }
});
