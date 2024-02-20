/**
 * Menu for possible
 * @author   M.Zwaving
 * @license  GPLv3
 * @version  0.0.7
 */
 'use strict'

/**
 * Station object
 */
 class Station
 {
     constructor( wmo, name, min_date, max_date )
     {
         this.wmo = wmo
         this.name = name
         this.min_date = min_date
         this.max_date = max_date
         this.base_src = `./${wmo}`
     }
 }

// Init vars
let jan=1, febr=2, march=3, april=4, mai=5, june=6, july=7, 
    aug=8, sept=9, oct=10,  nov=11,  dec=12, 
    id_menu       = 'dayvalues-menu', 
    id_iframe     = 'iframe-dayvalues-page', 
    id_option_lst = 'options-form-id', 
    id_datepicker = 'date-form-id',
    update_hour   = 901, // No daily updates before 9
    // Init wmo and date 
    wmo_act  = '', 
    date_act = '',
    date_min = '',
    date_max = '',
    lst_stations = [] // Will be filled with stations after page is loaded

// Helper fn
let docid = ( id ) => document.getElementById(id)
let show  = ( id ) => docid(id).style.display = 'inline-block'
let hide  = ( id ) => docid(id).style.display = 'none'
let set_value = ( id, val ) => docid(id).value = val
let get_value = ( id ) => docid(id).value
let set_html = (id, html) => docid(id).innerHTML = html
let set_key = (id, key ) => docid(id).selectedIndex = key
let add_zero  = ( i ) => i < 10 ? `0${i}` : `${i}`
let is_leap_year = ( y ) => y % 100 === 0 ? y % 400 === 0 : y % 4 === 0
let get_days_in_month = ( y, m ) => [ 31, is_leap_year(y) ? 29 : 28, 31, 30, 
                                      31, 30, 31, 31, 30, 31, 30, 31 ][m-1]
                                     
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
            post_get[ decodeURIComponent(tmp[0]) ] = decodeURIComponent(tmp.slice(1).join("").replace("+", " "))
        }
    }
    return post_get
}

let slice_date = ( d ) =>
{
    let str = d.toString(),
        yy = str.slice(0,4),
        mm = str.slice(4,6),
        dd = str.slice(6,8)

    return [ yy, mm, dd ]
}

// Date handling functions
let get_yyyymmdd_now = () =>
{
    let d = new Date(),
        yy = d.getFullYear(),
        mm = add_zero( d.getMonth() + 1 ),
        dd = add_zero( d.getDate() )

    return `${yy}${mm}${dd}`
}

let get_day_before = ( d ) =>
{
    let  l = slice_date( d ),
        yy = parseInt( l[0], 10 ),
        mm = parseInt( l[1], 10 ),
        dd = parseInt( l[2], 10 ) - 1

    if ( dd == 0 )
    {
        mm -= 1  // Last month
        if ( mm == 0 )
        {
            mm = 12
            yy -= 1
        }
        dd = get_days_in_month(yy, mm)
    }

    return `${yy}${add_zero(mm)}${add_zero(dd)}`
}

let get_max_available_date = () =>
{
    let maxx = get_day_before(get_yyyymmdd_now()), // Always yesterday
        d = new Date(), 
        t = d.getHours() * 100 + d.getMinutes()

    // Cannot update before certain time.
    if ( t < update_hour ) 
    {
        maxx = get_day_before(maxx) // Another day back
    }

    return maxx
}

let get_station_from_list_by_wmo = ( wmo ) =>
{
    let station = undefined
    lst_stations.forEach( (el) => { if ( el.wmo == wmo ) station = el } )
    return station
}

let update_min_date_from_list_by_wmo = () =>
{
    lst_stations.forEach( (el) => { if ( el.wmo == wmo_act ) date_min = el.min_date } )
    return date_min
}

let update_max_date_from_list_by_wmo = () =>
{
    lst_stations.forEach( (el) => { if ( el.wmo == wmo_act ) date_max = el.max_date } )
    if (date_max == '-1') date_max = get_max_available_date()
    return date_max
}

