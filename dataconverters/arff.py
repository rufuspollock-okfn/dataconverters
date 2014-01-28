import datetime

MIMETYPE = 'application/weka'

class ARFF:
    
    def __init__(self, dataset_name='dataset'):
        self.header = u''
        self.data = u'\n@DATA\n'
        self.attr_list = []
        self._add_relation(dataset_name=dataset_name)
        
    def __str__(self):
        return self.header + self.data
    
    def _to_arff_type(self, attr_type):
        if attr_type == 'String':
            return 'STRING'
        elif attr_type == 'Integer':
            return 'NUMERIC'
        elif attr_type == 'Float':
            return 'NUMERIC'
        elif attr_type == 'Decimal':
            return 'NUMERIC'
        elif attr_type == 'DateTime':
            return 'DATE'
            
    def _to_arff_data(self, attr_val, attr_type):
        if not attr_val:
            return u'?'
        if attr_type == 'DATE':
            return unicode(attr_val).replace(' ', 'T')
        if attr_type == 'STRING':
            return u'\'%s\'' % unicode(attr_val).replace('\'', '\"')
        else:
            return unicode(attr_val)  
              
    def _add_relation(self, dataset_name):
        self.header += u'@RELATION %s\n\n' % dataset_name
    
    def add_attr(self, attr_name, attr_type):
        attr_type = self._to_arff_type(attr_type)
        self.attr_list.append((attr_name, attr_type))
        attr_name = attr_name.replace(' ','_')
        self.header += u'@ATTRIBUTE %s %s\n' % (attr_name, attr_type)
        
    def add_record(self, row):
        #for attr_name, attr_type in self.attr_list:
        #    self.data += str(row[attr_name])
        #    self.data += ','
        self.data += ','.join([self._to_arff_data(row[attr_name], attr_type) for attr_name, attr_type in self.attr_list])
        self.data += '\n' 
            
def write(stream, records, metadata, indent=2, **kwargs):
    '''Write data into Weka ARFF structure on the given stream
    
    :param stream: file-like object supporting writing.

    :return: null
    '''
    
    #print 'ARFF\n'
    a = ARFF()
    for attribute in metadata['fields']:
        a.add_attr(attribute['id'], attribute['type'])
    for record in records:
        a.add_record(record)
    
    #print 'Writing...'
    stream.write(unicode(a).encode("UTF-8"))
    