# -*- coding: utf-8 -*-
'''Library contains lsts with possible cell option.
   TODO check input from user based on available cell options'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.2.2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

# Available statistics entities calculations
lst_entities_statistics = [ 
    'ave_fhvec', 'ave_fg', 'ave_fhx', 'ave_fhn', 'ave_fxx', 'ave_tg', 
    'ave_tn', 'ave_tx', 'ave_t10n', 'ave_sq', 'ave_sp', 'ave_q', 'ave_dr', 
    'ave_rh', 'ave_rhx', 'ave_pg', 'ave_px', 'ave_pn', 'ave_vvn', 'ave_vvx', 
    'ave_ng', 'ave_ug', 'ave_ux', 'ave_un', 'ave_ev24', 'max_fhvec', 
    'max_fg', 'max_fhx', 'max_fhn', 'max_fxx', 'max_tg', 'max_tn', 'max_tx', 
    'max_t10n', 'max_sq', 'max_sp', 'max_q', 'max_dr', 'max_rh', 'max_rhx', 
    'max_pg', 'max_px', 'max_pn', 'max_vvn', 'max_vvx', 'max_ng', 'max_ug', 
    'max_ux', 'max_un', 'max_ev24', 'min_fhvec', 'min_fg', 'min_fhx', 
    'min_fhn', 'min_fxx', 'min_tg', 'min_tn', 'min_tx', 'min_t10n', 
    'min_sq', 'min_sp', 'min_q', 'min_dr', 'min_rh', 'min_rhx', 'min_pg', 
    'min_px', 'min_pn', 'min_vvn', 'min_vvx', 'min_ng', 'min_ug', 'min_ux', 
    'min_un', 'min_ev24', 
    
    'clima_fhvec', 'clima_fg', 'clima_fhx', 'clima_fhn', 
    'clima_fxx', 'clima_tg', 'clima_tn', 'clima_tx', 'clima_t10n', 'clima_sq', 
    'clima_sp', 'clima_q', 'clima_dr', 'clima_rh', 'clima_rhx', 'clima_pg', 
    'clima_px', 'clima_pn', 'clima_vvn', 'clima_vvx', 'clima_ng', 'clima_ug', 
    'clima_ux', 'clima_un', 'clima_ev24'
]

# Available calculations
lst_indices = [
    'ndx_hellman', 'ndx_heat-ndx', 'ndx_frostsum', 'ndx_ijnsen'
]

# Available counters
lst_counters = [
    'cnt_fhvec_gt_NUM', 'cnt_fhvec_>_NUM', 'cnt_fhvec_ge_NUM', 'cnt_fhvec_>=_NUM', 'cnt_fhvec_≥_NUM', 
    'cnt_fhvec_gte_NUM', 'cnt_fhvec_lt_NUM', 'cnt_fhvec_<_NUM', 'cnt_fhvec_le_NUM', 'cnt_fhvec_<=_NUM', 
    'cnt_fhvec_≤_NUM', 'cnt_fhvec_lte_NUM', 'cnt_fhvec_eq_NUM', 'cnt_fhvec_==_NUM', 'cnt_fhvec_equal_NUM', 
    'cnt_fhvec_ne_NUM', 'cnt_fhvec_!=_NUM', 'cnt_fhvec_<>_NUM', 'cnt_fhvec_not_NUM', 'cnt_fg_gt_NUM', 
    'cnt_fg_>_NUM', 'cnt_fg_ge_NUM', 'cnt_fg_>=_NUM', 'cnt_fg_≥_NUM', 'cnt_fg_gte_NUM', 'cnt_fg_lt_NUM', 
    'cnt_fg_<_NUM', 'cnt_fg_le_NUM', 'cnt_fg_<=_NUM', 'cnt_fg_≤_NUM', 'cnt_fg_lte_NUM', 'cnt_fg_eq_NUM', 
    'cnt_fg_==_NUM', 'cnt_fg_equal_NUM', 'cnt_fg_ne_NUM', 'cnt_fg_!=_NUM', 'cnt_fg_<>_NUM', 'cnt_fg_not_NUM', 
    'cnt_fhx_gt_NUM', 'cnt_fhx_>_NUM', 'cnt_fhx_ge_NUM', 'cnt_fhx_>=_NUM', 'cnt_fhx_≥_NUM', 'cnt_fhx_gte_NUM', 
    'cnt_fhx_lt_NUM', 'cnt_fhx_<_NUM', 'cnt_fhx_le_NUM', 'cnt_fhx_<=_NUM', 'cnt_fhx_≤_NUM', 'cnt_fhx_lte_NUM', 
    'cnt_fhx_eq_NUM', 'cnt_fhx_==_NUM', 'cnt_fhx_equal_NUM', 'cnt_fhx_ne_NUM', 'cnt_fhx_!=_NUM', 'cnt_fhx_<>_NUM', 
    'cnt_fhx_not_NUM', 'cnt_fhn_gt_NUM', 'cnt_fhn_>_NUM', 'cnt_fhn_ge_NUM', 'cnt_fhn_>=_NUM', 'cnt_fhn_≥_NUM', 
    'cnt_fhn_gte_NUM', 'cnt_fhn_lt_NUM', 'cnt_fhn_<_NUM', 'cnt_fhn_le_NUM', 'cnt_fhn_<=_NUM', 'cnt_fhn_≤_NUM', 
    'cnt_fhn_lte_NUM', 'cnt_fhn_eq_NUM', 'cnt_fhn_==_NUM', 'cnt_fhn_equal_NUM', 'cnt_fhn_ne_NUM', 'cnt_fhn_!=_NUM', 
    'cnt_fhn_<>_NUM', 'cnt_fhn_not_NUM', 'cnt_fxx_gt_NUM', 'cnt_fxx_>_NUM', 'cnt_fxx_ge_NUM', 'cnt_fxx_>=_NUM', 
    'cnt_fxx_≥_NUM', 'cnt_fxx_gte_NUM', 'cnt_fxx_lt_NUM', 'cnt_fxx_<_NUM', 'cnt_fxx_le_NUM', 'cnt_fxx_<=_NUM', 
    'cnt_fxx_≤_NUM', 'cnt_fxx_lte_NUM', 'cnt_fxx_eq_NUM', 'cnt_fxx_==_NUM', 'cnt_fxx_equal_NUM', 'cnt_fxx_ne_NUM', 
    'cnt_fxx_!=_NUM', 'cnt_fxx_<>_NUM', 'cnt_fxx_not_NUM', 'cnt_tg_gt_NUM', 'cnt_tg_>_NUM', 'cnt_tg_ge_NUM', 
    'cnt_tg_>=_NUM', 'cnt_tg_≥_NUM', 'cnt_tg_gte_NUM', 'cnt_tg_lt_NUM', 'cnt_tg_<_NUM', 'cnt_tg_le_NUM', 
    'cnt_tg_<=_NUM', 'cnt_tg_≤_NUM', 'cnt_tg_lte_NUM', 'cnt_tg_eq_NUM', 'cnt_tg_==_NUM', 'cnt_tg_equal_NUM', 
    'cnt_tg_ne_NUM', 'cnt_tg_!=_NUM', 'cnt_tg_<>_NUM', 'cnt_tg_not_NUM', 'cnt_tn_gt_NUM', 'cnt_tn_>_NUM', 
    'cnt_tn_ge_NUM', 'cnt_tn_>=_NUM', 'cnt_tn_≥_NUM', 'cnt_tn_gte_NUM', 'cnt_tn_lt_NUM', 'cnt_tn_<_NUM', 
    'cnt_tn_le_NUM', 'cnt_tn_<=_NUM', 'cnt_tn_≤_NUM', 'cnt_tn_lte_NUM', 'cnt_tn_eq_NUM', 'cnt_tn_==_NUM', 
    'cnt_tn_equal_NUM', 'cnt_tn_ne_NUM', 'cnt_tn_!=_NUM', 'cnt_tn_<>_NUM', 'cnt_tn_not_NUM', 'cnt_tx_gt_NUM', 
    'cnt_tx_>_NUM', 'cnt_tx_ge_NUM', 'cnt_tx_>=_NUM', 'cnt_tx_≥_NUM', 'cnt_tx_gte_NUM', 'cnt_tx_lt_NUM', 
    'cnt_tx_<_NUM', 'cnt_tx_le_NUM', 'cnt_tx_<=_NUM', 'cnt_tx_≤_NUM', 'cnt_tx_lte_NUM', 'cnt_tx_eq_NUM', 
    'cnt_tx_==_NUM', 'cnt_tx_equal_NUM', 'cnt_tx_ne_NUM', 'cnt_tx_!=_NUM', 'cnt_tx_<>_NUM', 'cnt_tx_not_NUM', 
    'cnt_t10n_gt_NUM', 'cnt_t10n_>_NUM', 'cnt_t10n_ge_NUM', 'cnt_t10n_>=_NUM', 'cnt_t10n_≥_NUM', 'cnt_t10n_gte_NUM', 
    'cnt_t10n_lt_NUM', 'cnt_t10n_<_NUM', 'cnt_t10n_le_NUM', 'cnt_t10n_<=_NUM', 'cnt_t10n_≤_NUM', 'cnt_t10n_lte_NUM', 
    'cnt_t10n_eq_NUM', 'cnt_t10n_==_NUM', 'cnt_t10n_equal_NUM', 'cnt_t10n_ne_NUM', 'cnt_t10n_!=_NUM', 'cnt_t10n_<>_NUM', 
    'cnt_t10n_not_NUM', 'cnt_sq_gt_NUM', 'cnt_sq_>_NUM', 'cnt_sq_ge_NUM', 'cnt_sq_>=_NUM', 'cnt_sq_≥_NUM', 'cnt_sq_gte_NUM', 
    'cnt_sq_lt_NUM', 'cnt_sq_<_NUM', 'cnt_sq_le_NUM', 'cnt_sq_<=_NUM', 'cnt_sq_≤_NUM', 'cnt_sq_lte_NUM', 'cnt_sq_eq_NUM', 
    'cnt_sq_==_NUM', 'cnt_sq_equal_NUM', 'cnt_sq_ne_NUM', 'cnt_sq_!=_NUM', 'cnt_sq_<>_NUM', 'cnt_sq_not_NUM', 'cnt_sp_gt_NUM', 
    'cnt_sp_>_NUM', 'cnt_sp_ge_NUM', 'cnt_sp_>=_NUM', 'cnt_sp_≥_NUM', 'cnt_sp_gte_NUM', 'cnt_sp_lt_NUM', 'cnt_sp_<_NUM', 
    'cnt_sp_le_NUM', 'cnt_sp_<=_NUM', 'cnt_sp_≤_NUM', 'cnt_sp_lte_NUM', 'cnt_sp_eq_NUM', 'cnt_sp_==_NUM', 'cnt_sp_equal_NUM', 
    'cnt_sp_ne_NUM', 'cnt_sp_!=_NUM', 'cnt_sp_<>_NUM', 'cnt_sp_not_NUM', 'cnt_q_gt_NUM', 'cnt_q_>_NUM', 'cnt_q_ge_NUM', 
    'cnt_q_>=_NUM', 'cnt_q_≥_NUM', 'cnt_q_gte_NUM', 'cnt_q_lt_NUM', 'cnt_q_<_NUM', 'cnt_q_le_NUM', 'cnt_q_<=_NUM', 
    'cnt_q_≤_NUM', 'cnt_q_lte_NUM', 'cnt_q_eq_NUM', 'cnt_q_==_NUM', 'cnt_q_equal_NUM', 'cnt_q_ne_NUM', 'cnt_q_!=_NUM', 
    'cnt_q_<>_NUM', 'cnt_q_not_NUM', 'cnt_dr_gt_NUM', 'cnt_dr_>_NUM', 'cnt_dr_ge_NUM', 'cnt_dr_>=_NUM', 'cnt_dr_≥_NUM', 
    'cnt_dr_gte_NUM', 'cnt_dr_lt_NUM', 'cnt_dr_<_NUM', 'cnt_dr_le_NUM', 'cnt_dr_<=_NUM', 'cnt_dr_≤_NUM', 'cnt_dr_lte_NUM', 
    'cnt_dr_eq_NUM', 'cnt_dr_==_NUM', 'cnt_dr_equal_NUM', 'cnt_dr_ne_NUM', 'cnt_dr_!=_NUM', 'cnt_dr_<>_NUM', 'cnt_dr_not_NUM', 
    'cnt_rh_gt_NUM', 'cnt_rh_>_NUM', 'cnt_rh_ge_NUM', 'cnt_rh_>=_NUM', 'cnt_rh_≥_NUM', 'cnt_rh_gte_NUM', 'cnt_rh_lt_NUM', 
    'cnt_rh_<_NUM', 'cnt_rh_le_NUM', 'cnt_rh_<=_NUM', 'cnt_rh_≤_NUM', 'cnt_rh_lte_NUM', 'cnt_rh_eq_NUM', 'cnt_rh_==_NUM', 
    'cnt_rh_equal_NUM', 'cnt_rh_ne_NUM', 'cnt_rh_!=_NUM', 'cnt_rh_<>_NUM', 'cnt_rh_not_NUM', 'cnt_rhx_gt_NUM', 'cnt_rhx_>_NUM', 
    'cnt_rhx_ge_NUM', 'cnt_rhx_>=_NUM', 'cnt_rhx_≥_NUM', 'cnt_rhx_gte_NUM', 'cnt_rhx_lt_NUM', 'cnt_rhx_<_NUM', 'cnt_rhx_le_NUM', 
    'cnt_rhx_<=_NUM', 'cnt_rhx_≤_NUM', 'cnt_rhx_lte_NUM', 'cnt_rhx_eq_NUM', 'cnt_rhx_==_NUM', 'cnt_rhx_equal_NUM', 
    'cnt_rhx_ne_NUM', 'cnt_rhx_!=_NUM', 'cnt_rhx_<>_NUM', 'cnt_rhx_not_NUM', 'cnt_pg_gt_NUM', 'cnt_pg_>_NUM', 'cnt_pg_ge_NUM', 
    'cnt_pg_>=_NUM', 'cnt_pg_≥_NUM', 'cnt_pg_gte_NUM', 'cnt_pg_lt_NUM', 'cnt_pg_<_NUM', 'cnt_pg_le_NUM', 'cnt_pg_<=_NUM', 
    'cnt_pg_≤_NUM', 'cnt_pg_lte_NUM', 'cnt_pg_eq_NUM', 'cnt_pg_==_NUM', 'cnt_pg_equal_NUM', 'cnt_pg_ne_NUM', 'cnt_pg_!=_NUM', 
    'cnt_pg_<>_NUM', 'cnt_pg_not_NUM', 'cnt_px_gt_NUM', 'cnt_px_>_NUM', 'cnt_px_ge_NUM', 'cnt_px_>=_NUM', 'cnt_px_≥_NUM', 
    'cnt_px_gte_NUM', 'cnt_px_lt_NUM', 'cnt_px_<_NUM', 'cnt_px_le_NUM', 'cnt_px_<=_NUM', 'cnt_px_≤_NUM', 'cnt_px_lte_NUM', 
    'cnt_px_eq_NUM', 'cnt_px_==_NUM', 'cnt_px_equal_NUM', 'cnt_px_ne_NUM', 'cnt_px_!=_NUM', 'cnt_px_<>_NUM', 'cnt_px_not_NUM', 
    'cnt_pn_gt_NUM', 'cnt_pn_>_NUM', 'cnt_pn_ge_NUM', 'cnt_pn_>=_NUM', 'cnt_pn_≥_NUM', 'cnt_pn_gte_NUM', 'cnt_pn_lt_NUM', 
    'cnt_pn_<_NUM', 'cnt_pn_le_NUM', 'cnt_pn_<=_NUM', 'cnt_pn_≤_NUM', 'cnt_pn_lte_NUM', 'cnt_pn_eq_NUM', 'cnt_pn_==_NUM', 
    'cnt_pn_equal_NUM', 'cnt_pn_ne_NUM', 'cnt_pn_!=_NUM', 'cnt_pn_<>_NUM', 'cnt_pn_not_NUM', 'cnt_vvn_gt_NUM', 'cnt_vvn_>_NUM', 
    'cnt_vvn_ge_NUM', 'cnt_vvn_>=_NUM', 'cnt_vvn_≥_NUM', 'cnt_vvn_gte_NUM', 'cnt_vvn_lt_NUM', 'cnt_vvn_<_NUM', 'cnt_vvn_le_NUM', 
    'cnt_vvn_<=_NUM', 'cnt_vvn_≤_NUM', 'cnt_vvn_lte_NUM', 'cnt_vvn_eq_NUM', 'cnt_vvn_==_NUM', 'cnt_vvn_equal_NUM', 
    'cnt_vvn_ne_NUM', 'cnt_vvn_!=_NUM', 'cnt_vvn_<>_NUM', 'cnt_vvn_not_NUM', 'cnt_vvx_gt_NUM', 'cnt_vvx_>_NUM', 
    'cnt_vvx_ge_NUM', 'cnt_vvx_>=_NUM', 'cnt_vvx_≥_NUM', 'cnt_vvx_gte_NUM', 'cnt_vvx_lt_NUM', 'cnt_vvx_<_NUM', 'cnt_vvx_le_NUM', 
    'cnt_vvx_<=_NUM', 'cnt_vvx_≤_NUM', 'cnt_vvx_lte_NUM', 'cnt_vvx_eq_NUM', 'cnt_vvx_==_NUM', 'cnt_vvx_equal_NUM', 'cnt_vvx_ne_NUM', 
    'cnt_vvx_!=_NUM', 'cnt_vvx_<>_NUM', 'cnt_vvx_not_NUM', 'cnt_ng_gt_NUM', 'cnt_ng_>_NUM', 'cnt_ng_ge_NUM', 'cnt_ng_>=_NUM', 
    'cnt_ng_≥_NUM', 'cnt_ng_gte_NUM', 'cnt_ng_lt_NUM', 'cnt_ng_<_NUM', 'cnt_ng_le_NUM', 'cnt_ng_<=_NUM', 'cnt_ng_≤_NUM', 
    'cnt_ng_lte_NUM', 'cnt_ng_eq_NUM', 'cnt_ng_==_NUM', 'cnt_ng_equal_NUM', 'cnt_ng_ne_NUM', 'cnt_ng_!=_NUM', 'cnt_ng_<>_NUM', 
    'cnt_ng_not_NUM', 'cnt_ug_gt_NUM', 'cnt_ug_>_NUM', 'cnt_ug_ge_NUM', 'cnt_ug_>=_NUM', 'cnt_ug_≥_NUM', 'cnt_ug_gte_NUM', 
    'cnt_ug_lt_NUM', 'cnt_ug_<_NUM', 'cnt_ug_le_NUM', 'cnt_ug_<=_NUM', 'cnt_ug_≤_NUM', 'cnt_ug_lte_NUM', 'cnt_ug_eq_NUM', 
    'cnt_ug_==_NUM', 'cnt_ug_equal_NUM', 'cnt_ug_ne_NUM', 'cnt_ug_!=_NUM', 'cnt_ug_<>_NUM', 'cnt_ug_not_NUM', 'cnt_ux_gt_NUM', 
    'cnt_ux_>_NUM', 'cnt_ux_ge_NUM', 'cnt_ux_>=_NUM', 'cnt_ux_≥_NUM', 'cnt_ux_gte_NUM', 'cnt_ux_lt_NUM', 'cnt_ux_<_NUM', 
    'cnt_ux_le_NUM', 'cnt_ux_<=_NUM', 'cnt_ux_≤_NUM', 'cnt_ux_lte_NUM', 'cnt_ux_eq_NUM', 'cnt_ux_==_NUM', 'cnt_ux_equal_NUM', 
    'cnt_ux_ne_NUM', 'cnt_ux_!=_NUM', 'cnt_ux_<>_NUM', 'cnt_ux_not_NUM', 'cnt_un_gt_NUM', 'cnt_un_>_NUM', 'cnt_un_ge_NUM', 
    'cnt_un_>=_NUM', 'cnt_un_≥_NUM', 'cnt_un_gte_NUM', 'cnt_un_lt_NUM', 'cnt_un_<_NUM', 'cnt_un_le_NUM', 'cnt_un_<=_NUM', 
    'cnt_un_≤_NUM', 'cnt_un_lte_NUM', 'cnt_un_eq_NUM', 'cnt_un_==_NUM', 'cnt_un_equal_NUM', 'cnt_un_ne_NUM', 'cnt_un_!=_NUM', 
    'cnt_un_<>_NUM', 'cnt_un_not_NUM', 'cnt_ev24_gt_NUM', 'cnt_ev24_>_NUM', 'cnt_ev24_ge_NUM', 'cnt_ev24_>=_NUM', 
    'cnt_ev24_≥_NUM', 'cnt_ev24_gte_NUM', 'cnt_ev24_lt_NUM', 'cnt_ev24_<_NUM', 'cnt_ev24_le_NUM', 'cnt_ev24_<=_NUM', 
    'cnt_ev24_≤_NUM', 'cnt_ev24_lte_NUM', 'cnt_ev24_eq_NUM', 'cnt_ev24_==_NUM', 'cnt_ev24_equal_NUM', 'cnt_ev24_ne_NUM', 
    'cnt_ev24_!=_NUM', 'cnt_ev24_<>_NUM', 'cnt_ev24_not_NUM'
    ]

# TODO
lst_climate_entities = [
    'clima_ave_fhvec', 'clima_ave_fg', 'clima_ave_fhx', 'clima_ave_fhn', 'clima_ave_fxx', 'clima_ave_tg', 'clima_ave_tn', 
    'clima_ave_tx', 'clima_ave_t10n', 'clima_ave_sq', 'clima_ave_sp', 'clima_ave_q', 'clima_ave_dr', 'clima_ave_rh', 
    'clima_ave_rhx', 'clima_ave_pg', 'clima_ave_px', 'clima_ave_pn', 'clima_ave_vvn', 'clima_ave_vvx', 'clima_ave_ng', 
    'clima_ave_ug', 'clima_ave_ux', 'clima_ave_un', 'clima_ave_ev24', 'clima_max_fhvec', 'clima_max_fg', 'clima_max_fhx', 
    'clima_max_fhn', 'clima_max_fxx', 'clima_max_tg', 'clima_max_tn', 'clima_max_tx', 'clima_max_t10n', 'clima_max_sq', 
    'clima_max_sp', 'clima_max_q', 'clima_max_dr', 'clima_max_rh', 'clima_max_rhx', 'clima_max_pg', 'clima_max_px', 
    'clima_max_pn', 'clima_max_vvn', 'clima_max_vvx', 'clima_max_ng', 'clima_max_ug', 'clima_max_ux', 'clima_max_un', 
    'clima_max_ev24', 'clima_min_fhvec', 'clima_min_fg', 'clima_min_fhx', 'clima_min_fhn', 'clima_min_fxx', 'clima_min_tg', 
    'clima_min_tn', 'clima_min_tx', 'clima_min_t10n', 'clima_min_sq', 'clima_min_sp', 'clima_min_q', 'clima_min_dr', 
    'clima_min_rh', 'clima_min_rhx', 'clima_min_pg', 'clima_min_px', 'clima_min_pn', 'clima_min_vvn', 'clima_min_vvx',
    'clima_min_ng', 'clima_min_ug', 'clima_min_ux', 'clima_min_un', 'clima_min_ev24'
]

lst_all = lst_entities_statistics + lst_indices + lst_counters + lst_climate_entities

# All the available entities for the calculation of the statistics cells
lst_entities = [
    # 'YYYYMMDD', # Datum (YYYY=jaar MM=maand DD=dag) / Date (YYYY=year MM=month DD=day)
    # 'DDVEC',    # Vector mean wind direction in degrees (360=north, 90=east, 180=south, 270=west, 0=calm/variable)
    'FHVEC',    # Vector mean windspeed (in 0.1 m/s)  
    'FG',       # Daily mean windspeed (in 0.1 m/s)
    'FHX',      # Maximum hourly mean windspeed (in 0.1 m/s)
    # 'FHXH',     # Hourly division in which FHX was measured
    'FHN',      # Minimum hourly mean windspeed (in 0.1 m/s)
    # 'FHNH',     # Hourly division in which FHN was measured
    'FXX',      # Maximum wind gust (in 0.1 m/s)
    # 'FXXH',     # Hourly division in which FXX was measured
    'TG',       # Daily mean temperature in (0.1 degrees Celsius)
    'TN',       # Minimum temperature (in 0.1 degrees Celsius)
    # 'TNH',      # Hourly division in which TN was measured
    'TX',       # Maximum temperature (in 0.1 degrees Celsius)
    # 'TXH',      # Hourly division in which TX was measured
    'T10N',     # Minimum temperature at 10 cm above surface (in 0.1 degrees Celsius)
    # 'T10NH',    # 6-hourly division in which T10N was measured; 6=0-6 UT, 12=6-12 UT, 18=12-18 UT, 24=18-24 UT
    'SQ',       # Sunshine duration (in 0.1 hour) calculated from global radiation (-1 for <0.05 hour)
    'SP',       # Percentage of maximum potential sunshine duration
    'Q',        # Global radiation (in J/cm2)
    'DR',       # Precipitation duration (in 0.1 hour)
    'RH',       # Daily precipitation amount (in 0.1 mm) (-1 for <0.05 mm)
    'RHX',      # Maximum hourly precipitation amount (in 0.1 mm) (-1 for <0.05 mm)
    # 'RHXH',     # Hourly division in which RHX was measured
    'PG',       # Daily mean sea level pressure (in 0.1 hPa) calculated from 24 hourly values
    'PX',       # Maximum hourly sea level pressure (in 0.1 hPa)
    # 'PXH',      # Hourly division in which PX was measured
    'PN',       # Minimum hourly sea level pressure (in 0.1 hPa)
    # 'PNH',      # Hourly division in which PN was measured
    'VVN',      # Minimum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)
    # 'VVNH',     # Hourly division in which VVN was measured
    'VVX',      # Maximum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)
    # 'VVXH',     # Hourly division in which VVX was measured
    'NG',       # Mean daily cloud cover (in octants, 9=sky invisible)
    'UG',       # Daily mean relative atmospheric humidity (in percents)
    'UX',       # Maximum relative atmospheric humidity (in percents)
    # 'UXH',      # Hourly division in which UX was measured
    'UN',       # Minimum relative atmospheric humidity (in percents)
    # 'UNH',      # Hourly division in which UN was measured
    'EV24'      # Potential evapotranspiration (Makkink) (in 0.1 mm)
]

lst_statistics = [ 
    'ave', 
    'max', 
    'min'
]

lst_clima = [
    'clima'
]

lst_count = [
    'cnt'
]

# Available operands for the counter 
lst_operands = [
    'gt', '>', 'ge', '>=', '≥', 'gte', 'lt', '<', 'le', '<=', 
    '≤', 'lte', 'eq', '==', 'equal', 'ne', '!=', '<>', 'not'
]

def entities_statistics(): 
    lst, cnt, col, just = [], 1, 10, 12
    print('STATISTICS')
    for stat in lst_statistics: 
        for ent in lst_entities: 
            el = f'{stat}_{ent}'.lower()
            lst.append(el)
            print(f'{el.ljust(just)}', end='')
            if cnt % col == 0:
                print(' ') 
                cnt = 0
            cnt += 1
    print(' ')
    return lst 

def counters_entities():
    # import random
    lst, cnt, col, just = [], 1, 4, 23
    print('COUNTERS')
    for cnter in lst_count: 
        for ent in lst_entities: 
            for oper in lst_operands: 
                el = f'{cnter}_{ent.lower()}_{oper}_NUM'
                lst.append(el)
                print(f'{el.ljust(just)}', end='')
                if cnt % col == 0:
                    print(' ') 
                    cnt = 0
                cnt += 1
    print(' ')
    return lst

def clima_entities():
    lst, lst_ent, cnt, col, just = [], [], 1, 6, 17
    # Make list entities
    for stat in lst_statistics: 
        for ent in lst_entities: 
            el = f'{stat}_{ent}'.lower()
            lst_ent.append(el)

    print('CLIMATE ENTITIES')
    for clima in lst_clima:
        for ent in lst_ent:
            el = f'{clima}_{ent}'.lower()
            lst.append(el)
            print(f'{el.ljust(just)}', end='')
            if cnt % col == 0:
                print(' ') 
                cnt = 0
            cnt += 1
    print(' ')
    return lst




if __name__ == "__main__":
    lst = entities_statistics()
    print(lst)

    lst = counters_entities()
    print(lst)

    lst = clima_entities()
    print(lst)