let get_min_date_for_menu = () =>
{
    update_min_date_from_list_by_wmo()
    return `${date_min.slice(0,4)}-${date_min.slice(4,6)}-${date_min.slice(6,8)}`
}

let get_max_date_for_menu = () =>
{
    update_max_date_from_list_by_wmo()
    return `${date_max.slice(0,4)}-${date_max.slice(4,6)}-${date_max.slice(6,8)}`
}

let get_month_before = ( d ) =>
{
    let  l = slice_date( d ),
        yy = parseInt( l[0], 10 ),
        mm = parseInt( l[1], 10 ) - 1,
        dd = parseInt( l[2], 10 )

    if ( mm == 0 )
        mm = dec, yy -= 1

    let max = get_days_in_month(yy,mm)

    if ( dd > max )
        dd = max

    return `${yy}${add_zero(mm)}${add_zero(dd)}`
}

let get_year_before = ( d ) =>
{
    let  l = slice_date( d ),
        yy = parseInt( l[0], 10 ) - 1,
        mm = parseInt( l[1], 10 ),
        dd = parseInt( l[2], 10 )

    if ( mm == 2 && dd == 29 )
        dd = 28

    return `${yy}${add_zero(mm)}${add_zero(dd)}`
}

let check_with_max = (d) =>
{
    let act = parseInt(d, 10),
        max = parseInt(get_max_available_date(), 10),
        res = act > max ? max.toString() : d

    return res
}

let correct_dates_range = (date) => 
{
    let i_date_act = parseInt(date, 10),
        i_date_min = parseInt(date_min, 10),
        i_date_max = parseInt(date_max, 10)

    // Out of range chech
    if (i_date_act < i_date_min)
        i_date_act = i_date_min
    else if (i_date_act > i_date_max)
        i_date_act = i_date_max

    return i_date_act.toString()
}

let get_day_next = ( d ) =>
{
    let  l  = slice_date( d ),
        yy  = parseInt(l[0], 10),
        mm  = parseInt(l[1], 10),
        dd  = parseInt(l[2], 10) + 1,  // Next
        max = get_days_in_month(yy, mm)

    if ( dd > max )
        mm += 1, dd = 1

    if ( mm == 13 )
        mm = jan

    let res = check_with_max(`${yy}${add_zero(mm)}${add_zero(dd)}`)
    return res
}

let get_month_next = ( d ) =>
{
    let  l = slice_date( d ),
        yy = parseInt( l[0], 10 ),
        mm = parseInt( l[1], 10 ) + 1,
        dd = parseInt( l[2], 10 )

    if ( mm == 13 )
        mm = jan, yy += 1

    let max = get_days_in_month(yy, mm)

    if ( dd > max )
        dd = max

    let res = check_with_max( `${yy}${add_zero(mm)}${add_zero(dd)}` )
    return res
}

let get_year_next = ( d ) =>
{
    let  l = slice_date( d ),
        yy = parseInt( l[0], 10 ) + 1,
        mm = parseInt( l[1], 10 ),
        dd = parseInt( l[2], 10 )

    if ( mm == febr && dd == 29 )
        dd = 28

    let res = check_with_max( `${yy}${add_zero(mm)}${add_zero(dd)}` )
    return res
}

let set_wmo_option_lst = (wmo) => 
{
    let key = 0
    lst_stations.forEach( ( el, i ) => { if (el.wmo == wmo) key = i } )
    wmo_act = wmo
    set_key(id_option_lst, key)
}

let get_date_picker = () => get_value(id_datepicker).replace(/-/g, '')

let set_datepicker = () =>
{
    let lst = slice_date(date_act),
        yy = lst[0], 
        mm = lst[1], 
        dd = lst[2]

    set_value( id_datepicker, `${yy}-${mm}-${dd}` )
}

let set_min_date = date => docid('date-form-id').setAttribute('min', get_min_date_for_menu()) 
let set_max_date = date => docid('date-form-id').setAttribute('max', get_max_date_for_menu()) 

