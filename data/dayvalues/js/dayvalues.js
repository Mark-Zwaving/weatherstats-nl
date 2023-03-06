/**
 * Menu for possible
 * @author   M.Zwaving
 * @license  MIT-license
 * @version  0.0.4
 */
'use strict';

 // Global setter any menu Set: true for 'yess' and false for 'no'
let activate_menu = true,                // Global activator for all menu's
    activate_menu_dropdown = false,       // Activate dropdown menu (slow)
    activate_menu_days_min_plus = true,  // Activate navigation menu. Next day or day before
    activate_menu_form = true,           // Form menu
    date_act  = '20200101',               // Start date
    wmo_act   = '260',                    // Station
    font_size = '0.7rem',                // Font size menu
    update_hour = 8,                     // What time data can be updated. Needed for max date check

    // Give wmo number of stations to be shown in dropdown menu. Many will make a slow start
    stations_list_dropdown_menu = [
      '260', '280', '235', '310', '380', '286', '391'
    ],

    // Give wmo number of stations to be shown in menu option list
    stations_list_datepicker_menu = [
      '391', '249', '348', '260', '235', '275', '280', '370', '377', '350', '278',
      '356', '330', '279', '251', '283', '277', '270', '269', '380', '273', '286',
      '344', '240', '267', '290', '242', '310', '375', '215', '319', '257', '323'
    ],

    // Name of months in menu
    months = [ 'januari', 'februari', 'march', 'april', 'mai', 'june',
               'july', 'august', 'september', 'october', 'november',
               'december' ],

    // No need to change below
    path_to_root = './',  // ->  {}/wmo/yyyy/mm/
    jan=1, febr=2, march=3, april=4, mai=5, june=6,
    july=7, aug=8, sept=9, oct=10, nov=11, dec=12,
    id_menu = 'dayvalues_menu',
    id_iframe = 'dayvalues_page';

// Helper fn
let docid = ( id ) => document.getElementById(id);
let show  = ( id ) => docid(id).style.display = 'inline-block';
let hide  = ( id ) => docid(id).style.display = 'none';
let set_value = ( id, val ) => docid(id).value = val;
let add_zero  = ( i ) => i < 10 ? `0${i}` : `${i}`;
let is_leap_year = ( y ) => y % 100 === 0 ? y % 400 === 0 : y % 4 === 0;
let get_days_in_month = ( y, m ) => [ 31, is_leap_year(y) ? 29 : 28,
                                      31, 30, 31, 30, 31, 31, 30, 31,
                                      30, 31 ][m-1];

// Source: https://stackoverflow.com/questions/1961069/getting-value-get-or-post-variable-using-javascript
let get_object_post_url = () =>
{
    let post_get = {},
        args = location.search.substr(1).split(/&/)

    for ( let i=0; i<args.length; ++i )
    {
        let tmp = args[i].split(/=/)
        if ( tmp[0] != "" )
        {
            post_get[ decodeURIComponent(tmp[0]) ] = decodeURIComponent(tmp.slice(1).join("").replace("+", " "));
        }
    }
    return post_get
}

let get_yyyymmdd_now = () =>
{
    let d  = new Date(),
        yy = d.getFullYear(),
        mm = d.getMonth() + 1,
        dd = d.getDate();

    return `${yy}${add_zero(mm)}${add_zero(dd)}`;
}

let split_date = ( d ) =>
{
    let yy = d.slice(0, 4),
        mm = d.slice(4, 6),
        dd = d.slice(6, 8);

    return [ yy, mm, dd ];
}

let get_day_before = ( d ) =>
{
    let  l = split_date( d ),
        yy = parseInt( l[0], 10 ),
        mm = parseInt( l[1], 10 ),
        dd = parseInt( l[2], 10 ) - 1;

    if ( dd == 0 )
    {
        mm -= 1;  // Last month
        if ( mm == 0 )
        {
            mm = 12
            yy -= 1
        }
        dd = get_days_in_month(yy, mm);
    }

    return `${yy}${add_zero(mm)}${add_zero(dd)}`;
}

let get_max_available_date = () =>
{
    let now = get_yyyymmdd_now(),
        max = get_day_before(now),
        d   = new Date(),
        hh  = d.getHours();

    // Cannot update before certain time.
    if ( hh < update_hour )
      	max = get_day_before(max);

    return max;
}

let get_max_date_for_menu = () =>
{
    let max = get_max_available_date(),
          l = split_date(max),
         yy = l[0],
         mm = l[1],
         dd = l[2];

    return `${yy}-${mm}-${dd}`;
}

