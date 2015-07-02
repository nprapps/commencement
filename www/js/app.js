var $speeches = null;
var $tags = null;
var $tagButtons = null;
var $resetSearchButton = null;
var $search = null;
var $searchForm = null;
var $body = null;
var $leadQuote = null;
var $imgSource = null;
var $refreshQuoteButton = null;
var $noResults = null;
var $speechCount = null;
var $speechTotal = null;
var $emailShare = null;
var $facebookShare = null;
var $twitterShare = null;
var $pinterestShare = null;
var FEATURED = null;
var featured_position = 0;

var searchIndex = null;

var filterSpeeches = function() {
    $speeches.hide();

    var $visibleSpeeches = $speeches;
    var query = $search.val();
    var tags = $tags.find('.active').first().data('tag');
    var showReset = false;

    if (query) {
        var results = searchIndex.search(query);
        var slugs = _.pluck(results, 'ref');
        var ids = _.map(slugs, function(s) { return '#' + s });

        $visibleSpeeches = $(ids.join(','));

        showReset = true;
    }

    if (tags) {
        $visibleSpeeches = $visibleSpeeches.filter('.tag-' + tags)

        showReset = true;
    }

    if (showReset) {
        $resetSearchButton.show();
    } else {
        $resetSearchButton.hide();
    }

    $visibleSpeeches.show();

    if ($visibleSpeeches.length > 0){
        $noResults.hide();
        $speechCount.html($visibleSpeeches.length);
        $speechCount.parent('p').show();
    } else {
        $noResults.show();
        $speechCount.html(0);
        $speechCount.parent('p').show();
    }
}

var renderLeadQuote = function() {

    // Indexes into the list of featured quotes using the global state
    // of where you are in the list.
    var context = FEATURED[featured_position];
    if (featured_position == (FEATURED.length - 1)) {
        featured_position = 0;
    } else {
        featured_position += 1;
    }

    // Loads the identified quote with some easing animation.
    var html = JST.quote(context);
    var src = context['img_source'];

    $leadQuote.fadeOut('fast', function(){
        $leadQuote.css('height', 'auto');
        $leadQuote.html(html);
        $leadQuote.fadeIn();
    });
}

var renderMostViewed = function(data) {
    var context = data;

    // Loads the identified quote with some easing animation.
    var html = JST.most_viewed(context);
    $('#most-viewed').html(html);
}