let set_iframe = () =>
{
    let l  = slice_date( date_act ),
        yy = l[0], 
        mm = l[1], 
        dd = l[2],
        station = get_station_from_list_by_wmo(wmo_act),
        fname = `dayvalues-${wmo_act}-${yy}-${mm}-${dd}`,
        src = `${station.base_src}/${yy}/${mm}/${fname}.html`

    docid(id_iframe).src = src
}

let log = () => 
{
    console.log(`wmo is: ${wmo_act} `)
    console.log(`date is: ${date_act} `)
    console.log(`minimum date is: ${date_min} `)
    console.log(`maximum date is: ${date_max} `)
}

let process_page = () => 
{
    set_iframe()
    log()
}

let start_all_up = () => 
{
    // Startup code
    // Add stations to option list
    let options = ''
    lst_stations.forEach( 
        station => options += `<option value="${station.wmo}"> ${station.wmo} ${station.name} </option>`
    )
    set_html(id_option_lst, options)

    // Overwrite page by url (if there) GET-methode
    let get  = get_object_post_url(), 
        wmo_url  = get['wmo'], 
        date_url = get['date']

    if ( wmo_url !== undefined )
        wmo_act = wmo_url
    if ( date_url !== undefined ) 
        date_act = date_url

    // Set menu based on current wmo_act and date_act
    set_wmo_option_lst(wmo_act)
    set_datepicker(date_act)
    set_min_date() 
    set_max_date()
    set_iframe(wmo_act, date_act)
}

// Start init after document is loaded
window.addEventListener( 'DOMContentLoaded', (event) =>  
{
    
    // btn goto first date
    docid('date-min').addEventListener('click', function(event)
    {
        event.preventDefault()
        date_act = correct_dates_range(update_min_date_from_list_by_wmo())
        set_datepicker()
        process_page()
    })
    // btn goto 1 year before
    docid('year-before').addEventListener('click', function(event) 
    {
        event.preventDefault()
        // Get new date, wmo_act is unchanged
        date_act = correct_dates_range(get_year_before(date_act)) 
        set_datepicker()
        process_page()
    })
    // btn goto 1 month before
    docid('month-before').addEventListener('click', function(event)
    {
        event.preventDefault()
        date_act = correct_dates_range(get_month_before(date_act))
        set_datepicker()
        process_page()
    })
    // btn goto 1 day before
    docid('day-before').addEventListener('click', function(event)
    {
        event.preventDefault()
        date_act = correct_dates_range(get_day_before(date_act))
        set_datepicker()
        process_page()
    })
    // btn goto 1 day next
    docid('day-next').addEventListener('click', function(event)
    {
        event.preventDefault()
        date_act = correct_dates_range(get_day_next(date_act))
        set_datepicker()
        process_page()
    })
    // btn goto 1 month next
    docid('month-next').addEventListener('click', function(event)
    {
        event.preventDefault()
        date_act = correct_dates_range(get_month_next(date_act))
        set_datepicker()
        process_page()
    })
    // btn goto 1 year next
    docid('year-next').addEventListener('click', function(event)
    {
        event.preventDefault()
        date_act = correct_dates_range(get_year_next(date_act))
        set_datepicker()
        process_page()
    })
    // btn goto last dat
    docid('date-max').addEventListener('click', function(event)
    {
        event.preventDefault()
        date_act = correct_dates_range(update_max_date_from_list_by_wmo())
        set_datepicker()
        process_page()
    })

    // Optionlist for new WMO stations
    docid('options-form-id').addEventListener('click', function(event) 
    {
        event.preventDefault()
        wmo_act = get_value(id_option_lst)  // date act is unchanged
        update_min_date_from_list_by_wmo() // Update min for new wmo_act
        update_max_date_from_list_by_wmo() // Update max for new wmo_act
        date_act = correct_dates_range(date_act) // Possible new date
        set_min_date()   // Update min value in date picker
        set_max_date()   // Update max value in date picker
        set_datepicker() // Set (corrected) date in date picker
        process_page()   // Process new page
    })

    // New date from the datepicker
    docid('date-form-id').addEventListener('change', function(event) 
    {
        event.preventDefault()
        // wmo_act unchanged
        date_act = correct_dates_range(get_date_picker())
        set_datepicker() // For a possible correction
        process_page()
    })

    start_all_up()
} )
