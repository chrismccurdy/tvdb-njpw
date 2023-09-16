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
    if (alertBox.value) {
      alertBox.value.hideMessage()
    }
  }, timeoutSeconds * 1000)
}

export function useSuccessAlert() {
  const successRef = ref(null)
  const successAlert = {
    alert: successRef,
    show: (msg, timeoutSeconds) => {
      successRef.value.setMessage(msg)
      setTimeout(() => {
        if (successRef.value) {
          successRef.value.hideMessage()
        }
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

const progressVisible = ref(false)
const progressToast = {
  visible: progressVisible,
  show: () => (progressVisible.value = true),
  hide: () => (progressVisible.value = false)
}

export function useProgressToast() {
  return progressToast
}

export function filtered(filters, episodeList) {
  let filteredEpisodes = episodeList
  if (filters.series && filters.series.length > 0) {
    filteredEpisodes = filteredEpisodes.filter(
      (ep) => ep.series && (ep.series.title == filters.series || ep.series.name == filters.series)
    )
  }
  if (filters.year && filters.year.length > 0) {
    filteredEpisodes = filteredEpisodes.filter(
      (ep) => ep.air_date != null && ep.air_date.startsWith(filters.year)
    )
  }
  if (filters.month && filters.month.length > 0) {
    filteredEpisodes = filteredEpisodes.filter(
      (ep) => ep.air_date != null && ep.air_date.substring(5, 7) == filters.month
    )
  }
  if (!filters.hidden) {
    filteredEpisodes = filteredEpisodes.filter((ep) => !ep.hidden)
  }
  return filteredEpisodes
}
