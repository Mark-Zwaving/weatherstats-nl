/**
 * Menu for possible
 * @author   M.Zwaving
 * @license  MIT-license
 * @version  0.0.5
 */
 'use strict';

/**
 * Station object
 */
 class Station
 {
     constructor( wmo, name )
     {
         this.wmo = wmo;
         this.name = name;
         this.base_src = `./${wmo}`;
     }
 }


// Init vars
let jan=1, febr=2, march=3, april=4, mai=5, june=6, july=7, 
    aug=8, sept=9, oct=10,  nov=11,  dec=12, 
    id_menu = 'dayvalues-menu', 
    id_iframe = 'iframe-dayvalues-page', 
    id_option_lst = 'options-form-id', 
    id_datepicker = 'date-form-id',
    update_hour = 901, // No daily updates before 9
    // Make global 
    wmo_act = '', 
    date_act = ''; 


// Helper fn
let docid = ( id ) => 
{
    return document.getElementById(id);
}

let show  = ( id ) => 
{
    docid(id).style.display = 'inline-block';
}

let hide  = ( id ) => 
{
    docid(id).style.display = 'none';
}

let set_value = ( id, val ) => 
{
    docid(id).value = val;
}

let get_value = ( id ) =>
{
    return docid(id).value;
}

let set_html = (id, html) =>
{
    docid(id).innerHTML = html;
}

let set_key = (id, key ) =>
{
    docid(id).selectedIndex = key
}

let add_zero  = ( i ) =>
{
    return i < 10 ? `0${i}` : `${i}`;
}

let is_leap_year = ( y ) => 
{
    return y % 100 === 0 ? y % 400 === 0 : y % 4 === 0;
}

let get_days_in_month = ( y, m ) => 
{
    return [ 31, is_leap_year(y) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ][m-1]
}

let get_station_from_list_by_wmo = ( wmo ) =>
{
    let ndx = 0, station = false;
    while ( ndx < lst_stations.length )
    {
        station = lst_stations[ndx];
        if ( station.wmo == wmo )
            break;
        ndx++;
    }
    return station;
}

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

// Date handling functions
let get_yyyymmdd_now = () =>
{
    let d = new Date(),
        yy = d.getFullYear(),
        mm = add_zero(d.getMonth() + 1),
        dd = add_zero(d.getDate());

    return `${yy}${mm}${dd}`;
}

let split_date = ( d ) =>
{
    let str = d.toString(),
        yy = str.slice(0,4),
        mm = str.slice(4,6),
        dd = str.slice(6,8);

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
    let max = get_day_before(get_yyyymmdd_now()), // Always yesterday
        d = new Date(), 
        tnow = d.getHours() * 100 + d.getMinutes()

    // Cannot update before certain time.
    if ( tnow < update_hour ) 
    {
        max = get_day_before(max) // Another day back
    }

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


// Setters
let set_wmo_option_lst = (wmo) => 
{
    let key = 0
    lst_stations.forEach( ( item, i ) => { if (item.wmo == wmo) key = i } )
    wmo_act = wmo
    set_key(id_option_lst, key)
}

function set_datepicker(date)
{
    let lst = split_date(date),
        yy = lst[0], mm = lst[1], dd = lst[2],
        dp = `${yy}-${mm}-${dd}`

    date_act = date
    wmo_act = get_wmo_option()

    set_value(id_datepicker, dp)
}

let set_iframe = ( wmo, date ) =>
{
    let l  = split_date( date ),
        yy = l[0], 
        mm = l[1], 
        dd = l[2],
        station = get_station_from_list_by_wmo(wmo),
        fname = `dayvalues-${wmo}-${yy}-${mm}-${dd}`,
        src = `${station.base_src}/${yy}/${mm}/${fname}.html`;

    docid(id_iframe).src = src
}


// Gettters
let get_datepicker = () => 
{
    let date = get_value(id_datepicker),
        lst = date.split('-'),
        yy = lst[0], 
        mm = lst[1], 
        dd = lst[2];

    date_act = `${yy}${mm}${dd}`
    return date_act
}

let get_wmo_option = () => 
{
    return get_value(id_option_lst)
}

let onchange_wmo_or_date = () => 
{
    wmo_act = get_wmo_option()
    date_act = get_datepicker()
    set_iframe(wmo_act, date_act)
}

// Start init after document is loaded
window.addEventListener( 'DOMContentLoaded', (event) =>  
{
    // Add events to btn
    docid('year-before').addEventListener('click', function(event) 
    {
        event.preventDefault()
        set_datepicker( get_year_before(get_datepicker()) )
        onchange_wmo_or_date()
    });

    docid('month-before').addEventListener('click', function(event)
    {
        event.preventDefault()
        set_datepicker( get_month_before(get_datepicker()) )
        onchange_wmo_or_date()
    });

    docid('day-before').addEventListener('click', function(event)
    {
        event.preventDefault()
        set_datepicker( get_day_before(get_datepicker()) )
        onchange_wmo_or_date() 
    });

    docid('day-next').addEventListener('click', function(event)
    {
        event.preventDefault()
        set_datepicker( get_day_next(get_datepicker()) )
        onchange_wmo_or_date()
    });

    docid('month-next').addEventListener('click', function(event)
    {
        event.preventDefault()
        set_datepicker( get_month_next(get_datepicker()) )
        onchange_wmo_or_date()
    });

    docid('year-next').addEventListener('click', function(event)
    {
        event.preventDefault()
        set_datepicker( get_year_next(get_datepicker()) )
        onchange_wmo_or_date()
    });

    // Add event to option lst
    docid('options-form-id').addEventListener('click', function(event) 
    {
        event.preventDefault()
        onchange_wmo_or_date()

    });

    // Add event to datepicker
    docid('date-form-id').addEventListener('change', function(event) 
    {
        event.preventDefault()
        onchange_wmo_or_date()
    });

    // Set max date
    docid('date-form-id').setAttribute("max", (function()
    {
        let lst = split_date(get_max_date_for_menu()),
            yy = lst[0], mm = lst[1], dd = lst[2];

        return `${yy}-${mm}-${dd}`
    })() );  


    // Startup code
    // Add stations to option list
    let options = ''
    lst_stations.forEach( 
        station => options += `<option value="${station.wmo}"> ${station.wmo} ${station.name} </option>`
    )
    set_html(id_option_lst, options)

    // Overwrite page by url (if there)
    let get  = get_object_post_url(), wmo  = get['wmo'], date = get['date']
    if ( wmo !== undefined && date !== undefined )
    {
        wmo_act = wmo
        date_act = date
    }
    else
    {
        date_act = get_max_available_date()
    }

    set_wmo_option_lst(wmo_act)
    set_datepicker(date_act)
    set_iframe(wmo_act, date_act)
    
} );
