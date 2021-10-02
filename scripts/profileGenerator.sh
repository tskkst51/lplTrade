## Take algo string and write a profile from it

# TB2_HS_IT_OB1_OS1_CB3_CS3

args=" "
algo=""
stock=""

loc=$1
algo=$2
stock=$3

wp=$(pwd)

host=$(hostname -s | awk '{print $1}')

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

# Execute script to populate source library path

dt=$(date "+%Y%m%d")



