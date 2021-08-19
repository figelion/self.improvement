#!/bin/bash

#which bash
#bash --version

#imie="Ania"
#echo $imie
#
#my_current_dir=$(ls)
#current_date=$(date +%d%m%Y)
#echo $my_current_dir + $current_date

#imie="Piotr"
#
#function imie_zbyszek() {
#    local imie="Zbychu"
#    echo $imie
#}
#imie_zbyszek
#
#hello_zbychu(){
#  echo Hello $1
#  return 0
#}
#
#hello_zbychu Zbychu
#a=hello_zbychu ZaZbychu
#
#echo $a
#
#distro_name=$1
#echo $distro_name
#echo 'uname -a'
#echo $(uname -a)

#echo $(ls a*.txt)
#echo $(ls a?.txt)
#echo $(ls a??.txt)
#echo "zad" $( ls a[a-z].txt)
#
#echo "Amount of moeny \$12.3"

#arr=( 1 2 3 )
#echo ${arr}

#echo -e "Podaj liczbe: "
#read liczba
#echo "Liczba: $liczba"

#echo "asd" 1>&2
#dates 2>&1
#date 2>/dev/null

#number=11
#
#if [ $number -eq 12 ]; then
#  echo "Boom"
#elif [ $number -lt 13 ]; then
#  echo "Karamba"
#else
#  echo "Noom"
#fi
#
#arr=(1 2 3)
#
#for i in "${arr[@]}"
#do
#  echo $i
#done


#i=0
#while [ $i -lt 3 ]; do
#  echo $i
#  i=$[$i+1]
#done
#
#i=0
#until [ $i -gt 3 ]; do
#  echo $i
#  i=$[$i+1]
#done