let get_month_before = ( d ) =>
{
    let  l = split_date( d ),
        yy = parseInt( l[0], 10 ),
        mm = parseInt( l[1], 10 ) - 1,
        dd = parseInt( l[2], 10 );

    if ( mm == 0 )
        mm = dec, yy -= 1;

    let max = get_days_in_month(yy,mm);

    if ( dd > max )
        dd = max

    return `${yy}${add_zero(mm)}${add_zero(dd)}`;
}

let get_year_before = ( d ) =>
{
    let  l = split_date( d ),
        yy = parseInt( l[0], 10 ) - 1,
        mm = parseInt( l[1], 10 ),
        dd = parseInt( l[2], 10 );

    if ( mm == 2 && dd == 29 )
        dd = 28;

    return `${yy}${add_zero(mm)}${add_zero(dd)}`;
}

let check_with_max = (d) =>
{
    let act = parseInt(d, 10),
        max = parseInt(get_max_available_date(), 10),
        res = act > max ? max.toString() : d;

    return res;
}

let get_day_next = ( d ) =>
{
    let  l  = split_date( d ),
        yy  = parseInt(l[0], 10),
        mm  = parseInt(l[1], 10),
        dd  = parseInt(l[2], 10) + 1,  // Next
        max = get_days_in_month(yy, mm);

    if ( dd > max )
        mm += 1, dd = 1;

    if ( mm == 13 )
        mm = jan;

    let res = check_with_max( `${yy}${add_zero(mm)}${add_zero(dd)}` );
    return res;
}

let get_month_next = ( d ) =>
{
    let  l = split_date( d ),
        yy = parseInt( l[0], 10 ),
        mm = parseInt( l[1], 10 ) + 1,
        dd = parseInt( l[2], 10 );

    if ( mm == 13 )
        mm = jan, yy += 1;

    let max = get_days_in_month(yy, mm);

    if ( dd > max )
        dd = max

    let res = check_with_max( `${yy}${add_zero(mm)}${add_zero(dd)}` );
    return res;
}

let get_year_next = ( d ) =>
{
    let  l = split_date( d ),
        yy = parseInt( l[0], 10 ) + 1,
        mm = parseInt( l[1], 10 ),
        dd = parseInt( l[2], 10 );

    if ( mm == febr && dd == 29 )
        dd = 28;

    let res = check_with_max( `${yy}${add_zero(mm)}${add_zero(dd)}` );
    return res;
}

/**
 * Station object
 */
class Station
{
    constructor( wmo, name, sdate )
    {
        this.wmo = wmo;
        this.name = name;
        this.sdate = sdate;             // Start date of data
        this.edate = get_day_before(get_yyyymmdd_now()); // Max date of data
        this.base_url = `./${wmo}`;
        this.base_file = `dayvalues-${wmo}`;
    }
}

let station_list = [
    new Station('391', 'Arcen', '19900704'),
    new Station('249', 'Berkhout', '19510101'),
    new Station('348', 'Cabauw Mast', '19510101'),
    new Station('260', 'De Bilt', '19010101'),
    new Station('235', 'De Kooy', '19060101'),
    new Station('275', 'Deelen', '19010101'),
    new Station('280', 'Eelde', '19060301'),
    new Station('370', 'Eindhoven', '19010101'),
    new Station('377', 'Ell', '19010101'),
    new Station('350', 'Gilze-Rijen', '19010101'),
    new Station('278', 'Heino', '19010101'),
    new Station('356', 'Herwijnen', '19010101'),
    new Station('330', 'Hoek van Holland', '19010101'),
    new Station('279', 'Hoogeveen', '19010101'),
    new Station('251', 'Hoorn Terschelling', '19010101'),
    new Station('283', 'Hupsel', '19010101'),
    new Station('277', 'Lauwersoog', '19010101'),
    new Station('270', 'Leeuwarden', '19010101'),
    new Station('269', 'Lelystad', '19010101'),
    new Station('380', 'Maastricht', '19060101'),
    new Station('273', 'Marknesse', '19010101'),
    new Station('286', 'Nieuw Beerta', '19900219'),
    new Station('344', 'Rotterdam', '19010101'),
    new Station('240', 'Schiphol', '19010101'),
    new Station('267', 'Stavoren', '19010101'),
    new Station('290', 'Twenthe', '19010101'),
    new Station('242', 'Vlieland', '19010101'),
    new Station('310', 'Vlissingen', '19060101'),
    new Station('375', 'Volkel', '19010101'),
    new Station('215', 'Voorschoten', '19010101'),
    new Station('319', 'Westdorpe', '19010101'),
    new Station('257', 'Wijk aan Zee', '19010101'),
    new Station('323', 'Wilhelminadorp', '19010101')
];

