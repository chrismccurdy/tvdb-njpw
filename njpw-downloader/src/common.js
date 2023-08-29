import { ref } from 'vue'

export function errorCallback(error, errorAlert) {
  console.log(error)
  errorAlert.value.setMessage(error)
}

export function hideError(errorAlert) {
  errorAlert.value.hideMessage()
}

export function showMessage(alertBox, message, timeoutSeconds) {
  alertBox.value.setMessage(message)
  setTimeout(() => {
    alertBox.value.hideMessage()
  }, timeoutSeconds * 1000)
}

export function useSuccessAlert() {
  const successRef = ref(null)
  const successAlert = {
    alert: successRef,
    show: (msg, timeoutSeconds) => {
      successRef.value.setMessage(msg)
      setTimeout(() => {
        successRef.value.hideMessage()
      }, timeoutSeconds * 1000)
    }
  }
  return successAlert
}

export function useErrorAlert() {
  const errorRef = ref(null)
  const errorAlert = {
    alert: errorRef,
    hide: () => {
      errorRef.value.hideMessage()
    },
    show: (msg) => {
      console.log(msg)
      errorRef.value.setMessage(msg)
    }
  }
  return errorAlert
}

export function useAlerts() {
  const success = useSuccessAlert()
  const error = useErrorAlert()
  return { success, error }
}
