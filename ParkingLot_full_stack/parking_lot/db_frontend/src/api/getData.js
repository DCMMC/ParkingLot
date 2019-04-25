import request from '@/utils/request'

export function getParkings(data) {
  return request({
    url: '/getParkingsFilter',
    method: 'post',
    data
  })
}

export function updateParkingApi(data) {
  return request({
    url: '/updateParking',
    method: 'post',
    data
  })
}

export function getVehiclesApi(data) {
  var r = request({
    url: '/getVehicleFilter',
    method: 'post',
    data
  })
  r.then(res => console.log(res)).catch(res => console.log(res))
  return r
}

export function updateVehicleApi(data) {
  return request({
    url: '/updateVehicle',
    method: 'post',
    data
  })
}

export function rmVehicleApi(data) {
  return request({
    url: '/rmVehicle',
    method: 'post',
    data
  })
}

export function addVehicleApi(data) {
  return request({
    url: '/addVehicle',
    method: 'post',
    data
  })
}

export function getBillLog(data) {
  return request({
    url: '/getBillLogFilter',
    method: 'post',
    data
  })
}