let get_station_from_list_by_wmo = ( wmo ) =>
{
    let ndx = 0, station = false;
    while ( ndx < station_list.length )
    {
        station = station_list[ndx];
        if ( station.wmo == wmo )
            break;
        ndx++;
    }
    return station;
}

let open_url = ( url ) =>
{
    let i_act = parseInt(date_act, 10),
        i_max = parseInt(get_day_before(get_yyyymmdd_now()), 10);

    date_act = (i_act > i_max ? i_max : i_act).toString()

    set_date_picker()
    set_wmo_optionlist()

    console.log(`Open url ${url}`);
    docid(id_iframe).src = url
}

let make_url = (wmo, date) =>
{
    let       l = split_date( date ),
             yy = l[0], mm = l[1], dd = l[2],
        station = get_station_from_list_by_wmo(wmo),
           name = `${station.base_file}-${yy}-${mm}-${dd}.html`,
           url  = `${station.base_url}/${yy}/${mm}/${name}`;

    return url
}

let onclick_dropdown_menu = ( wmo, date ) =>
{
    let url = make_url(wmo, date);

    // Update globals
    date_act = date;
    wmo_act  = wmo;

    open_url(url);  // Open the url
}

let onclick_go_btn = () =>
{
    let  wmo = document.getElementById('station_form_id').value,
        date = document.getElementById('date_form_id').value,
           l = date.split('-'),
           y = parseInt(l[0], 10),
           m = add_zero(parseInt(l[1],10)),
           d = add_zero(parseInt(l[2],10)),
         ymd = `${y}${m}${d}`,
         url = make_url( wmo, ymd );

    // Update globals
    date_act = ymd;
    wmo_act  = wmo;

    open_url(url);  // Open the url
}

let onclick_day_before = () =>
{
    date_act = get_day_before( date_act );
    let url = make_url(wmo_act, date_act);
    open_url(url);  // Open the url
}

let onclick_month_before = () =>
{
    date_act = get_month_before( date_act );
    let url = make_url(wmo_act, date_act);
    open_url(url);  // Open the url
}

let onclick_year_before = () =>
{
    date_act = get_year_before( date_act );
    let url = make_url(wmo_act, date_act);
    open_url(url);  // Open the url
}

let onclick_day_next = () =>
{
    date_act = get_day_next( date_act );
    let url = make_url(wmo_act, date_act);
    open_url(url);  // Open the url
}

let onclick_month_next = () =>
{
    date_act = get_month_next( date_act );
    let url = make_url(wmo_act, date_act);
    open_url(url);  // Open the url
}

let onclick_year_next = () =>
{
    date_act = get_year_next( date_act );
    let url = make_url(wmo_act, date_act);
    open_url(url);  // Open the url
}

let show_init_station = () =>
{
    let url = make_url(wmo_act, date_act);
    open_url(url);
}

function set_date_picker()
{
    let id = 'date_form_id',
        date = split_date(date_act).join('-')

    set_value( id, date ) // Set date
}

function get_index_act_station()
{
    let key = 0;
    station_list.forEach( ( item, i ) =>
    {
        let wmo = item.wmo
        console.log(wmo + ' | ' + wmo_act)

        if (wmo == wmo_act)
        {
            key = i + 1
        }
    })

    return key
}

function set_wmo_optionlist()
{
    let id = 'station_form_id'

    docid(id).selectedIndex = get_index_act_station()
}

let html_menu_dropdown = () =>
{
      let html = `<button class="navbar-toggler" type="button" data-toggle="collapse"
                   data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown"
                   aria-expanded="false" aria-label="Toggle navigation">
                   <span class="navbar-toggler-icon"></span></button>
                   <div class="collapse navbar-collapse" id="navbarNavDropdown">`;

      stations_list_dropdown_menu.forEach( ( wmo ) =>
      {
          let station = get_station_from_list_by_wmo ( wmo );
          html += `<ul class="navbar-nav">
                   <li class="nav-item dropdown">
                   <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink"
                      data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> ${station.name} </a>
                   <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">`;

          let l_s = split_date(station.sdate),
              i_y = parseInt( l_s[0], 10 ),
              l_e = split_date(station.edate),
              i_e = parseInt( l_e[0], 10 ),
              i_date_e = parseInt(station.edate, 10);

          while ( i_y <= i_e )
          {
              // All Months
              html += `<li class="dropdown-submenu">
                         <a class="dropdown-item dropdown-toggle" href="#"
                            style="font-size:${font_size};"> ${i_y} </a>
                         <ul class="dropdown-menu">`;
              // Months
              let i_m = 1;
              while ( i_m <= 12 )
              {
                  // Days
                  html += `<li class="dropdown-submenu">
                             <a class="dropdown-item dropdown-toggle" href="#"
                                style="font-size:${font_size};"> ${months[i_m-1]} </a>
                                <ul class="dropdown-menu">`;
                  let i_d   = 1,
                      i_max = get_days_in_month(i_y, i_m),
                      mm = add_zero(i_m);

                  while ( i_d <= i_max )
                  {
                      let dd = add_zero(i_d),
                          ymd = `${i_y}${mm}${dd}`;

                      html += `<li><a class="dropdown-item" href="#"
                                      onclick="onclick_dropdown_menu('${station.wmo}','${ymd}'); return false;"
                                      style="font-size:${font_size};"> ${dd} </a>
                                      </li>`;

                      let i_date_s = parseInt(get_day_next(ymd), 10);
                      if ( i_date_s > i_date_e )
                          i_y = i_e, i_d = i_max, i_m = 12  // Set all to max

                      ++i_d;
                  }
                  html += '</ul></li>'; // dd
                  ++i_m;
              }
              html += '</ul></li>';  // mm
              ++i_y;
          }
          html += '</ul></li></ul>';  // stations
      } );

      html += '</div>';

      return html;
}