var onTagButtonClick = function() {
    var tag = $(this).data('tag');
    hasher.setHash(tag);
    _gaq.push(['_trackEvent', 'Filters', 'onTagButtonClick', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('select-tag', tag);
}

var onResetSearchButtonClick = function() {
    $search.val('');
    hasher.setHash('_');
    _gaq.push(['_trackEvent', 'Filters', 'onResetSearchButtonClick', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('reset-search');
}

var onRefreshQuoteButtonClick = function() {
    renderLeadQuote();
    _gaq.push(['_trackEvent', 'Featured Quote', 'onRefreshQuoteButtonClick', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('refresh-quote');
}

var onFeaturedSpeechImageClick = function(slug) {
    _gaq.push(['_trackEvent', 'Social', 'Click Image Link From Featured Quote', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('featured-quote-image-click', slug);
}

var onFeaturedSpeechEmailClick = function(slug) {
    _gaq.push(['_trackEvent', 'Social', 'Click Email From Featured Quote', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('featured-quote-email-click', slug);
}

var onFeaturedSpeechFacebookClick = function(slug) {
    _gaq.push(['_trackEvent', 'Social', 'Click Facebook From Featured Quote', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('featured-quote-facebook-click', slug);
}

var onFeaturedSpeechTwitterClick = function(slug) {
    _gaq.push(['_trackEvent', 'Social', 'Click Twitter From Featured Quote', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('featured-quote-twitter-click', slug);
}

var onFeaturedSpeechPinterestClick = function(slug) {
    _gaq.push(['_trackEvent', 'Social', 'Click Pinterest From Featured Quote', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('featured-quote-pinterest-click', slug);
}

var onSpeechDetailImageClick = function() {
    _gaq.push(['_trackEvent', 'Social', 'Click Image Link From Speech Detail', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('speech-detail-image-click', speechSlug);
}

var onSpeechDetailEmailClick = function() {
    _gaq.push(['_trackEvent', 'Social', 'Click Email From Speech Detail', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('speech-detail-email-click', speechSlug);
}

var onSpeechDetailFacebookClick = function() {
    _gaq.push(['_trackEvent', 'Social', 'Click Facebook From Speech Detail', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('speech-detail-facebook-click', speechSlug);
}

var onSpeechDetailTwitterClick = function() {
    _gaq.push(['_trackEvent', 'Social', 'Click Twitter From Speech Detail', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('speech-detail-twitter-click', speechSlug);
}

var onSpeechDetailPinterestClick = function() {
    _gaq.push(['_trackEvent', 'Social', 'Click Pinterest From Speech Detail', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('speech-detail-pinterest-click', speechSlug);
}

var onSpeechDetailRelatedClick = function() {
    _gaq.push(['_trackEvent', 'Filters', 'Click Tag Link From Speech', APP_CONFIG.PROJECT_SLUG]);
    ANALYTICS.trackEvent('speech-detail-related-click', speechSlug);
}

var onFormSubmit = function(e) {
    e.preventDefault();
}

var onHashChanged = function(new_hash, old_hash) {
    if (new_hash === '_') { new_hash = ''; }

    if (new_hash === '') {
        $tagButtons.removeClass('active');
    } else {
        var $this = $('div.tags li a[data-tag="' + new_hash + '"]');
        $tagButtons.not($this).removeClass('active');
        $this.toggleClass('active');

        _.defer(function(){
            $.scrollTo('.tags', { duration: 350 })
        });
    }

    filterSpeeches();
};

$(function() {
    $speeches = $('.speeches .speech');
    $tags = $('.tags');
    $tagButtons = $('.tags .btn').not('.reset-tags');
    $resetSearchButton = $('.reset-tags');
    $searchForm = $('.filters form');
    $search = $('#search');
    $body = $('body');
    $refreshQuoteButton = $('#refresh-quote');

    $emailShare = $('.share-email');
    $facebookShare = $('.share-facebook');
    $twitterShare = $('.share-twitter');
    $pinterestShare = $('.pinterest-share');

    $emailShare.on('click', ANALYTICS.clickEmail);
    $facebookShare.on('click', ANALYTICS.clickFacebook);
    $twitterShare.on('click', ANALYTICS.clickTweet);
    $pinterestShare.on('click', ANALYTICS.clickPinterest);

    if ($body.hasClass('homepage')){
        $leadQuote = $('#lead-quote');
        $imgSource = $('.img-source');
        $noResults = $('#no-results');
        $speechCount = $('.speech-count');
        $speechTotal = $('.speech-total');

        $tagButtons.on('click', onTagButtonClick);
        $resetSearchButton.on('click', onResetSearchButtonClick);
        $search.on('keyup', filterSpeeches);
        $refreshQuoteButton.on('click', onRefreshQuoteButtonClick);
        $searchForm.on('submit', onFormSubmit);

        // Get the featured speeches.
        FEATURED = _.shuffle(_.filter(SPEECHES, function(speech) {
            return speech.img;
        }));
        onRefreshQuoteButtonClick();

        for (i = 0; i < SPEECHES.length; i++) {
            SPEECHES[i]['simple_name'] = SPEECHES[i]['name'].replace(/[\.,-\/#!$%\^&\*;:{}=\-_`~()']/g, '')
        }

        // Set up the search index.
        searchIndex = lunr(function () {
            this.field('name', {boost: 10})
            this.field('simple_name', {boost: 10})
            this.field('school')
            this.field('year')
            this.ref('slug')
        })
        _.each(SPEECHES, function(speech) { searchIndex.add(speech); });

        hasher.changed.add(onHashChanged);
        hasher.initialized.add(onHashChanged);
        hasher.init();

        $speechTotal.html(SPEECHES.length);
    }
});
