/**
 * Functions for sorting html table columns
 *
 * @author   M.Zwaving
 * @license  MIT-license
 * @version  0.1.1
 */

'use strict';

let table_tbody      =  'table#stats>tbody',
    table_stats_sel  =  'table#stats>tbody>tr',  // Locations of the tr with data
    table_popup_sel  =  'table#stats>tbody>tr>td>table.popup', // Popup table
    css_click_cell   =  'cursor: cell;',  // Extra css for click cell
    separator        =  '<span></span>',  // Default separator in html files
    no_data_given    =  '.', // Default dummy value in weatherstats
    empthy           =   '', // Fault value 
    num_max          =  Number.MAX_VALUE,  // Max possible value
    num_min          =  Number.MIN_VALUE,  // Min possible value
    descending       =  '+',   // Identifier sort direction: large to small
    ascending        =  '-',   // Identifier sort direction: small to high
    sort_num         =  'num', // Identifier sort num-based
    sort_txt         =  'txt', // Identifier sort txt-based
    row_nr           =  2,     // Row tr num for click to sort
    // Reg expression for grepping a float number from a td cell.
    // Result float is used for numeric sorting in a td cell.
    // Update here reg expression for extracting floats, if needed
    reg_float        = /-?\d*\.\d+|\d+/,
    //  TODO plus min goes wrong
    //  /-?(\d*\.\d+|\d+),?/
    //  /-?\d+(?:.\d+)?/
    //  /^[-+]?[0-9]*\.?[0-9]+$/

    ////////////////////////////////////////////////////////////////////////////
    // Grep a float from a string. Needed for correct sorting
    grep_float = el => {
        let fl = 0.0
        if ( el == no_data_given || el == empthy )
        {
            // This value will always be most extreme
            fl = col_titles.dir == ascending ? num_min : num_max;
        }
        else 
        { 
            try {
                // let multi = el[0] == '-' ? -1.0 : 1.0
                // Replace chars and remove whitespace
                el = el.replace( /|A-Z|a-z|°|%|\/|cm2|^\s+|\s+$|\s+(?=\s)|/gi, '' )
                if ( el == '0.0' || el == '0' )
                    fl = 0.000001 // Zero goes to false? Oke, make it very close to 0
                else
                {
                    fl = parseFloat( el.match( reg_float ), 10 ); // Match a float digit
                    // fl *= multi
                }
            } 
            catch (error) { 
                console.log(error)
            }
            console.log(fl)
        }
        return fl;
    },

    // Function updates the sort direction for a given object
    reverse_sort_dir = obj => {
        obj.dir = obj.dir == descending ? ascending : descending;
    },

    // Function gets a DOM object with all the rows in the selected table
    read_dom = selector => {
        // Do not add the tr from the popup table
        return document.querySelectorAll(selector);
    },

    // Function deletes a DOM object with all the rows in the selected table
    delete_dom = selector => {
        let nodelist = document.querySelectorAll(selector);
        nodelist.forEach((nodelist, node) => {
            while (node.hasChildNodes())
                node.removeChild(node.lastChild);
        });
    },

    // Function sets the values of a matrix (2d array) to text
    txt_matrix = matrix => {
        let txt = '\n[\n';
        matrix.forEach( ( row, i ) => {
            txt += ' [ ';
            row.forEach( ( item, i ) => txt += `${item}, ` );
            txt += ' ]\n';
        } );
        txt += '];\n';

        return txt;
    },

    // Function reads al the data from an tr DOM object into an 2d array/matrix
    read_matrix = tr => {
        let matrix = [];
        tr.forEach( (row, i) => {
            let tds = [];
            row.querySelectorAll('.val').forEach( (val, i) => {   // Get values
                 let td = val.innerHTML.replace(/\s+/g,'') // Remove \s
                 tds.push(td);
            } );
            matrix.push(tds);
        } );

        return matrix;
    },

    // Function reads all the column values from the weather object into a list
    list_col_from_matrix = ( matrix, obj ) => {
        let cols = [], ndx = obj.col;
        matrix.forEach( (row, i) => cols.push(row[ndx]) );

        return cols;
    },

    // Function gets a maximum value and his key from a list
    max_from_list = l => {
        let max = num_min, key = 0;
        l.forEach( (item, i) => {
            if ( item != no_data_given )
                if (item > max)
                    max = item, key = i;
        } );

        return { val: max, key: key };
    },

    // Function gets a minimum value and his key from a list
    min_from_list = l => {
        let min = num_max, key = 0;
        l.forEach( (item, i) => {
            if ( item != no_data_given )
                if (item < min)
                    min = item, key = i;
        } );

        return { val: min, key: key };
    },

    // Function gets the numeric sorted key list with values
    num_sort_keys_col = (col_list, obj) => {

        let len = col_list.length, keys = [];

         // Replace/remove all non-numeric values in col_list
        col_list.forEach( (item, i) => col_list[i] = grep_float(item) );

        while ( --len !== -1 )
        { 
            let extreme = max_from_list( col_list ); 
            col_list.splice( extreme.key, 1, num_min );  // Replace with a contradictio extreme value
            keys.push( extreme.key );  // Add max key row to keys
        }

        if ( obj.dir == ascending ) 
            keys.reverse()

        return keys; // Sorted keys
    },

    // Function gets the txt sorted key list with values
    txt_sort_keys_col = (col_list, obj) => {
        let len = col_list.length, txt_keys = [], keys = [];

        // Make new array txt_keys with the text and their keys
        col_list.forEach(
            (item, i) => txt_keys.push({ txt : item, key : i })
        );

        // Sort text only
        txt_keys.sort( (a, b) => {
            a = a.txt.toLowerCase();
            b = b.txt.toLowerCase();

            return a == b ? 0 : a < b ? -1 : 1;
        } );

        // Make keys only list
        while ( --len !== -1 ) keys.push( txt_keys[len].key );

        if ( obj.dir == ascending )
            keys.reverse()

        return keys;
    },

    // Function makes the sorted html (tr rows) based on the list with sorted keys.
    // The sorted keys sort the TR Dom object.
    html_sorted_list = (tr, sort_keys) => {

        let html = '', ndx = 0;  // Make new html tr rows based on sorted keys
        sort_keys.forEach(
            el => html += `<tr>${tr.item(el).innerHTML}</tr>`
        );

        return html;
    },

    // Function called after clicked on a table column title. Start sorting the clicked column.
    event_click_num_sort = (obj) => {
        let tr        =  read_dom( table_stats_sel ),
            matrix    =  read_matrix( tr ),   // Read all values into matrix list
            col_list  =  list_col_from_matrix( matrix, obj );  // Get values col in list

        // Get sorted keys list
        let sort_keys = [];
        if ( obj.type == sort_num )
            sort_keys = num_sort_keys_col( col_list, obj );
        else if ( obj.type == sort_txt )
            sort_keys = txt_sort_keys_col( col_list, obj );

        let html = html_sorted_list( tr, sort_keys );  // Get html tr sorted
        document.querySelector( table_tbody ).innerHTML = html;  // Write sorted tr to table/tbody
        reverse_sort_dir( obj );  // Update sort direction for next time
    },

    // Function adds/attaches the click events to the columns in the table
    add_events_to_table = () => {
        // Add events to table titles
        for ( var x in col_titles )
            col_titles[x].doc.addEventListener(
                'click', (
                  ( obj ) => () => event_click_num_sort( obj )
                ) ( col_titles[x] ),
                false
            );  
    },

    // Function adds css to the clickable column titles in the table
    add_css_to_table_titles = () => {
        // Add events to table titles
        for ( var x in col_titles )
            col_titles[x].doc.style = css_click_cell;
    };

//  After loading the page, add all events and css
window.onload = (e) => {
    console.log('JS col sort loading...');
    add_events_to_table();
    add_css_to_table_titles(); // Add cursor to the cells
    console.log('JS loaded !');
};
