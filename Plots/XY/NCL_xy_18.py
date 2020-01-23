"""
NCL_xy_18.py
============
Concepts illustrated:

- Filling the area between two curves in an XY plot
- Labeling the bottom X axis with years
- Drawing a main title on three separate lines
- Calculating a weighted average
- Changing the size/shape of an XY plot using viewport resources
- Manually creating a legend
- Overlaying XY plots on each other
- Maximizing plots after they've been created

See the [original NCL example](https://www.ncl.ucar.edu/Applications/Scripts/xy_18.ncl)
"""

###############################################################################
# Basic imports
import numpy as np
import xarray as xr

###############################################################################
# Open files and read in monthly data


v1 = xr.open_dataset("../../data/netcdf_files/TREFHT.B06.61.atm.1890-1999ANN.nc")
v2 = xr.open_dataset("../../data/netcdf_files/TREFHT.B06.59.atm.1890-1999ANN.nc")
v3 = xr.open_dataset("../../data/netcdf_files/TREFHT.B06.60.atm.1890-1999ANN.nc")
v4 = xr.open_dataset("../../data/netcdf_files/TREFHT.B06.57.atm.1890-1999ANN.nc")
n1 = xr.open_dataset("../../data/netcdf_files/TREFHT.B06.66.atm.1890-1999ANN.nc")
n2 = xr.open_dataset("../../data/netcdf_files/TREFHT.B06.67.atm.1890-1999ANN.nc")
n3 = xr.open_dataset("../../data/netcdf_files/TREFHT.B06.68.atm.1890-1999ANN.nc")
n4 = xr.open_dataset("../../data/netcdf_files/TREFHT.B06.69.atm.1890-1999ANN.nc")
g = xr.open_dataset("../../data/netcdf_files/gw.nc")

###############################################################################
# Some parameters
nyrs = 110
nlon = 128
nlat = 64
time = np.linspace(1890, 1999, endpoint=True)

###############################################################################
# OBS

obs = np.loadtxt("../../data/ascii_files/jones_glob_ann_2002.asc", dtype=float)

###############################################################################
# NATURAL

pass

# nat          = new ((/4,nyrs,nlat,nlon/), float)
# nat(0,:,:,:) = n1->TREFHT
# nat(1,:,:,:) = n2->TREFHT
# nat(2,:,:,:) = n3->TREFHT
# nat(3,:,:,:) = n4->TREFHT

# ncase = 4
# gavn  = wgt_areaave(nat,g->gw,1.0,0)
# gavan = new((/ncase,nyrs/),float)

# do c = 0, ncase-1
# gavan(c,:) =  gavn(c,:)-dim_avg(gavn(c,0:29))
# end do
# gavan!0    = "ensembles"
# gavan!1    = "time"
# gavan&time = v1->time

# delete(nat)

###############################################################################
# ALL

pass

# volc          = new ((/4,nyrs,nlat,nlon/), float)
# volc(0,:,:,:) = v1->TREFHT
# volc(1,:,:,:) = v2->TREFHT
# volc(2,:,:,:) = v3->TREFHT
# volc(3,:,:,:) = v4->TREFHT

# ncase  = 4
# gavv   = wgt_areaave(volc,g->gw,1.0,0)
# gavav  = new((/ncase,nyrs/),float)

# do c = 0, ncase-1
# gavav(c,:) =  gavv(c,:)-dim_avg(gavv(c,0:29))
# end do

# gavav!0    = "ensembles"
# gavav!1    = "time"
# gavav&time = v1->time

# delete(volc)

###############################################################################
# CALCULATE MIN & MAX

pass

# mnmx      = new ((/7,nyrs/), float)
# mnmx(0,:) = dim_min( gavav(time|:,ensembles|:) )
# mnmx(1,:) = dim_max( gavav(time|:,ensembles|:) )
# mnmx(2,:) = dim_min( gavan(time|:,ensembles|:) )
# mnmx(3,:) = dim_max( gavan(time|:,ensembles|:) )
# mnmx(4,:) = dim_avg( gavav(time|:,ensembles|:) )
# mnmx(5,:) = dim_avg( gavan(time|:,ensembles|:) )
# mnmx(6,0:109) = obs(34:143)-dim_avg(obs(34:63))

###############################################################################
# Create plot

pass

# wks = gsn_open_wks("png","xy")             ; send graphics to PNG file

# res                    = True              ; plot mods desired
# res@gsnDraw            = False             ; don't draw yet
# res@gsnFrame           = False             ; don't advance frame yet

