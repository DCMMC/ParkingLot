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
  return request({
    url: '/getVehicleFilter',
    method: 'post',
    data
  })
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

export function getMemberCardApi(data) {
  return request({
    url: '/getMemberCard',
    method: 'post',
    data
  })
}

export function rmMemberCardApi(data) {
  return request({
    url: '/rmMemberCard',
    method: 'post',
    data
  })
}

export function updateMemberCardApi(data) {
  return request({
    url: '/updateMemberCard',
    method: 'post',
    data
  })
}

export function addMemberCardApi(data) {
  return request({
    url: '/addMemberCard',
    method: 'post',
    data
  })
}

export function getMemberCardLog(data) {
  return request({
    url: '/getMemberCardLog',
    method: 'post',
    data
  })
}

export function getParkingLotLog(data) {
  return request({
    url: '/getParkingLotLog',
    method: 'post',
    data
  })
}
