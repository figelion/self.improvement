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


function is_folder_existing () {
  if [ -e "$1" ]; then
    return 1
  else
    return 0
  fi
}

function is_folder_empty() {
  if [ "$(ls -A "$1")" ]; then
    return 0
  else
    return 1
  fi
}

function create_catalog () {
  mkdir $1
  return 0
}

function is_source_url(){
    if [[ "$SOURCE" =~ $URL_PATTERN ]]; then
      return 0
    else
      return 1
    fi
}

function get_name_of_source() {
  filename=$(basename -- "$1")
}

function save_source_file() {
  if is_source_url "$1" -eq 1; then
    wget "$1" -P "$SOURCE_FOLDER"
  else
    cp "$1" "$SOURCE_FOLDER"
  fi
}

function parse_arguments(){
  while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
      -h|--help)
        echo "Help is coming!"
        exit 0
      ;;

      -s|--source)
        if [ $# -gt 0 ]; then
          SOURCE=$2
          shift
          shift
        fi
      ;;

      -f|--filter)
        if [ $# -gt 0 ]; then
          FILTR=$2
          shift
          shift
        fi
      ;;

      -frow|--filter_row)
        if [ $# -gt 0 ]; then
          FILTER_ROW=$2
          shift
          shift
        fi
      ;;
      -freg|--filter_regex)
        if [ $# -gt 0 ]; then
          FILTER_REGEX=$2
          shift
          shift
        fi
    esac
  done
  return 1
}

function is_source_csv(){
  if [[ "$1" =~ $CSV_PATTERN ]]; then
    return 1
  else
    return 0
  fi
}

function check_essential_arguments() {
  if is_source_csv "$SOURCE" -eq 0; then
    echo "The source file is not csv. The program will be stopped."
    exit 0
  fi
}

function process_file(){
  echo $1
  csvgrep --help
  return 0

}

function run () {

  SOURCE=""
  FILTR=""
  FILTER_ROW=""
  FILTER_REGEX=""

  filename=""

  URL_PATTERN='(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'
  CSV_PATTERN='.+(\.csv)$'

  SOURCE_FOLDER="./source/"
  DESTINY_FOLDER="./destiny/"

  parse_arguments "$@"
  check_essential_arguments
  get_name_of_source "$SOURCE"

  declare -a folders=("$SOURCE_FOLDER" "$DESTINY_FOLDER")

  for folder_name in "${folders[@]}"
  do
    if is_folder_existing "$folder_name" -eq 0 ;  then
      create_catalog "$folder_name"
    fi

    if is_folder_empty "$folder_name" -eq 0; then
      echo "Folder '$folder_name' is not empty"
    fi
  done

  save_source_file "$SOURCE"
  process_file "$SOURCE_FOLDER$filename"

}

run "$@"
