<template>
  <BAlert
    title="Verbindungsfehler"
    variant="danger"
    :show="showingAlert"
    class="position-fixed fixed-top m-0 rounded-0"
    dismissible
    @dismissed="alertDismissed"
  >
    <div class="container">
      Beim abholen neuer Daten trat ein Verbindungsfehler auf. Angezeigte Daten sind nun möglicherweise nicht mehr
      aktuell.
      <br><b>Wenn diese Meldung nicht geschlossen wird lädt die Seite in {{ reloadCountdown }} Sekunden neu</b>
    </div>
  </BAlert>
</template>

<script lang="ts">
import Vue from 'vue'
import {
  CONNECTION_ALERT_DISMISSED_EVENT,
  CONNECTION_ALERT_EVENT,
  ConnectionAlertBus
} from '@/common/ConnectionAlertBus'
import { BAlert } from 'bootstrap-vue'

const CONNECTION_ISSUE_RELOAD_COUNTDOWN_SECONDS = 10
const CONNECTION_ALERT_TOAST_ID = 'CONNECTION_ALERT_TOAST_ID'

interface Data {
  showingAlert: boolean;
  reloadCountdown: number;
  toastId: string;
  aborted: boolean;
}

interface Methods {
  reloadCountdownStep (): void;

  stopAndResetReloadCountdown (): void;

  alertDismissed (): void;
}

export default Vue.extend<Data, Methods, {}, {}>({
  components: {
    BAlert
  },
  data () {
    return {
      toastId: CONNECTION_ALERT_TOAST_ID,
      showingAlert: false,
      reloadCountdown: CONNECTION_ISSUE_RELOAD_COUNTDOWN_SECONDS,
      aborted: false
    }
  },
  created () {
    ConnectionAlertBus.$on(CONNECTION_ALERT_EVENT, () => {
      if (!this.showingAlert) {
        this.showingAlert = true
        this.reloadCountdownStep()
      }
    })

    ConnectionAlertBus.$on(CONNECTION_ALERT_DISMISSED_EVENT, () => {
      this.aborted = true
    })
  },
  methods: {
    alertDismissed () {
      ConnectionAlertBus.$emit(CONNECTION_ALERT_DISMISSED_EVENT)
    },
    reloadCountdownStep () {
      setTimeout(() => {
        if (this.aborted) {
          this.stopAndResetReloadCountdown()
        } else if (this.reloadCountdown <= 0) {
          location.reload()
        } else {
          this.reloadCountdown--
          this.reloadCountdownStep()
        }
      }, 1000)
    },
    stopAndResetReloadCountdown () {
      this.showingAlert = false
      this.aborted = false
      this.reloadCountdown = CONNECTION_ISSUE_RELOAD_COUNTDOWN_SECONDS
    }
  }
})
</script>
