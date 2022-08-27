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

function create_folder () {
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

function get_name_extension_of_source() {
  bare_name=$(basename -- "$1")
  filename="${bare_name%.*}"
  file_extension="${bare_name##*.}"
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
        echo "Script used to load the csv and filter it by options"
        echo " "
        echo "Require arguemnts:"
        echo "-s|--source:            url or path to csv which should be processed"
        echo "--frow:     column in csv which should be filtered."
        echo " "
        echo "One of belowe arguemnts must be define:"
        echo "--fexp:                 string which will be looked for in given column in csv"
        echo "--freg:                 regex which will be match in given column in csv"
        exit 0
      ;;

      -s|--source)
        if [ $# -gt 0 ]; then
          SOURCE=$2
          shift
          shift
        fi
      ;;

      --fexp)
        if [ $# -gt 0 ]; then
          FILTER_EXPRE=$2
          shift
          shift
        fi
      ;;

      --frow)
        if [ $# -gt 0 ]; then
          FILTER_COLUMN=$2
          shift
          shift
        fi
      ;;

      --freg)
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
    exit 1
  elif ! [ "$FILTER_COLUMN" ]; then
    echo "No column for filtering define. The program will be stopped"
    exit 1
  elif ! [[ "$FILTER_EXPRE" || "$FILTER_REGEX" ]]; then
    echo "No filtering defined. The program will be stopped"
    exit 1
  fi
}

function create_meta_file(){
  OWNER=$(stat -c '%U' $0)
  SIZE=$(stat -c '%s' $0)
  SOURCE=$(pwd)
  COLUMN_NAMES=$(cat $SOURCE_FILE_PATH | head -n 1)

  echo "source: $SOURCE" >> $DEST_FILE_PATH
  echo "owner: $OWNER" >> $DEST_FILE_PATH
  echo "size: $SIZE bytes" >> $DEST_FILE_PATH
  echo "output lines: $LINES" >> $DEST_FILE_PATH
  echo "column names: $COLUMN_NAMES" >> $DEST_FILE_PATH

}

function process_file(){
  output_date=$(date +"%Y%m%d%H%M")
  if [ "$FILTER_COLUMN" ]; then
    if [ "$FILTER_EXPRE" ]; then
      echo "use expre"
      csvgrep -c "$FILTER_COLUMN" -m "$FILTER_EXPRE" "$1" | csvlook > "$DESTINY_FOLDER$output_date"_"$filename"".txt"
    elif [ "$FILTER_REGEX" ]; then
      echo "use reg"
      echo "$FILTER_REGEX"
      csvgrep -c "$FILTER_COLUMN" -r "$FILTER_EXPRE" "$1" | csvlook > "$DESTINY_FOLDER$output_date"_"$filename"".txt"
    fi
  fi
  return 0
}

function run () {

  SOURCE=""
  FILTER_COLUMN=""
  FILTER_EXPRE=""
  FILTER_REGEX=""

  filename=""
  file_extension=""

  URL_PATTERN='(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'
  CSV_PATTERN='.+(\.csv)$'

  SOURCE_FOLDER="./source/"
  DESTINY_FOLDER="./destiny/"

  parse_arguments "$@"
  check_essential_arguments
  get_name_extension_of_source "$SOURCE"

  declare -a folders=("$SOURCE_FOLDER" "$DESTINY_FOLDER")

  for folder_name in "${folders[@]}"
  do
    if is_folder_existing "$folder_name" -eq 0 ;  then
      create_folder "$folder_name"
    fi

    if is_folder_empty "$folder_name" -eq 0; then
      echo "Folder '$folder_name' is not empty"
    fi
  done

  save_source_file "$SOURCE"
  process_file "$SOURCE_FOLDER$filename.$file_extension"

}

run "$@"
