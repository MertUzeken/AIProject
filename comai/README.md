# comai

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### Before running, make sure to do the following steps first:
### 0. Install node.js and then npm if not already done. 
### 0.1 Install the requirements for python, Inside terminal type pip install -r requirements.txt.
### 0.2 Inside terminal, navigate to the project folder and run npm install to download dependencies for the frontend.

### Auto Installation
###      |
###      |
###      V


### You can now use the run_server.sh bashfile to automatically setup, start front and backend for you.
### Open a bash shell, navigate to the project folder, type in --> ./run_server.sh
### When script is running type 3 to fetch PDF's from Sharepoint. A Window should open (in the background sometimes check taskbar).
### You can change or leave the credentials as they are and continue --> hit save.
### When finished, you will be back at the menu. Now choose the model you want to use and wait for it to finish.
### Have fun.



### Manual Installation 
###         |
###         |
###         V

### 1. Delete any db folder inside comai root folder. (ingestion is going to create a fresh one)
### 2. Run SetupGUI version of the setup, hit save and let it proceed.
### 3. Run the respective version of ingestion for the version you going to use (LangChain or GPT4All)

### Info:
### 3.1 Each respective ingestion creates different dimensioned chroma vector db tabels, 
### according to the model used.

### 4. Run server.py to start the backend
### 5. Open console, navigate to the root of comai and run >>  npm run serve (for dev build) to start the frontend




### Additional infos:
### 1. The questions for the frontend (navbar) are stored inside the PDFStore container as excel sheet (.xsls)
### to change questions locally, just change the rows except the first (A1) following the example given.

### 2. When running SetupGUI, it will pull the example questions from the >>Sharepoint<<, which will make it necessary to change it again locally by hand.
### A new list can be uploaded to the sharepoint folder for further testing / development.

### 3. You can use any GGML model provided by Nomic AI (GTP4All). For our case we tested the code with ggml-gpt4all-j-v1.3-groovy.bin.




