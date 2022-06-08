# Django_Portal_Pracy

Troje dzielnych muszkieterów rusza w świat, aby rozpocząć pracę z Django oraz zmierzyć się z przeciwnościami losu. Czy uda im się ukończyć ten projekt na czas? Przekonajmy się!

Autorzy: Patrycja Biryło, Rafał Ciupek, Arkadiusz Żebrowski

Portal pracy
Aplikacja ma służyć firmom poszukującym nowych pracowników oraz osobom poszukującym pracy.
Podstawowe funkcje aplikacji: zgłaszanie ofert przez firmy (formularz z parametrami oferty, np. branża,
zawód, stanowisko), określenie formularza odpowiedzi na ofertę, tzn. jakich informacji o osobie zainteresowanej
oferta firma potrzebuje (np. wiek, rodzaj wykształcenia, miejsce zamieszkania, staż), przeglądanie
ofert z możliwoscią ich filtrowania, odpowiadanie na ofertę (wypełnienie formularza odpowiedzi).
projekt dla grupy maksymalnie 3-osobowej


Przy wyłączonej opcji debugowania (DEBUG = False) Django nie obsługuje plików static i media - powinien to zrobić serwer przy odpowiedniej konfiguracji,
np. tak jak u nas:
<a href="http://djangojobportal.pl/" target="_blank"> DjangoPortalPracy</a>

Aby lokalnie uruchomić stronę z wyłączonym debugowaniem musisz uruchomić lokalny server używając polecenia:
py manage.py runserver --insecure
lub zmienić opcje debugowania w pliku settings.py na: 
DEBUG = True

