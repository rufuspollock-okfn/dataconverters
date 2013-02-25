import tempfile
from subprocess import Popen
import pipes


def parse(stream, **kwargs):
    '''Parse KML file and return row iterator plus metadata.
    '''
    o = tempfile.NamedTemporaryFile()
    o.close()
    with tempfile.NamedTemporaryFile() as i:
        # Write kml stream into input file
        print i.name, o.name
        i.write(stream.read())

        # Flush to disk
        i.flush()
        # Perform conversion with ogr2ogr
        cmd = pipes.quote('ogr2ogr -f "GeoJSON" {ofile} {ifile}'.format(
                          ifile=i.name, ofile=o.name))
        print cmd
        inst = Popen(cmd, shell=True)
        stdout, stderr = inst.communicate()
        print "STDOUT \n"
        print stdout
        print "STDERR \n"
        print stderr
        """# Read o
        output = o.read()
        #parse back to python dict
        print output """
