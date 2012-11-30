Data Converters
===============

Web services for converting data from one format to another.  The converters accept data as a query parameter named url.  There's already [CORS](https://en.wikipedia.org/wiki/Cross-Origin_Resource_Sharing) support and JSOP (add callback parameter to the URL).  Empty column names will be auto-generated with column_1, column_2, etc. Duplicate column names will have _n added as well. For instance, two columns with name date will be date_1, date_2.

* [Architecture slidedeck](https://docs.google.com/presentation/d/1LplNTIFwVIAfeP-C8RkPhlZJqaV95DasHlhloPrdvIc/edit)
* [Architecture (Simple) Drawing](https://docs.google.com/drawings/d/1fxamPv8ccJYI-NSQJ_7hcPoF5X8eBTQDatg-HCybsZk/edit)
* [Architecture (Complex) Drawing](https://docs.google.com/drawings/d/1GbtXf5m9HLVXTNXhJiE0V1SQs0mP9os11y-48TDzKqA/edit)

User stories are on [Google Docs](https://docs.google.com/document/d/1ivosmeaFS0NgQI-wlehCIdQGlnRm-Yk571tqA2FMBqg/edit), if you want to add more, please file an issue.

Please bugs for any issues you see.

CSV -> JSON
-----------

For CSV input files, add `type=csv` to the url.

Example - http://converter.dev.okfn.org/api/convert/json?url=http://resources.opendatalabs.org/u/nigelb/data-converters/csv/simple.csv

Example with type - http://converter.dev.okfn.org/api/convert/json?url=http://resources.opendatalabs.org/u/nigelb/data-converters/csv/simple.csv&type=csv

Example with JSONP - http://converter.dev.okfn.org/api/convert/json?url=http://resources.opendatalabs.org/u/nigelb/data-converters/csv/simple.csv&callback=callback

XLS(X) -> JSON
--------------

For XLS input files add `type=xls` to the URL, and for XLSX files, add `type=xls&excel_type=xlsx`.

Example - http://converter.dev.okfn.org/api/convert/json?url=http://resources.opendatalabs.org/u/nigelb/data-converters/xls/simple.xls

Example with type - http://converter.dev.okfn.org/api/convert/json?url=http://resources.opendatalabs.org/u/nigelb/data-converters/xls/simple.xls&type=xls

Example of xlsx file with type - http://converter.dev.okfn.org/api/convert/json?url=http://resources.opendatalabs.org/u/nigelb/data-converters/xls/simple.xlsx&type=xls&excel_type=xlsx
