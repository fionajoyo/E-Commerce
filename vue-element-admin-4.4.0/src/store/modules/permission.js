import { asyncRoutes, constantRoutes } from '@/router'

/**
 * Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes({ commit }, roles) {
    return new Promise(resolve => {
      // 过滤出来的路由
      let accessedRoutes
      if (roles.includes('admin')) {
        // 如果是管理员用户则不进行过滤
        console.log('管理员登录')
        accessedRoutes = asyncRoutes || []
      } else {
        // 如果不是管理员则进行过滤
        console.log('非管理员登录')
        accessedRoutes = []
      }
      commit('SET_ROUTES', accessedRoutes)
      resolve(accessedRoutes)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
