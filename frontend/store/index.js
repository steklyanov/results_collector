import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import catches from '~/store/modules/catches'

const store = () => new Vuex.Store({

  modules: {
    catches
  }
})

export default store
