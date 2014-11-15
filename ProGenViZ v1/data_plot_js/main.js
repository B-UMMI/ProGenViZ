// main.js

//Global stats of the representation. Call for visualization creation functions.
  var snap      = function(i) { return function() { return i; }; }

  var get_info  = function(data_set, format) {

    var degree  = Math.PI / 180,
        x_max   = $(window).width()-($(window).width() * 0.14),  x_off   = x_max * 0.5,
        y_max   = $(window).height() - ($(window).height() * 0.09),    y_off   = y_max * 0.5;

    if (format === 'conv') {  // "conventional"
      var a_off   =   20,
          a_so    =    0,     a_st    = (260 - a_off),
          a_to    = 100,     a_ts    = (120 + a_off),
          a_fivo   = 55,    a_fivs  = (300 - a_off),
          a_seto   = 180,    a_sets  = (300 - a_off),
          i_rad   =   1000,     o_rad   = 30000;

    } else {                  // "rectangular"
      var a_so    =  -45,     a_st    = 45,
          a_to    = -135,     a_ts    = 135,
          i_rad   =   25,     o_rad   = 350;
    }

    var info  = {
      'global': {
        'selector':       ( snap(data_set) )(),
        'x_max':          x_max,      'x_off':          x_off,
        'y_max':          y_max,      'y_off':          y_off,
        'inner_radius':   i_rad,      'outer_radius':   o_rad
      },

      'axes': {
        'Str1':  { 'angle':  degree * a_so },
        'Str2':  { 'angle':  degree * a_st },
        'Str3':  { 'angle':  degree * a_ts },
        'Str4':  { 'angle':  degree * a_to },
        'Str5':  { 'angle':  degree * a_fivo },
        'Str6':  { 'angle':  degree * a_fivs },
        'Str7':  { 'angle':  degree * a_seto }
      }
    };

    return info;
  };

  
  var data_sets     = { '#demo_2':   inputwhere };

  var info_sets     = {};

  var allInfo="";
  var NumberOfColors=0;
  var ArrayOfColors=[];
  var ArrayOfProducts=[];
  var ArrayOfProductCount=[];
  var ArrayOfSizes=[];
  var biggestGene=0;

  for (var data_set in data_sets) {

    info_sets[data_set]  = get_info(data_set,'conv');

    var func_f = function() {
      var info_set  = info_sets[data_set];

      var func  = function(nodes) {

        prep_data(info_set, nodes);
        setup_mouse(info_set);
        display_plot(info_set);
  
      };
      return func;
    };

    setup_plot(info_sets[data_set]);
    d3.json(data_sets[data_set], func_f() );
  }