# res@vpHeightF 	 = 0.4               ; change aspect ratio of plot
# res@vpWidthF 	         = 0.7

# res@trYMaxF            = 1.0
# res@trXMinF	         = 1890              ; set x-axis minimum

# res@xyMonoLineColor    = False             ; want colored lines
# res@xyLineColors       = (/"Red","Blue","Black"/) ; colors chosen
# res@xyLineThicknesses	 = (/3.,3.,4./)      ; line thicknesses
# res@xyDashPatterns	 = (/0.,0.,0./)      ; make all lines solid

# res@tiYAxisString	 = "~F35~J~F~C"      ; add an axis title
# res@txFontHeightF	 = 0.0195            ; change title font heights

# top_plot = gsn_csm_xy (wks,time,mnmx(4:6,:),res)       ; create line plot

# # Create a plot with the area between both curves filled in blue.
# delete(res@xyLineColors)
# res@gsnXYFillColors = "LightBlue"
# res@xyLineColor     = -1                           ; We don't want the line, so make it transparent.
# bot_plot  = gsn_csm_xy (wks,time,mnmx(2:3,:),res)  ; Create filled XY plot.

# # Create a plot with the area between both curves filled in pink.
# res@gsnXYFillColors = "LightPink"
# res@xyLineColor     = -1                           ; We don't want the line, so make it transparent.
# mid_plot  = gsn_csm_xy (wks,time,mnmx(0:1,:),res)  ; Create another filled XY plot.

# #
# # Overlay the top and mid plots on the bottom plot.
# #
# # Don't draw anything yet, because we still need to
# # attach a legend and some titles.
# #
# overlay(bot_plot,mid_plot)
# overlay(bot_plot,top_plot)

###############################################################################
# Manually create and attach legend

# res_text                    = True                  ; text mods desired
# res_text@txFontHeightF      = 0.015                 ; change text size
# res_text@txJust             = "CenterLeft"          ; text justification

# res_lines                   = True                  ; polyline mods desired
# res_lines@gsLineDashPattern = 0.                    ; solid line
# res_lines@gsLineThicknessF  = 5.                    ; line thicker
# res_lines@gsLineColor       = "red"                 ; line color
# xx = (/1893,1907/)
# yy = (/0.705,0.705/)
# dum1 = gsn_add_polyline(wks,bot_plot,xx,yy,res_lines)              ; add polyline
# dum2 = gsn_add_text(wks,bot_plot,"Anthropogenic + Natural",1910,0.705,res_text); add text

# yy = (/0.79,0.79/)
# res_lines@gsLineColor       = "blue"                                 ; change to blue
# dum3 = gsn_add_polyline(wks,bot_plot,xx,yy,res_lines)                ; add polyline
# dum4 = gsn_add_text(wks,bot_plot,"Natural",1910,0.79,res_text)       ; add text

# yy = (/0.875,0.875/)
# res_lines@gsLineColor       = "black"                                ; change to black
# dum5 = gsn_add_polyline(wks,bot_plot,xx,yy,res_lines)                ; add polyline
# dum6 = gsn_add_text(wks,bot_plot,"Observations",1910,0.875,res_text) ; add text

###############################################################################
# Manually create and attach titles

pass

# #
# # Attach some titles at the top.
# #
#   res_text               = True
#   res_text@txFontHeightF = 0.03                       ; change font size
#   txid_top = gsn_create_text(wks, "Parallel Climate Model Ensembles", res_text)

#   amres                  = True
#   amres@amJust           = "BottomCenter"
#   amres@amParallelPosF   =  0.0    ; This is the center of the plot.
#   amres@amOrthogonalPosF = -0.72   ; This is above the top edge of the plot.
#   annoid_top = gsn_add_annotation(bot_plot, txid_top, amres)

#   res_text@txFontHeightF = 0.02                       ; change font size
#   txid_mid = gsn_create_text(wks, "Global Temperature Anomalies",res_text)

#   amres@amOrthogonalPosF = -0.62  ; This is just below the previous title.
#   annoid_mid = gsn_add_annotation(bot_plot, txid_mid, amres)

#   res_text@txFontHeightF = 0.015                      ; change font size
#   txid_bot = gsn_create_text(wks,"from 1890-1919 average",res_text)

#   amres@amOrthogonalPosF = -0.55  ; This is just below the previous title.
#   annoid_bot = gsn_add_annotation(bot_plot, txid_bot, amres)

#   pres = True
#   maximize_output(wks,pres)
