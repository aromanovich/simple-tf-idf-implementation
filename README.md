simple-tf-idf-implementation
============================

Very simple search engine using tf*idf measure and mystem.  

Usage:  

1. Create index using `python create_index.py -i <index_file> -c <path_to_collection> [-m <path_to_mystem_binary>]`;
2. Run `python -i search.py -i <index_file> [-m <path_to_mystem_binary>]`.  
Now you can issue commands like `s.search('WHAT DO YOU GET IF YOU MULTIPLY SIX BY NINE?')`.

Mystem available here: http://company.yandex.ru/technologies/mystem/
