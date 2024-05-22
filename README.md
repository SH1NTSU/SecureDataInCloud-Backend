# SecureDataInCloud

## Opis działania kodu

Funkcja ```upload file``` po wybraniu pliku przesyła go na server, gdzie jest szyfrowany wykorzystując AES i wysyłany na Google Cloud Storage. Aby zapisac klucz szyfrujący plik przesyłamy go do bazy danych (postgres) z zaszyfrowaną nazwą pliku. 

Aby pobrać plik z chmury wybieramy ```download file``` i wpisujemy nazwę pliku, na którym nam zależy. Przesyła sie ona na server, po czym plik jest wyjmowany z Google Cloud Storage i klucz z pasującą nazwa pliku jest wyjmowany z bazy danych. Następnie odszyfrowujemy plik wykorzystując AES i klucz z bazy. Odszyfrowany tekst jest zapisywany do pliku o tej samej nazwie co pierwotny i pobierany na komputer użytkownika w folderze pobrane.  

- Server → Flask
- Szyfrowanie → AES
- Frontend → React + Axios
- Database → Postgres w Dockerze 
- Chmura → Google Cloud

## Jak uruchomić projekt

Najlepiej pokazać podczas lekcji. 
