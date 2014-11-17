ProGenViZ v1.0

ProGenViZ is a simple web-based program build to visualize, compare, search, order sequences against a reference, and annotate multiple prokaryotic genome sequences and contigs.

Fully functional with Google-Chrome and Safari web browsers

Auxiliary software needed to locally install ProgenViZ:

	- Python -> version 2.7.3 and Biopython 1.58 or above.
	- BLAST -> version 2.2.25 or above.
	- nucmer alignment software -> version 3.07 or above (sudo apt-get install nucmer). Used to order contigs againsta a reference and detect SNPs.
	- Perl   -> version 5.14.2 or above with the modules File::Slurp and File::Temp, CGI::Carp installed through CPAN. Need to define the cgi-bin folder on the webserver. 
	- rsvg-convert -> version 2.36.1 or above. Used to perform conversions from SVG images to PDF or PNG using the export.pl script from the cgi-bin folder.
	- Prodigal -> version 2.60 or above. Used to predict prokaryotic CDS locations in nucleotide sequences


Plugins:

	- DataTables-1.9.4 -> Used to create interactive html tables.
