import Vue from 'vue'

export const PULSE_EVENT = 'PULSE_EVENT'
export const RESET_PULSE_EVENT = 'RESET_PULSE_EVENT'
export const PULSE_INTERVAL_MS = 60000

interface Data {
  currentPulse?: number | null;
}

interface Methods {
  emitPulse(): void;
}

const PulseEventBus = Vue.extend<Data, Methods, {}>({
  data () {
    return {
      currentPulse: null
    }
  },
  created () {
    this.currentPulse = setInterval(this.emitPulse, PULSE_INTERVAL_MS)
    this.$on(RESET_PULSE_EVENT, () => {
      if (this.currentPulse !== null) {
        clearInterval(this.currentPulse)
      }
      this.currentPulse = setInterval(this.emitPulse, PULSE_INTERVAL_MS)
    })
  },
  methods: {
    emitPulse () {
      this.$emit(PULSE_EVENT, new Date())
    }
  }
})

export const GlobalPulse = new PulseEventBus()
