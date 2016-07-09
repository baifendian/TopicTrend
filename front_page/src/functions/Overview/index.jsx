import React from 'react'
import d3 from 'd3'
import G2 from 'public/g2'
import './index.less'

const simpleFormat = d3.time.format("%Y-%m-%d");

const customTimeFormat = d3.time.format.multi([
  //["%a %d日", function(d) { return d.getDay() && d.getDate() != 1; }],
  ["%-d日", function(d) { return d.getDate() != 1; }],
  ["%-m月", function(d) { return d.getMonth(); }],
  ["%Y年", function() { return true; }]
]);

var TimelineChart = function (element) {
  var self = this;

  var today = new Date((new Date(simpleFormat(new Date())).getTime())-24*3600*1000*5);

  self.cache = {};
  self.color = d3.scale.category20();
  self.ruler_width = 120;
  self.cache = {};
  self.pre_date = simpleFormat(today);
  self.zoomend_status = Math.random(); //zoom结束状态变量

  init();

  function init() {
    var elementWidth = element.clientWidth;
    var elementHeight = element.clientHeight;

    self.width = elementWidth>800 ? elementWidth : 800;
    self.height = elementHeight>600 ? elementWidth : 600;
    self.width_8p = parseInt(elementWidth * 0.75);

    self.y = d3.time.scale().domain([new Date('2016-06-30'), new Date('2016-07-10')]).range([0, self.height]);
    self.yAxis = d3.svg.axis()
        .scale(self.y)
        .tickFormat(customTimeFormat)
        .tickPadding(22)
        .ticks(6)
        .orient('right');
    self.bubble_layout = d3.layout.pack()
        .size([self.width_8p, self.height])
        .sort(null)
        .value(function(d) {return d.influence; })
        .padding(8);

    self.svg = d3.select(element).append('svg')
        .attr('width', self.width)
        .attr('height', self.height);

    append_defs();
    append_background();

    make_cook();

    flush_bubbles(1, self.pre_date);
  }

  /**
   * 添加定義：線性漸變
   * @param svg
   */
  function append_defs(svg) {
    var defs = self.svg.append('defs');
    var background = defs.append('linearGradient').attr('id', 'background');
    background.append('stop')
        .attr('offset', '5%')
        .attr('stop-color', "#D5EFF7")
        .attr('stop-opacity', 0.6);
    background.append('stop')
        .attr('offset', '95%')
        .attr('stop-color', "#FFFFFF")
        .attr('stop-opacity', 0.6);

    var backgroundReverse = defs.append('linearGradient').attr('id', 'backgroundReverse');
    backgroundReverse.append('stop')
        .attr('offset', '5%')
        .attr('stop-color', "#FFFFFF");
    backgroundReverse.append('stop')
        .attr('offset', '95%')
        .attr('stop-color', "#D5EFF7");

    var directive = defs.append('linearGradient').attr('id', 'directive');
    directive.append('stop')
        .attr('offset', '5%')
        .attr('stop-color', "#FFFFFF")
        .attr('stop-opacity', 0.4);
    directive.append('stop')
        .attr('offset', '50%')
        .attr('stop-color', "#FFFFFF")
        .attr('stop-opacity', 1);
    directive.append('stop')
        .attr('offset', '95%')
        .attr('stop-color', "#FFFFFF")
        .attr('stop-opacity', 0.4);
  }

  /**
   * 添加背景漸變
   */
  function append_background() {
    self.svg.append('rect')
        .style('fill', 'url(#background)')
        .attr('x', self.width_8p+self.ruler_width)
        .attr('y', 0)
        .attr('height', self.height)
        .attr('width', self.width-self.width_8p);
    self.svg.append('rect')
        .style('fill', 'url(#backgroundReverse)')
        .attr('x', 0)
        .attr('y', 0)
        .attr('height', self.height)
        .attr('width', self.width_8p);
  }

  /**
   * 開始作圖
   */
  function make_cook() {
    var zoom = d3.behavior.zoom()
        .center([0, self.height/2])
        .scaleExtent([0.7, 30])
        .on('zoom', zoomon)
        .y(self.y);

    zoom.translate([0, -1*(self.y(today)-self.height/2-14)]);

    bind_axis(zoom);
  }

  /**
   * 綁定
   * @param zoom
   */
  function bind_axis(zoom) {
    var axis_g = self.svg.append('g')
        .attr('transform', 'translate('+self.width_8p+',0)')
        .call(zoom);

    axis_g.append('rect')
        .attr('class', 'axis-bounds')
        .attr('x', 0)
        .attr('y', -10)
        .attr('height', self.height+100)
        .attr('width', self.ruler_width)
        .attr('stroke', '#76C552')
        .attr('stroke-width', '3')
        .attr('fill', '#E3F7DF');

    axis_g.append('g')
        .attr('class', 'y axis')
        .attr('transform', 'translate(0,0)')
        .call(self.yAxis);

    var directive_g = axis_g.append('g').attr('transform', 'translate(60,'+ self.height/2 +')')
    directive_g.append('rect')
        .style('fill', 'url(#directive)')
        .attr('x', -60)
        .attr('y', -12)
        .attr('height', 24)
        .attr('width', self.ruler_width);
    directive_g.append('text')
        .attr('id', 'directive_text')
        .style("text-anchor", "middle")
        .attr('y', '.3em')
        .text(function(){
          var range = self.y.domain();
          return simpleFormat(new Date((range[1].getTime() + range[0].getTime())/2));
        });
  }


  /**
   * zoom监听函数: zoomon
   * zoom时触发
   */
  function zoomon() {
    self.zoomend_status = Math.random();

    var range = self.y.domain();
    self.svg.select('#directive_text').text(simpleFormat(new Date((range[1].getTime() + range[0].getTime())/2)));

    self.svg.select('.y.axis').call(self.yAxis);

    var event = d3.event;
    setTimeout((function(zoomend_status){
      return function() {
        if (zoomend_status == self.zoomend_status) {
          var range = self.y.domain();
          var final_date = simpleFormat(new Date((range[1].getTime() + range[0].getTime()) / 2))
          console.log('final date:' + final_date);

          var source_event = event.sourceEvent;
          console.log(source_event.movementY);
          if (source_event && source_event.type == 'mousemove' && self.pre_date != final_date) {
            flush_bubbles(source_event.movementY > 0 ? 1 : -1, final_date);
            self.pre_date = final_date;
          }
        }
      }
    })(self.zoomend_status), 500);
  }

  /**
   * 刷新氣泡圖
   * @param direction
   * @param final_date
   */
  function flush_bubbles(direction, final_date) {
    console.log('flush bubbles');

    var data_url = 'http://172.24.3.71:8002/data/events/?date=' + final_date;

    if (self.cache[data_url]) {
      handle_bubles_data(direction, self.cache[data_url]);
    }
    else {
      d3.json(data_url, function (res) {
        if (res.rc != 0) {
          return;
        }

        console.log(res);
        self.cache[data_url] = res.data;

        handle_bubles_data(direction, res.data);
      })
    }
  }

  function handle_bubles_data(direction, data) {
    var daily_data = {'name': 'events', "children": data.elements};
    //console.log(JSON.stringify(daily_data));
    draw_bubbles(direction, daily_data);
  }

  function draw_bubbles(direction, daily_data) {
    self.svg.selectAll(".bubbles_root").transition().duration(500)
        .attr('transform', 'translate(0,'+direction*self.height+')')
        .remove();

    if (!daily_data.children || daily_data.children.length == 0) {
      return ;
    }
    var bubble_id = 'g_'+Math.random().toString(36).substr(2);
    var bubbles = self.svg.append('g')
        .attr('id', bubble_id)
        .attr('class', 'bubbles_root')
        .attr('transform', 'translate(0,'+ (-1*direction*self.height) +')');

    var node = bubbles.selectAll(".node")
        .data(self.bubble_layout.nodes(daily_data).filter(function(d) { return !d.children; }))
        .enter().append("g")
        .attr("class", "bubble")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
        .on("mouseover", function(d) {return activateBubble(d);})
        .on("mouseleave", function(d) {return resetBubbles();})
        .on("click", function(d) {return show_tip(d);});

    node.append("title")
        .text(function(d) { return d.desc + ": " + d.influence; });

    node.append("circle")
        .attr("r", function(d) { return d.r; })
        .style("fill", function(d) { return self.color(d.id); });

    node.append("text")
      //.attr("dy", ".3em")
        .style("text-anchor", "middle")
        .attr("font-size", "1em")
        .text(function(d) {
          return d.desc;
        });

    self.svg.selectAll('#'+bubble_id).transition().duration(500)
        .attr('transform', 'translate(0,0)');
  }

  function activateBubble(d) {
    // increase this bubble and decrease others
    var trans = self.svg.selectAll(".bubble").transition().duration(350);

    var current_d = d;
    var mutative_radius = current_d.r*0.6 > 32 ? 32 : current_d.r*0.4;

    trans.selectAll(".bubble > circle")
        .attr("r", function(d) {
          if(d.id == current_d.id)
            return d.r + mutative_radius;
          else
            return (d.r - mutative_radius) > 14 ? (d.r - mutative_radius) : 14;
        });

    trans.selectAll(".bubble > text")
        .attr("font-size", function(d){
          if(d.id == current_d.id)
            return "1.5em";
          else
            return ".6em";
        });
  }

  function resetBubbles() {
    // increase this bubble and decrease others
    var trans = self.svg.selectAll(".bubble").transition().duration(350);

    trans.selectAll(".bubble > circle")
        .attr("r", function(d) {
          return d.r;
        });

    trans.selectAll(".bubble > text")
        .attr("font-size", "1em");
  }

  function show_tip(d) {
    var data_url = 'http://172.24.3.71:8002/data/events/lifetime/?id=' + d.id;

    if (self.cache[data_url]) {
      handle_lifetime_data(self.cache[data_url]);
    }
    else {
      d3.json(data_url, function (res) {
        if (res.rc != 0) {
          return;
        }

        console.log(res);
        self.cache[data_url] = res.data;

        handle_lifetime_data(res.data);
      })
    }
  }

  function handle_lifetime_data(data) {
    var dd = [];
    var elements = data.elements;
    if (elements) {
      elements.forEach(function(d){
        dd.push({time: new Date(d.date), value: d.influence})
      })
    }
    //console.log(JSON.stringify(dd));
    draw_lifetime(dd);
  }

  var chart;
  function draw_lifetime(data) {
    if (chart) {
      chart.destroy();
    }

    chart = new G2.Chart({
      id: 'lifetime',
      width: 600,
      height: 300
    });
    chart.source(data, {
      time: {
        type: 'time',
        mask: 'mm-dd',
        alias: '日期'
      },
      value: {
        alias: '事件影响力'
      }
    });
    chart.legend(false);
    chart.line().position('time*value').shape('smooth').size(2);
    chart.point().position('time*value').shape('circle').size(4);
    chart.render();
  }
};

export default React.createClass({
  componentDidMount: function componentDidMount() {
    console.log(this);
    new TimelineChart(this.refs.chart);
  },
  render() {
    //console.log(customTimeFormat(new Date()));
    var chart = React.createElement('div', {className: 'timeline-chart', style: { height: '100%' }, ref: 'chart' });
    return chart
  }
})