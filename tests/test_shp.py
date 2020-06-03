from dataconverters import shp

class _TestShapefile:
    def test_shapefile(self):
        path = 'testdata/shapefiles/karnataka_poi.shp'
        # stream = open(path)
        iterator, metdata = shp.parse(path)
        data = [ geom for geom in iterator ]
        assert len(data) == 8050, len(data)