let html_days_plus_min = () =>
{
    let l = [ ['onclick_year_before', 'fa fa-fast-backward'],
              ['onclick_month_before', 'fa fa-step-backward'],
              ['onclick_day_before', 'fa fa-caret-left'],
              ['onclick_day_next', 'fa fa-caret-right'],
              ['onclick_month_next', 'fa fa-step-forward'],
              ['onclick_year_next', 'fa fa-fast-forward'] ];

    let html = '<div class="form-group m-1">';
    l.forEach( (el) =>
    {
        let fn = el[0], icon = el[1];
        html += `<button class="btn btn-info btn-sm m-1" style="font-size:${font_size};"
                  onclick="${fn}(); return false;"><i class="${icon}" aria-hidden="true"></i>
                  </button>`;
    } );
    html += '</div>';

    return html;
}

let html_menu_datepicker = () =>
{
    let html = `<form class="form-inline m-1" style="font-size:${font_size};">
                <div class="form-group m-1"> <select id="station_form_id"
                 class="form-control custom-select" style="font-size:${font_size};">
                 <option selected> Select a station </option>`;

    stations_list_datepicker_menu.forEach( (wmo) =>
    {
        let station = get_station_from_list_by_wmo ( wmo )
        html += `<option value="${station.wmo}"> ${station.wmo} ${station.name} </option>`;
    } );

    html += `</select>
     </div>
        <div class="form-group m-1">
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text" id="inputGroupPrepend3">
                <i class="fa fa-calendar fa-xs" aria-hidden="true"></i>
              </span>
            </div>
            <input type="date" id="date_form_id" class="form-control form-control-sm"
                   min="1906-01-01" max="${get_max_date_for_menu()}"
                   aria-describedby="inputGroupPrepend3" style="font-size:${font_size};" required>
          </div>
        </div>
        <div class="form-group m-1">
          <button class="btn btn-info btn-sm" style="font-size:${font_size};"
                  onclick="onclick_go_btn(); return false;">
                    <i class="fa fa-search" aria-hidden="true"></i>
          </button>
        </div>
      </div>
    </form>`;

    return html;
}

let add_menus_to_page = () =>
{
    console.log('The html page has loaded');
    if ( activate_menu )
    {
        console.log('Activate menu');
        let html = `<nav class="navbar navbar-expand-md navbar-light bg-light"
                         style="font-size:${font_size};">`;

        html += '<div class="row container-fluid">';
        if (activate_menu_dropdown)
        {
            console.log('Start make dropdown menu');
            html += '<div class="col">';
            html += html_menu_dropdown();
            html += '</div>';
            console.log('End make dropdown menu');
        }

        if ( activate_menu_days_min_plus )
        {
            console.log('Start make days plus and min menu');
            html += '<div class="col text-center">';
            html += html_days_plus_min();
            html += '</div>';
            console.log('End make days plus and min menu');
        }

        if (activate_menu_form)
        {
            console.log('Start make form menu');
            html += '<div class="col text-center">';
            html += html_menu_datepicker();
            html += '</div>';
            console.log('End make form menu');
        }
        html += '</div>';

        html +=  '</nav>';

        console.log('Start putting menu on screen');
        docid(id_menu).innerHTML = html //.replace( /\s+/g, ' ' );
        console.log('End putting menu on screen');
    }
    else
    {
          docid(id_menu).innerHTML = ' ' // No menu
    }

    // show_init_station();
};

// Start main fn
add_menus_to_page();
