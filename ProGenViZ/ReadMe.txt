Update Da VERSAO:
É possivel visualizar os HSPs alinhados após o BLAST e visualizar as single nucleotide variations

Programas necessários:

- Python -> Versao 2.7.3 com Biopython 1.58
- BLAST -> Versão 2.2.25 
- nucmer -> Ferramenta de alinhamento de sequencias de DNA. Versao 3.07 sudo apt-get install nucmer
- Perl   -> Versao 5.14.2 com modulos File::Slurp, File::Temp e CGI::Carp instalados atraves do CPAN.
- Google-Chrome -> Actualmente, o programa apenas está totalmente funcional com este Browser.
- rsvg-convert -> Version 2.36.1 Usado para fazer as conversoes de SVG para PDF ou PNG através de um script em Pearl presente em cgi-bin (export.pl) depois de submeter um form. 
- Prodigal -> Imbutido no programa a versão 2.60

Plugins:
Estão imbutidos no programa
- DataTables-1.9.4 -> Utilizado para criar tabelas html interactivas. extras: TableTools, ColReorder, ColVis
- pace-0.5.1 -> Usado para criar a Progress Bar

Indicações Adicionais:

- Alterar cgi-bin no web-server para que o export.pl funcione.
- Alterar php.ini para ter uploads superiores a 2M. upload_max_filesize, post_max_size e tempo de resposta maximo.
- Actualmente as permissões estão todas em 777 para construir o site à vontade mas depois têm de ser alteradas.
- Os ficheiros de python e alguns php quando criam ficheiros ou directorias alteram também as permissões para 777. Têm de ser adaptadas quando o site for passado para o servidor.

Possíveis permissões para Folders:

- parsers -> Executar
- makeComparisons -> Executar
- cgi-bin -> Executar
- css -> leitura
- data_plot_js -> leitura
- img -> leitura
- js -> leitura
- plugins -> leitura
- prodigal -> executar
- TesFiles -> leitura
- uploads -> leitura e gravação
