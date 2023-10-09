<template>
  <v-app>
    <v-main>
      <AIComponent/>
    </v-main>
  </v-app>
</template>

<script>
import AIComponent from './components/AI.vue'

export default {
  name: 'App',

  components: {
    AIComponent,
  },

  data: () => ({
    //
  }),
}
</script>
