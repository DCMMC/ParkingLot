import request from '@/utils/request'

export const getParkings = data => request({
  url: '/getParkingsFilter',
  method: 'post',
  data
})

export function updateParkingApi(data) {
  request({
    url: '/updateParking',
    method: 'post',
    data
  })
}

export function getVehiclesApi(data) {
  request({
    url: '/getVehicleFilter',
    method: 'post',
    data
  })
}

export function updateVehicleApi(data) {
  request({
    url: '/updateVehicle',
    method: 'post',
    data
  })
}

export function rmVehicleApi(data) {
  request({
    url: '/rmVehicle',
    method: 'post',
    data
  })
}

export function addVehicleApi(data) {
  request({
    url: '/addVehicle',
    method: 'post',
    data
  })
}

export function getBillLog(data) {
  request({
    url: '/getBillLogFilter',
    method: 'post',
    data
  })
}
