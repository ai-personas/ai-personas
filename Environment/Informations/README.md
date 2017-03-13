##Informations
Informations for Personas resides here. The informations will be added with protobuf definitions which will include information loader, extractor and urls from where information has to be retrieved.

Informations divided in two parts

###Category
The categorical information defintions included here. The defintions are in protobuf format with loader, extractor and URL details. The actual information will be stored in the URL locations and to be retrieved with loader.

###Process
The informations will be accessed through these processors. The process defined in three parts

####Load
The information will be retrieved/stored in the given URL location using loaders. The information could be stored/retireved anywhere with anykind of protocal. The loader is responsible to abstract these processing and provide simple function to store/retrieve the data.

####Extract
The information will be extracted from the loaded data using these extractors. The loader loads the data as its stored in the system and extractor retrieves the subset of these data for personas.

####Transform

