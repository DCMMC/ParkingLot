import request from '@/utils/request'

export function login(data) {
  // DCMMC: 更改这些 url, 和后端绑定, 现在暂时在前端 mock 模拟
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

