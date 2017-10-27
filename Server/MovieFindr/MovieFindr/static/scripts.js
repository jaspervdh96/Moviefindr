function getCheckedBoxes(chkboxName) {

    var checkboxes = document.getElementsByName(chkboxName);
    var checkboxesChecked = [];

    for (var i=0; i<checkboxes.length; i++) {

        if (checkboxes[i].checked) {
            checkboxesChecked.push(checkboxes[i].value);
        }
    }

    return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}

$('#searchForm').on('submit', (function(e) {

    e.preventDefault();
    $('#wordcloud').html("");

    var checkedBoxes = getCheckedBoxes("genre");
    var query = $("#query").val();
    var match_phrase = document.getElementsByName("match_phrase")[0].checked
    var person = $("#person").val();
    var upperDate = $("#upperDate").val();
    var lowerDate = $("#lowerDate").val();
    var data = {'query': query, 'person': person, 'lowerDate': lowerDate, 'upperDate': upperDate, 'genres': JSON.stringify(checkedBoxes), "match_phrase": match_phrase}

    $.post('/search', data, function(data, status) {

        if (status == "success") {
	        
            parsedData = JSON.parse(data);

            if (parsedData["hits"]["total"] > 0) {

                displayMovies(parsedData["hits"]["hits"], parsedData["hits"]["max_score"]);
                d3.wordcloud().size([1200, 600]).selector('#wordcloud').words(parsedData["hits"]["tfidf"]).start();
                
                window.timeline = new TL.Timeline('timeline-embed', parsedData["hits"]["timeline"]);
                
            } else {

                alert("No results were found...");
            }

        } else {

            alert("Er ging iets fout");
        }
    })    
}))

var displayMovies = function(movieData, max_score) {

    var append = "";
    var count = 1;
    console.log((max_score / 3));
    for(var i = 0; i < movieData.length; i++) {
	    if(movieData[i]["_score"] > (max_score / 3) && movieData[i]["_score"] > 0.05) {
	        if(count % 4 == 0) {
	            append += "<div class='row'>"
	        }
	        var poster = "http://moviefindr.thomaskamps.nl/static/placeholder.png";
	        if ("Poster" in movieData[i]["_source"]) {
		        if (movieData[i]["_source"]["Poster"] != "N/A") {
			        poster = movieData[i]["_source"]["Poster"];
		        }
	        }
	        var pre_append = "<div class='col-lg-3'><div class=\"panel panel-default\"><img src=\"" + poster + "\" class=\"img-rounded\" alt=\"cover\" style=\"width:80%; margin-left: 10%; margin-top: 25px;\"/><h3 style=\"text-align:center;\">" + movieData[i]["_source"]["Title"] + "<br/><a href=\"detail?id=" + movieData[i]["_id"] + "\" target=\"_blank\"><button type=\"button\" class=\"btn btn-info\" style=\"margin-top: 10px; margin-bottom: 10px;\">View more information</button></a></h3></div></div>";
	        append += pre_append;
	        if(count % 4 == 0) {
	            append += "</div>"
	        }
	        count += 1;
	    }
    }
    if (count == 1) {
	    alert("No results were found...")
    }
    $("#movies").html(append);
}

// make genre checkboxes
append = "";
['Drama', 'Comedy', 'Action', 'Crime', 'Thriller', 'Adventure', 'Romance', 'Horror', 'Mystery', 'Sci-Fi', 'Fantasy', 'Biography', 'Short', 'Animation', 'History', 'Family', 'Documentary', 'Sport', 'Music', 'War', 'Musical', 'Western'].forEach(function(item) {
	append += '<label class="form-check-label"><input class="form-check-input" type="checkbox" id="genre' + item + '" value="' + item + '" name="genre" style="margin-left: 15px;"> ' + item + '</label>';
})

$("#genres").html(append);
