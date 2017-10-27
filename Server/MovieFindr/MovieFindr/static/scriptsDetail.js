$(document).ready ( function(){
	
	var poster = "http://moviefindr.thomaskamps.nl/static/placeholder.png";
        if ("Poster" in jsonData["_source"]) {
	        if (jsonData["_source"]["Poster"] != "N/A") {
		        poster = jsonData["_source"]["Poster"];
	        }
        }
        
   document.title = "Info about " + jsonData["_source"]["Title"];
   $('#title').html(jsonData["_source"]["Title"]);
   $('#plot').html(jsonData["_source"]["Plot"]);
   $('#poster').html("<img src=\"" + poster + "\" class=\"img-rounded\" alt=\"cover\" style=\"width:80%; margin-top: 25px;\"/>");
   
   var properties = ["Genre", "Director", "Year", "Runtime", "Production", "Language", "imdbRating", "Awards", "Writer", "Actors"];
   var toAppend = "<table class=\"table table-striped table-bordered\">";
   
   properties.forEach(function(item) {
	   if (item in jsonData["_source"]) {
		   toAppend += "<tr><td>" + item + "</td><td>" + jsonData["_source"][item] + "</td></tr>";
	   }
   })
   
   $('#table').html(toAppend);
   
});

var showFull = function() {
	$('#fulltext').html("<p>"+jsonData["_source"]["body"]+"</p>");
}