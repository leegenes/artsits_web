var svg = d3.select("svg"),
  height = 100,
  width = 100,
  center_x = width / 2,
  center_y = height / 2
  big_r = (height * .9) / 2,
  theta = ((Math.PI*2) / artists.length);

var center = svg.append('g');

center.append('pattern')
  .attr('id', 'center_node')
  .attr('clipPathUnits', 'objectBoundingBox')
  .attr('width', "100%")
  .attr('height', "100%")
  .append('image')
  .attr('xlink:href', "")
  .attr('width', 0)
  .attr('height', 0);

center.append('circle')
  .attr('class', 'center-bakground')
  .attr('r', big_r)
  .attr('cx', center_x)
  .attr('cy', center_y)
  .attr('fill', "#fff");

center.append('circle')
    .attr('class', 'center_node')
    .attr('r', big_r)
    .attr('cx', center_x)
    .attr('cy', center_y)
    .attr('fill', "url(#center_node)")
    .style('opacity', .4)
    .style('filter', "alpha(opacity=40)");

center.append('text')
    .attr('id', 'big-name')
    .attr('x', '80%')
    .attr('y', '72.5%')
    .attr('text-anchor', 'end')
    .style('font-size', 3.75)
    .style('fill', '#485256')
    .style('font-family', 'sans-serif')
    .text('');

var nodeGroups = svg.selectAll('.group-node')
  .data(artists)
  .enter()
  .append('g')
  .attr('class', 'group-node')
  .attr('id', function (d) {
    return 'group-' + d.id;
  })
  .attr('x', function (d, i) {
        a = theta * i;
        return (big_r * Math.cos(a)) + center_x;
      })
  .attr('y', function (d, i) {
    a = theta * i;
    return (big_r * Math.sin(a)) + center_y;
  });

var patterns = nodeGroups.append('pattern')
  .attr('id', function (d) { return 'spattern-' + d.id; })
  .attr('clipPathUnits', 'userSpaceOnUse')
  .attr('width', 5.5)
  .attr('height', 5.5)
.append('image')
  .attr('xlink:href', function (d) { return d.img.url; })
  .attr('width', function (d) {
    if (d.img.width <= d.img.height) {
      return 5.5;
    }
  })
  .attr('height', function (d) {
    if (d.img.height <= d.img.width) {
      return 5.5;
    }
  });

var nodes = nodeGroups.append('circle')
      .attr('class', 'node')
      .on('mouseover', onMouse)
      .on('mouseout', offMouse)
      .attr('id', function (d) {
        return 'node-' + d.id;
      })
      .attr('cx', function (d, i) {
        a = theta * i;
        return (big_r * Math.cos(a)) + center_x;
      })
      .attr('cy', function (d, i) {
        a = theta * i;
        return (big_r * Math.sin(a)) + center_y;
      })
    .attr('r', 2.75)
    .attr('fill', function (d) { return 'url(#spattern-' + d.id + ')'; })
    .append('title')
      .text(function (d) { return d.name; });

function onMouse (d) {
  svg.select('#center_node')
    .select('image')
      .attr('xlink:href', d.img.url)
      .attr('width', setCenterWidth(d.img.width, d.img.height))
      .attr('height', setCenterHeight(d.img.width, d.img.height));

  svg.select('#big-name')
      .text(d.name);

  d.related_to.forEach( function (related) {
    group = d3.select("#group-" + related);
    x1 = group.attr('x');
    x2 = center_x + ((x1 - center_x) * .8);
    y1 = group.attr('y');
    y2 = center_y + ((y1 - center_y) * .8);
    group.select('#node-' + related).transition()
    .attr('cx', x2)
    .attr('cy', y2);
});
}

function offMouse(d) {
  d.related_to.forEach( function (related) {
    var group = d3.select('#group-' + related);
    var home_x = group.attr('x');
    var home_y = group.attr('y');
    var node = group.select('#node-' + related);
    node.transition()
    .attr('cx', home_x)
    .attr('cy', home_y);
  });
}

function setCenterWidth (width, height) {
  if (width <= height) {
    return big_r * 2;
  }
}

function setCenterHeight (width, height) {
    if (height <= width) {
      return big_r * 2;
    }
}
