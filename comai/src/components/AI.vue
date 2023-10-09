<template>
  <v-app>
    <v-toolbar app color="orange-darken-1">
    <v-toolbar-title>
      <span class="font-weight-light">communicate</span>
      <span>AI</span>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn 
    icon 
    @click.stop="drawer = !drawer"
    >
      <v-icon
       color="white"
       >
       mdi-menu-open</v-icon>
      
    </v-btn>

    </v-toolbar>

<!-- Chat here -->
    <v-container fluid
          class="fill-height pa-0 d-flex align-stretch"
        > 
          <v-row class="no-gutters elevation-4">
            <v-col
              cols="auto"
              class="flex-grow-1 flex-shrink-0"
            >
              <v-responsive
                v-if="activeChat"
                class="overflow-y-hidden fill-height"
                height="500"
              >
                <v-card
                  flat
                  class="d-flex flex-column fill-height"
                >
                  <v-card-text class="flex-grow-1 overflow-y-auto">
                    <template v-for="(msg, i) in messages" :key="i">  <!--msg,i  -->
                      <div
                        
                        :class="{ 'd-flex flex-row-reverse': msg.me }"
                      >
                        <v-menu offset-y>
                          <template v-slot:activator="{ on }">
                            <v-hover
                              v-slot:default="{ hover }"
                              v-on="on"
                              >
                              <v-chip
                                :color="msg.me ? 'primary' : ''"
                                dark
                                style="height:auto;white-space: normal;"
                                class="pa-4 mb-2"
                                hover
                                >
                                {{ msg.content }}
                                <sub
                                  class="ml-2"
                                  style="font-size: 0.5rem;"
                                >{{ msg.created_at }}</sub>
                                <v-icon
                                  v-if="hover"
                                  small
                                >
                                mdi-chevron-down
                                </v-icon>
                              </v-chip>
                            </v-hover>
                          </template>
                          <v-list>
                            <v-list-item>
                              <v-list-item-title>delete</v-list-item-title>
                            </v-list-item>
                          </v-list>
                        </v-menu>
                      </div>
                    </template>
                  </v-card-text>
                  <v-card-text height="100" class="flex-grow-0 flex-shrink-1">
                      <v-text-field
                      v-model="newMessageContent"
                      label="Stelle hier deine Frage . . ."
                      type="text"
                      no-details
                      outlined
                      append-outer-icon="send"
                      @keyup.enter="addMessageMe"
                      @click:append-outer="addMessageMe"
                      hide-details
                    />
                  </v-card-text>
                </v-card>
              </v-responsive>
            </v-col>
          </v-row>
        </v-container>
        <!-- Chat ends here -->

    <v-navigation-drawer class="grey lighten-1"
      location="right"
      v-model="drawer"
      temporary
    >
    <v-responsive
      class="overflow-y-hidden fill-height"
      height="500"
    >
        <v-card title="Vorschläge" subtitle="Oft gestellte Fragen" text="Andere Nutzer fragten auch folgendes...">
          <v-icon aria-hidden="false" icon="md:home"></v-icon>
        </v-card>
 
    <v-divider
      :thickness="7"
      class="border-opacity-75"
      color="grey"
    >
    </v-divider>
    <v-list density="compact" nav>
      <v-list-item 
        v-for="title in titles" 
        :key="title"
        :title="title"
        :value="title"
        @click="sendNavbarQuestion(title)">
      </v-list-item>
    </v-list>   </v-responsive>
    </v-navigation-drawer>
   
   <!-- <v-footer border app absolute inset>   optional*
      <span class="font-weight-light">
        communicate-germany 2023
      </span>  
    </v-footer>-->
  </v-app>
</template>


<script>
import axios from 'axios';
  export default {
      data: () => ({
        activeChat: 1,
        messages:[],
        drawer: false,
        newMessageContent: '',
        titles: []
      }),
    
      created(){
        this.greeting();
        this.loadNavbarQuestions();
      },

    methods: {

      addMessageAI(answer){
        this.messages.push(
          {
          content: answer,
          me: false,
          created_at: this.getDate()
        });
      },

      addMessageMe() {
        this.messages.push({
          content: this.newMessageContent,
          me: true,
          created_at : this.getDate()
        });
        this.postMessage(this.newMessageContent)
        this.newMessageContent=' ';
      },

      greeting() {
        this.messages.push(
          {
          content: "Hallo ! Wie kann ich dir behilflich sein ? 🙂",
          me: false,
          created_at: this.getDate()
        });
      },
  
      getDate(){
        var today = new Date();
        //var dd = String(today.getDate()).padStart(2, '0');
        //var mm = String(today.getMonth() + 1).padStart(2, '0');
        //var yyyy = today.getFullYear();
        var hr = today.getHours();
        var min = today.getMinutes();
        /*today = dd + '/' +  mm + '/' + yyyy + ' | ' + hr + ':' + min;*/
        today = hr + ":" + min;
        if (hr < 12)
          return today + 'am';
        else 
          return today + 'pm';
      },

      async loadNavbarQuestions(){
        try {
          const response = await axios.get('http://127.0.0.1:9000/getQuestions');
          console.log(response.data)
          this.titles = response.data.map(item=> item.Fragen); 
        } 
        catch (error) {
          console.error("Error loading titles:", error);
        }
      },

      async postMessage(message) {
        const messageBody = {message};
        const URL = 'http://127.0.0.1:9000/sendRequest';   //API Endpoint

        try {
          const response = await axios.post(URL,messageBody,{headers: {'Content-Type':'application/json'}})
          
          this.addMessageAI(response.data.response)
        }
        catch (error) {
          console.error('Error desc: ', error);
        }
      },
      sendNavbarQuestion(title){
        // This can be similar to your `addMessageMe` method, but for a title
        this.messages.push({
        content: title,
        me: true,
        created_at: this.getDate()
        });
        this.postMessage(title);  // I'm assuming you want to post the title to the backend as well
      }
  }
}
</script>