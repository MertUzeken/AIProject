#!/bin/bash

echo "choose which model you want to use"

showMenu(){
	echo ""
	echo ""
	for ((i=0; i<${#options[@]};i++))
        do
			let counter=$i+1
            echo "$counter) ${options[i]}"
        done
	echo ""
}

comAI(){
echo "comAI"
prepareSetup
python ./ingestcomai.py
python ./server.py -m 1

}


GPT4All(){
echo "GPT4All"
prepareSetup
python ./ingestgpt4all.py
python ./server.py -m 2
}


prepareSetup(){
echo "starting frontend"
npm run serve &
echo "deleting old db folder"
rm -rf db
}

runServerSetup(){
    python ./setupGUI.py
}

options=("ComAI with LangChain" "GPT4All" "Setup" "Quit")
select opt in "${options[@]}"
do
    case $opt in
	"ComAI with LangChain")
		comAI;sleep 2
		showMenu
            ;;
        "GPT4All")
        GPT4All;sleep 2
		showMenu
            ;;
        "Setup")
        echo "Setup for backend"
        runServerSetup;sleep 2
		showMenu
            ;;
        "Quit")
        	break
            ;;
        *) echo "invalid option $REPLY"
    esac
done