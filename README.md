# SecureDataInCloud-Backend

User wchodzi na strone jeśli chce wysłać i zaszyfrowac plik wybiera uploa. Później klika upload. Plik przesyła sie na server gdzie w serverze jest szyfrowant i zaszyfrowant plik wysyła sie do cloud storage a klucz i nazwa zaszyfrowanego pliku przesyła sie do bazy danych. Potem żeby pobrać ten plik user wpisuje który plik chce pobrac i klika download. nazwa pliku przesyła sie do servera gdzie server wyjmuje plik o tej nazwie z cloud storage i z bazy danych wyjmuje klucz który pasuje do tej nazwy pliku i z kluczem odszyfrwuje go i odzyfrowaną zawartość pliku przesyła na strone. Na stronie pobiera tą zawartość i tworz nowy plik z tą zawartośćą o podanej nazwie i go pobiera w downloads na komputerze usera.

server - flask
szyfrowanie - AES
frontend - react vite + axios
database - postgres + pgAdmin4