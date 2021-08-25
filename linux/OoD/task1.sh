#Stwórz programik w bashu, który będzie miał następujące funkcjonalności:
#
#1. Program powinien tworzyć dwa katalogi, w katalogu obecnym (tylko przy pierwszym uruchomieniu)
#- source, destiny
#2. Powinien sprawdzać czy coś istnieje w obecnych katalogach, zwrócić informację użytkownikowi
#3 - a. Program ładuje pliki o formacie csv
#3 - b. Program ściąga pliki o formacie csv
#4. Zapisuje plik do source
#5. Jeśli jest wyrażenie do filtrowania powinien uwzględnić tylko dane wiersze -f "Ania"
#6. Wyrażenie filtrujące można opakować w regexa -fr [a-Z]
#7. Rezultatem będą dwa pliki txt, jeden z sformatowaną tablicą i metadane programu. Metadane: źródło, właściciel, rozmiar, ilość danych(W_K), nazwy kolumn
#8. Każdy błąd powinien być zapisany jako log-error-%nazwa pliku%-%data%.txt


function create_catalog () {
  mkdir $1
  return 0
}

function is_folder_existing () {
  if [ -f "$1" ]; then
    return 0
  else
    return 1
  fi
}

function load_file_csv() {
  return 1
}

function download_file_csv() {
  return 1
}

function save_file() {
  return 1
}

function filter() {
  return 1
}

function redirect_errors() {
  return 1
}

function is_empty() {

}

function test () {

  if ! is_folder_existing source;  then
    create_catalog source
  fi

  if ! is_folder_exisitng destiny; then
    create_catalog destiny
  fi



}

test
