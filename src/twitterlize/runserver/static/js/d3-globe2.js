var feature; // eventually: all svg paths (countries) of the world

var country_reverse_lookup = {};

var projection = d3.geo.azimuthal()
    .scale(270)
    .origin([-71.03,42.37])
    .mode("orthographic")
    .translate([300, 270]);

var circle = d3.geo.greatCircle()
    .origin(projection.origin());

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select("#svgglobe").append("svg:svg")
    .attr("width",  600)
    .attr("height", 600)
    .on("mousedown", mousedown);

svg.append("circle")
    .attr('cx', 300)
    .attr('cy', 270)
    .attr('r', projection.scale())
   .attr("class","globe")
   .attr("filter", "url(#glow)")
   .attr("fill", "url(#gradBlue)");

if (frameElement) frameElement.style.height = '600px';

d3.json("static/data/world-countries.json", function(collection) {
  feature = svg.selectAll("path")
      .data(collection.features)
    .enter().append("svg:path")
    .on("mouseover", function(d) { 
        d3.select(this).style("fill", "#ffffff");
	$("#countrydesc").text(d.properties.name);
    })
    .on("mouseout", function(d) { 
        d3.select(this).style("fill", "#6CCC00"); 
	$("#countrydesc").text("");
	})
    .on("click", function(d) {
	select_country(d.id, d.properties.name, d.properties.geo);
     })
    .attr("class", "feature")
    .attr("d", clip);

  feature.append("svg:title")
      .text(function(d) { return d.properties.name; });

  var countries = get_countries(collection.features);
  $( "#countries" ).autocomplete({
    source: countries,
    appendTo: "#countrymenu",
    select: function(e, ui){
	select_country(country_reverse_lookup[ui.item.label]['name'], ui.item.label,country_reverse_lookup[ui.item.label]['geo']);
    }
  });
});


d3.select(window)
    .on("mousemove", mousemove)
    .on("mouseup", mouseup);

var m0
  , o0
  , done
  ;

function select_country(code, name, geo){
  if(!geo){
      geo = [-71.03,42.37];
  }
  projection.origin(geo);
  circle.origin(geo);
  refresh(1000);
  var domain = document.domain;
  $("#goto-selected").attr("href", "http://" + domain + ":8888/?code=" + code);
  $("#selected-country").text(name);
}

function mousedown() {
  m0 = [d3.event.pageX, d3.event.pageY];
  o0 = projection.origin();
  d3.event.preventDefault();
}

function mousemove() {
  if (m0) {
    var m1 = [d3.event.pageX, d3.event.pageY]
      , o1 = [o0[0] + (m0[0] - m1[0]) / 8, o0[1] + (m1[1] - m0[1]) / 8];
    projection.origin(o1);
    circle.origin(o1);
    refresh();
  }
}

function mouseup() {
  if (m0) {
    mousemove();
    m0 = null;
  }
}

function refresh(duration) {
  (duration ? feature.transition().duration(duration) : feature).attr("d", clip);
}

function clip(d) {
  return path(circle.clip(d));
}

function get_countries(features){
  var countries = [];
  for(var i=0; i<features.length; i++){
    countries.push(features[i].properties.name);
    country_reverse_lookup[features[i].properties.name] = {'name':features[i].id,'geo':features[i].properties.geo};
  }
  return countries;
}

function reframe(css) {
  for (var name in css)
    frameElement.style[name] = css[name] + 'px';
}
