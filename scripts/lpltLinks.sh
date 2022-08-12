#!/bin/bash

## Change links

tgt="/Volumes/2T2"
lplt="${tgt}/lplTrade/"
lpla="${tgt}/lpltArchives/"

cd $LPLT || exit 1

if [[ -n $1 ]]; then
   if [[ -h "db" ]]; then
      rm db || echo failed to delete
      mkdir db || echo failed to mkdir
   fi
   
   if [[ -h "dbArchive" ]]; then
      rm dbArchive || echo failed to delete
      mkdir dbArchive || echo failed to delete
   fi
   
   if [[ -h "test" ]]; then
      rm test || echo failed to delete
      mkdir test || echo failed to mkdir
   fi
   
   if [[ -h "exitResults" ]]; then
      rm exitResults || echo failed to delete
      mkdir exitResults || echo failed to mkdir
   fi
   
   if [[ -h "historyBestAlgos" ]]; then
      rm historyBestAlgos || echo failed to delete
      mkdir historyBestAlgos || echo failed to mkdir
   fi
   
   if [[ -h "totalResults" ]]; then
      rm totalResults || echo failed to delete
      mkdir totalResults || echo failed to mkdir
   fi

   cd ${LPLT}/.. || exit 1
   
   if [[ -h "lpltArchives" ]]; then
      rm lpltArchives || echo failed to delete
      mkdir totalResults || echo failed to mkdir
   fi

## Change dirs
else
   
   if [[ -d "db" ]]; then
      mv db dbOrig || echo failed move
      ln -s ${lplt}/db db || echo failed to link
   fi

   if [[ -d "dbArchive" ]]; then
      mv dbArchive dbArchiveOrig || echo failed move
      ln -s ${lplt}/dbArchive dbArchive || echo failed to link
   fi

   if [[ -d "test" ]]; then
      mv test testOrig || echo failed move
      ln -s ${lplt}/test test || echo failed to link
   fi

   if [[ -d "exitResults" ]]; then
      mv exitResults exitResultsOrig || echo failed move
      ln -s ${lplt}/exitResults exitResults || echo failed to link
   fi

   if [[ -d "historyBestAlgos" ]]; then
      mv historyBestAlgos historyBestAlgosOrig || echo failed move
      ln -s ${lplt}/historyBestAlgos historyBestAlgos || echo failed to link
   fi

   if [[ -d "totalResults" ]]; then
      mv totalResults totalResultsOrig || echo failed move
      ln -s ${lplt}/totalResults totalResults || echo failed to link
   fi

   cd ${LPLT}/.. || exit 1
   
   if [[ -d "lpltArchives" ]]; then
      mv lpltArchives lpltArchivesOrig || echo failed move
      ln -s ${lpla} lpltArchives || echo failed to link
   fi

fi

exit 0
