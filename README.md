# Vector Processing Pipeline

### 1 Transform shapefiles into EPSG:3857 projection (Web Mercator)
When a .prj file is provided double check for the correct EPSG Code here: http://prj2epsg.org/search
```
ogr2ogr -s_srs EPSG:31463 -t_srs EPSG:3857 output.shp input.shp
```
Or you can use the .prj file directly:
```
ogr2ogr -a_srs input.prj output_tmp.shp input.shp
ogr2ogr -t_srs EPSG:3857 output.shp output_tmp.shp (untested, könnte aber funktionieren)
```

### 1 Merge Shape Files
All shape files must be in the same directory. `-R` allows recursive merging.
```
python shapemerger.py input/*.shp outpath/outfile.shp
```
### 2 Create GeoJSON from shapefile
```
ogr2ogr -f GeoJSON -dsco "COORDINATE_PRECISION=6" output.json input.shp -progress
```
### 3 Create MBTiles with simplification of polygons (Tippecanoe)
The zoomlevel depends on the data and should be checked manually before create the MBTiles (e.g. loaded into TileMill).
See https://github.com/mapbox/tippecanoe/blob/master/README.md for a detailed parameter description.
As the input data is pretty big and dense (covers whole Germany with >200k features) we need a strong simplification to see something. --maximum-zoom=8 --minimum-zoom=14 --full-detail=10 (default 12) --projection=EPSG:3857 --simplification=5 --coalesce --drop-polygons --read-parallel (needs line seperated features) --drop-smallest-as-needed
```
tippecanoe --minimum-zoom=8 --maximum-zoom=18 --projection=EPSG:3857 --full-detail=10 --simplification=5 --coalesce --drop-polygons --read-parallel --drop-smallest-as-needed -o output.mbtiles input.json
```
### 4 Use the Patch Script from MBUtil package to create a composite layer of multiple Inputs
We are having three basemaps with a scale of 1:1000k, 1:200k and 1:25k which we use to create MBTiles for their intended zoomlevel. After that (Step 3) we join them together using following script: https://github.com/mapbox/mbutil/blob/master/patch
```
./patch.sh gk1000k_0-9.mbtiles gk200k_10-14.mbtiles 
.patch.sh [src] [dst]
```
However the script does not update the metadata.json, which must be edited by hand after the merging.
