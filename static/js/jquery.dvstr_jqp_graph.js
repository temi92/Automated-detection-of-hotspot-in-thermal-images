/*######################################################
Devstratum JQP Graph
jQuery plugin for render simple html block graphs

Version: 1.0
License: GNU General Public License v3.0
Author: Sergey Osipov
Website: https://devstratum.ru
Email: info@devstartum.ru
Repo: https://github.com/devstratum/Devstratum-JQP-Graph

     _                _             _
  __| | _____   _____| |_ _ __ __ _| |_ _   _ _ __ ___
 / _` |/ _ \ \ / / __| __| '__/ _` | __| | | | '_ ` _ \
| (_| |  __/\ V /\__ \ |_| | | (_| | |_| |_| | | | | | |
 \__,_|\___| \_/ |___/\__|_|  \__,_|\__|\__,_|_| |_| |_|

########################################################*/

;(function(factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery'], factory);
    } else if (typeof exports !== 'undefined') {
        module.exports = factory(require('jquery'));
    } else {
        factory(jQuery);
    }
}(function($) {

    // default options
    var defGraph = {
        title: '',
        description: '',
        unit: '',
        better: '',
        type: 'number',
        separate: false,
        grid_wmax: 0,
        grid_part: 5,
        points: [],
        graphs: []
    };

    // calcWidthPercent
    function calcWidthPercent(grid_wmax, val) {
        var percent = (val / grid_wmax) * 100;
        return percent.toFixed(4);
    }

    // calcValueSeconds
    function calcValueSeconds(val) {
        var seconds = 0;
        var time_array = val.split(':');
        time_array.reverse();

        // hours
        if (time_array[2]) {
            seconds = seconds + (Number(time_array[2]) * 3600);
        }
        // minutes
        if (time_array[1]) {
            seconds = seconds + (Number(time_array[1]) * 60);
        }
        // seconds
        if (time_array[0]) {
            seconds = seconds + Number(time_array[0]);
        }

        return seconds;
    }

    // calcGridMax
    function calcGridMax(options) {
        var output = 0;

        if (options.grid_wmax && typeof options.grid_wmax === 'number') {
            output = options.grid_wmax;
        } else {
            var bufer_max = 0;
            if (typeof options.graphs === 'object') {
                options.graphs.forEach(function(item) {
                    item.value.forEach(function(val) {
                        // check type
                        if (options.type === 'time') {
                            val = calcValueSeconds(val);
                        }

                        if (val > bufer_max) {
                            bufer_max = val;
                        }
                    });
                });
            }

            if (bufer_max > 100) {
                output = Math.ceil(bufer_max / 100) * 100;
            } else {
                output = Math.ceil(bufer_max);
            }

        }

        return output;
    }

    // calcGridStep
    function calcGridStep(grid_wmax, grid_part) {
        var i = 0;
        var output = '';
        var offset = 100 / grid_part;
        var grid_step = Math.round(grid_wmax / grid_part);
        while (grid_part > i) {
            var percent = Math.floor(i * offset);
            var val = i * grid_step;
            output += '<div class="dvstr-graph__grid-vrt-line" style="left:' + percent + '%;"><span>' + val + '</span></div>';
            i++;
        }

        return output;
    }

    // getGrid
    function getGrid(grid_wmax, grid_part) {
        var output = '';

        output += '<div class="dvstr-graph__grid">';
        output += '<div class="dvstr-graph__grid-hrz"></div>';
        output += '<div class="dvstr-graph__grid-vrt">' + calcGridStep(grid_wmax, grid_part) + '</div>';
        output += '<div class="dvstr-graph__grid-end"><span>' + grid_wmax + '</span></div>';
        output += '</div>';

        return output;
    }

    // getHeader
    function getHeader(options) {
        var output = '';

        output += '<div class="dvstr-graph__header">';

        if (options.title) {
            output += '<div class="dvstr-graph__title">' + options.title + '</div>';
        }

        output += '<div class="dvstr-graph__header-flex">';

        if (options.unit) {
            output += '<div class="dvstr-graph__header-flex-item">';
            output += '<div class="dvstr-graph__unit">' + options.unit + '</div>';
            output += '</div>';
        }

        var graph_points = getGraphPoints(options);

        if (graph_points) {
            output += '<div class="dvstr-graph__header-flex-item">';
            output += graph_points;
            output += '</div>';
        }

        if (options.better) {
            output += '<div class="dvstr-graph__header-flex-item">';
            output += '<div class="dvstr-graph__better">(' + options.better + ')</div>';
            output += '</div>';
        }

        output += '</div>';

        if (options.description) {
            output += '<div class="dvstr-graph__description">' + options.description + '</div>';
        }

        output += '</div>';

        return output;
    }

    // getGraphPoints
    function getGraphPoints(options) {
        var output = '';

        if (typeof options.points === 'object') {
            output += '<div class="dvstr-graph__point">';
            options.points.forEach(function(item) {
                var point_color = '';
                if (item.color) {
                    point_color = 'background: ' + item.color + ';';
                }

                if (item.title) {
                    output += '<div class="dvstr-graph__point-item">';
                    output += '<span class="dvstr-graph__point-item-color" style="' + point_color + ';"></span>';
                    output += '<span class="dvstr-graph__point-item-title">' + item.title + '</span>';
                    output += '</div>';
                }
            });
            output += '</div>';
        }

        return output;
    }

    // getGraphItems
    function getGraphItem(options, grid_wmax) {
        var output = '';

        if (typeof options.graphs === 'object') {
            options.graphs.forEach(function(item) {
                output += '<div class="dvstr-graph__item">';
                output += '<div class="dvstr-graph__label">' + item.label + '</div>';
                output += '<div class="dvstr-graph__group">';

                if (item.value) {
                    var index = 999;

                    item.value.forEach(function (val, i) {
                        // check type
                        if (options.type === 'time') {
                            var val_time = val;
                            val = calcValueSeconds(val);
                        }

                        if (typeof val === 'number') {
                            var line_index = 'z-index: ' + (index--) + ';';

                            var line_width = 'width: ' + calcWidthPercent(grid_wmax, val) + '%;';

                            var line_color = '';
                            if (item.color) {
                                line_color = 'background: ' + item.color[i] + ';';
                            }

                            var line_separate = 'position: absolute;';
                            if (options.separate) {
                                line_separate = 'position: relative;';
                            }

                            output += '<div class="dvstr-graph__line" style="' + line_width + line_color + line_separate + line_index +'">';
                            // check type
                            if (options.type === 'time') {
                                output += '<i class="time">' + val_time + '</i>';
                            }
                            output += '<span>' + val + '</span>';
                            output += '</div>';
                        }
                    });
                }

                output += '</div>';
                output += '</div>';
            });
        }

        return output;
    }

    // createGraph
    function createGraph(object, options) {
        var grid_wmax = calcGridMax(options);
        var grid_part = options.grid_part;

        var graph_grid = getGrid(grid_wmax, grid_part);
        var graph_header = getHeader(options);
        var graph_item = getGraphItem(options, grid_wmax);

        var output = '';

        output += '<div class="dvstr-graph">';

        output += graph_header;

        if (grid_wmax) {
            output += '<div class="dvstr-graph__body">';
            output += graph_grid;
            output += graph_item;
            output += '</div>';
        }

        output += '</div>';

        object.append(output);
    }

    // methods dvstr_graph
    var methods = {
        init: function(options) {
            var _ = this;
            var newOptions = $.extend({}, defGraph, options);

            createGraph(_, newOptions);
        }
    };

    // dvstr_graph
    $.fn.dvstr_graph = function(method) {
        var _ = this;

        if (methods[method]) {
            return methods[method].apply(_, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(_, arguments);
        } else {
            $.error('dvstr_graph method: ' +  method + 'not found');
        }

        return true;
    };
}));