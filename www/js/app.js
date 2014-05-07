var $speeches = null;
var $tagsFilter = {};
var $search = null;
var $body = null;
var $leadQuote = null;
var $refreshQuoteButton = null;
var moodSpeech = null;
var speechSlug = speechSlug||null;

var searchIndex = null;

var filterSpeeches = function() {
    $speeches.hide();

    var $visibleSpeeches = $speeches;
    var query = $search.val();
    var tags = $tagsFilter.val();

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

var getNewSpeech = function(key, value){
    var newSpeech = _.chain(SPEECHES)
                     .shuffle()
                     .filter(function(pair){
                         return pair[key] == value && pair['slug'] !== speechSlug && pair['slug'] !== moodSpeech;
                     })
                     .value()[0];

    if (newSpeech === undefined){
        newSpeech = _.chain(SPEECHES)
                     .shuffle()
                     .filter(function(pair){
                         return pair['slug'] !== speechSlug && pair['name'] !== '' && pair['slug'] !== moodSpeech;
                     })
                     .value()[0];
    }

    if (key === 'mood'){
        moodSpeech = newSpeech['slug'];
    }

    return newSpeech;
}

var renderLeadQuote = function(){
    var leadQuote = getNewSpeech();
    var context = leadQuote;
    var html = JST.quote(context);

    $leadQuote.html(html);
    _.defer(function(){
        $leadQuote.find('blockquote').addClass('fadein');
    });
}

$(function() {
    $speeches = $('.speeches li');
    $tagsFilter = $('#tags-filter');
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

        renderLeadQuote();

        _.each(SPEECHES, function(speech) {
            searchIndex.add(speech);
        });

        $tagsFilter.on('change', filterSpeeches);
        $search.on('keyup', filterSpeeches);
        $refreshQuoteButton.on('click', renderLeadQuote);

    }

    if ($body.hasClass('speech')){
        var $mood = $('.mood');
        var $topic = $('.topic');

        var newMoodSpeech = getNewSpeech('mood', speechMood);
        var newAdviceSpeech = getNewSpeech('tags', speechAdvice);

        $mood.attr('href', APP_CONFIG.S3_BASE_URL + '/speech/' + newMoodSpeech.slug + '/');
        $mood.find('h4').text(newMoodSpeech.name);
        $mood.find('span').text(newMoodSpeech.mood);
        $topic.attr('href', APP_CONFIG.S3_BASE_URL + '/speech/' + newAdviceSpeech.slug + '/');
        $topic.find('h4').text(newAdviceSpeech.name);
        $topic.find('span').text(newAdviceSpeech.tags);
    }
});
