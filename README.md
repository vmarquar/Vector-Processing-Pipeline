# Vector Processing Pipeline

### 1 Transform shapefiles into EPSG:3857 projection (Web Mercator)
```
ogr2ogr -s_srs EPSG:31467 -t_srs EPSG:3857 output.shp input.shp

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
```5. tippecanoe -f -s EPSG:3857 -o output.mbtiles input.json ```
