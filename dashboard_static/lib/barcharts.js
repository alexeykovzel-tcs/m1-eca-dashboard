(function ($, block) {
  // a simple barchart example
  block.fn.barchart = function (config) {
    var options = $.extend(
      {
        series: {},
      },
      config
    );

    var bar_init = {
      xaxis: {
        mode: "categories",
        tickLength: 0,
      },
    };

    var bardata_series = options.series;

    var translate_bar = function () {
      var result = [];
      for (var k in bardata_series) {
        if (bardata_series.hasOwnProperty(k)) {
          var newserie = jQuery.extend({}, bardata_series[k]);
          var newdata = [];
          var data = newserie.data;
          for (var l in data) {
            if (data.hasOwnProperty(l)) {
              newdata.push([l, data[l]]);
            }
          }
          newserie.data = newdata;
          result.push(newserie);
        }
      }
      return result;
    };

    var plot = $.plot(this.$element, translate_bar(), bar_init);

    var addbar = function (serie_label, category, value) {
      var data;

      if (bardata_series[serie_label]) {
        data = bardata_series[serie_label].data;
      } else {
        data = {};
      }

      if (data.hasOwnProperty(category))
        data[category] = data[category] + value;
      else data[category] = value;
      redraw();
    };

    var setbar = function (serie_label, category, value) {
      var data = bardata_series[serie_label].data;
      data[category] = value;
      redraw();
    };

    var setbarFull = function (dataFull, serie) {
      // func which insert the hole bar(all categories and values) to corresponding serie
      bardata_series[serie] = {
        color: "blue",
        data: dataFull,
        bars: {
          // the values are chosen for this project specifically
          show: true,
          barWidth: 0.7,
          align: "center",
        },
      };
      redraw();
    };

    var redraw = function () {
      plot.setData(translate_bar());
      plot.setupGrid();
      plot.draw();
    };

    var reset = function () {
      for (var k in bardata_series) {
        if (bardata_series.hasOwnProperty(k)) {
          bardata_series[k].data = {};
        }
      }
    };

    this.actions({
      set: function (e, message) {
        setbar(message.series, message.value[0], message.value[1]);
      },
      setFull: function (e, message) {
        // linking 'setbarFull' to action named 'setFull'(used in dashboard.py)
        setbarFull(message.dataFull, message.serie);
      },
      add: function (e, message) {
        addbar(message.series, message.value[0], message.value[1]);
      },
      reset: function (e, message) {
        reset();
      },
    });
    // return element to allow further work
    return this.$element;
  };
})(jQuery, block);
