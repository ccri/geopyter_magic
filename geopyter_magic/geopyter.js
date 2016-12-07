(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        // http://localhost:8888/ also works here
        define(['exports',
                '../../nbextensions/d3js/d3.v4.4.min.js',
                '../../nbextensions/leaflet/leaflet.v1.0.2.min.js'],
                factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory(
            requirejs['exports',
                    '../../nbextensions/d3js/d3.v4.4.min.js',
                    '../../nbextensions/leaflet/leaflet.v1.0.2.min.js']);
    } else {
        factory((root.geopyter = {}), root);
    }
}(this, function(exports, d3, L) {

'use strict';

var createLeaflet = function(mapElementId, params, callbacks = []) {
    if (callbacks.length == 0) {
        callbacks.push(function(map, params) { 
            console.log(map);
            console.log(params);
        });
    }

    if (params.baseMaps == null)
        params.baseMaps = {'OSM': 'http://{s}.tile.osm.org/{z}/{x}/{y}.png'};
    
    if (document.getElementById(mapElementId) === null) {
        params.cell.append($('<div/>', {
            id: mapElementId,
            width: '100%',
            height: 512
        }));
    }

    if (params.bbox)
        var map = L.map(mapElementId).fitBounds(params.bbox);
    else
        var map = L.map(mapElementId).fitWorld();

    params.baseLayer = {};
    for (let k in params.baseMaps) {
        if (!params.baseMaps.hasOwnProperty(k))
            continue;
        params.baseLayer[k] = L.tileLayer(params.baseMaps[k]).addTo(map);
    }
    callbacks.push(loadControl);
    callbacks.map(function(callback) {
        console.log(callback);
        callback(map, params);
    });
};

var loadControl = function(map, params) {
    params.leafletControl = L.control.layers(params.baseLayer).addTo(map);
};

var loadCss = function(url) {
    var link = document.createElement('link');
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = url;
    document.getElementsByTagName('head')[0].appendChild(link);
    console.log(url + ' - loaded');
};

var test = function() {
    console.log('-- testing geopyter --');
    console.log(d3);
    console.log(L);
};

var geojsonToLeaflet = function(mapElementId, geojsonUrl, element) {
    var params = {};
    params.geojsonUrl = geojsonUrl;
    params.cell = element;

    var loadGeojson = function(map, params) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var geojson = JSON.parse(this.response);
                L.geoJSON(geojson).addTo(map);
            }
        }
        xhr.open('GET', params.geojsonUrl, true);
        xhr.send();
    }

    createLeaflet(mapElementId, params, [loadGeojson]);
};

var histogram = function(hgramElemId, data, element) {    
    if (document.getElementById(hgramElemId) === null)
        element.append($('<div/>', {id: hgramElemId}));
        
    data = d3.range(10000).map(d3.randomNormal(1000, 100)); // temporary
    console.log(data);
    var formatCount = d3.format(",.0f");
        
    var svg = d3.select('#'+hgramElemId)
        .append('svg')
            .attr('viewBox', '0 0 960 480')
            .attr('width', 960)
            .attr('height', 480);

    var margin = {top: 20, right: 0, bottom: 20, left: 0},
        width = svg.attr('width') - margin.left - margin.right,
        height = svg.attr('height') - margin.top - margin.bottom,
        g = svg.append('g')
            .attr('transform', 'translate('+margin.left+','+margin.top+')');

    var histogram = d3.histogram()(data);

    var xScale = d3.scaleLinear().rangeRound([0, width])
            .domain([d3.min(data, function(d) { return d; }),
                d3.max(data, function(d) { return d; })])
            .range([margin.left, width]);

    var xAxis = d3.axisBottom(xScale);
            
    var yScale = d3.scaleLinear()
        .domain([0, d3.max(histogram, function(d) { return d.length; })])
        .range([height, 0]);
    
    var bar = g.selectAll('.bar')
        .data(histogram)
        .enter().append('g')
            .attr('class', 'bar')
            .attr('transform', function(d) {
                return 'translate('+xScale(d.x0)+','+yScale(d.length)+')';
            });
    
    bar.append('rect')
        .attr('x', 1)
        .attr('width', width / histogram.length) // x(histogram[0].x1) - x(histogram[0].x0)
        .attr('height', function(d) { return height - yScale(d.length); });
    
    bar.append('text')
        .attr('dy', '.75em')
        .attr('y', -10)
        .attr('x', width / histogram.length / 2) // (x(histogram[0].x1) - x(histogram[0].x0))
        .attr('text-anchor', 'middle')
        .text(function(d) { return formatCount(d.length); });
    
    g.append('g')
        .attr('class', 'axis axis--x')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);
};

var timeSeries = function(tsElemId, data, element) {
    if (document.getElementById(tsElemId) == null)
        element.append($('<div/>', {id: tsElemId}));
    
    var svg = d3.select('#'+tsElemId)
            .append('svg')
                .attr('viewBox', '0 0 960 480')
                .attr('width', 960)
                .attr('height', 480)
                .attr('class', 'timeSeries');

    var margin = {top: 0, right: 20, bottom: 20, left: 30},
        width = svg.attr('width') - margin.left - margin.right,
        height = svg.attr('height') - margin.top - margin.bottom,
        g = svg.append('g')
            .attr('transform', 'translate('+margin.left+','+margin.top+')');
    
    var parseDate = d3.timeParse('%Y-%m-%d');
    
    var xScale = d3.scaleTime()
            .domain([d3.min(data, function(d) { return d.date; }),
                     d3.max(data, function(d) { return d.date; })])
            .range([margin.left, width]);

    var xAxis = d3.axisBottom()
            .scale(xScale)
            .tickFormat(d3.timeFormat('%Y-%m-%d'));
    
    var yScale = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return d.count; })])
            .range([height, margin.bottom]);

    var yAxis = d3.axisLeft()
            .scale(yScale);
    
    g.append('g')
        .attr('class', 'axis axis--x')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);
    
    g.append('g')
        .attr('class', 'axis axis--y')
        .call(yAxis);
    
    var bar = g.selectAll('.bar')
        .data(data)
        .enter().append('g')
            .attr('class', 'bar');

    bar.append('rect')
        .attr('class', 'databar')
        .attr('x', function(d) { return xScale(d.date); })
        .attr('y', function(d) { return yScale(d.count); })
        .attr('width', width / data.length)
        .attr('height', function(d) { return height - yScale(d.count); });
}

exports.leaflet = L;
exports.d3 = d3;

exports.test = test;
exports.createLeaflet = createLeaflet;
exports.geojsonToLeaflet = geojsonToLeaflet;
exports.histogram = histogram;
exports.timeSeries = timeSeries;

exports.load_ipython_extension = function() {
    console.log('geopyter - loading css');
    loadCss('../../nbextensions/leaflet/leaflet.css');
    loadCss('../../nbextensions/geopyter/geopyter.css');
};

}));