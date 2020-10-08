import axios from "@/.nuxt/axios";

export default {
  URL: "localhost",

  state: {
    catches: [],
    personsUnique: [],
  },
  getters: {
    allPersons(state) {
      return state.persons
    },
    allUniquePersons(state) {
      return state.personsUnique
    }
  },
  mutations: {
    updateCatches(state, catches) {
      console.log("set this", catches)
      state.catches = catches
    },
    addPerson(state, person) {
      state.persons.push(person)
    },
    setUniquePersons(state, personsUnique) {
      console.log("mut" ,personsUnique)
      state.personsUnique = personsUnique
    }
  },
  actions: {
    getCatches(ctx, payload) {
      console.log(payload)
      this.$axios.get('api/v1/collector/catches_list/' + payload)
        .then(response => {
          console.log("RESPONSE", response)
          ctx.commit('updateCatches', response.data)
        }).catch(e => {
        console.log("ERROR", e)
      })
    },
    getUniquePersons(ctx, payload) {
      this.$axios.post('http://' + ctx.state.URL + ':5000/api/v1/persons_unique', payload)
        .then(resp => {
          console.log(resp)
          ctx.commit('setUniquePersons', resp.data)
        }).catch(err => {
        console.log(err)
      })
    },
  },

}
