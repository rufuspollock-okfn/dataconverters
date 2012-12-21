from dataconverters import geo

class TestShapefile:
    def test_shapefile(self):
        path = 'testdata/shapefiles/karnataka_poi.shp'
        # stream = open(path)
        iterator, metdata = geo.shp_parse(path)
        data = [ geom for geom in iterator ]
        assert len(data) == 8050, len(data)

