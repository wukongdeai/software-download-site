import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    username: (state) => state.user?.username || '',
    isAdmin: (state) => state.user?.is_admin || false
  },

  actions: {
    async login(username, password) {
      try {
        const response = await fetch('/api/auth/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        })

        if (!response.ok) {
          throw new Error('登录失败')
        }

        const data = await response.json()
        this.token = data.access_token
        localStorage.setItem('token', data.access_token)

        // 获取用户信息
        const userResponse = await fetch('/api/auth/me', {
          headers: {
            'Authorization': `Bearer ${data.access_token}`
          }
        })

        if (!userResponse.ok) {
          throw new Error('获取用户信息失败')
        }

        const userData = await userResponse.json()
        this.user = userData
        localStorage.setItem('user', JSON.stringify(userData))

        return true
      } catch (error) {
        console.error('登录错误:', error)
        throw error
      }
    },

    async logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    async register(userData) {
      try {
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(userData)
        })

        if (!response.ok) {
          throw new Error('注册失败')
        }

        return true
      } catch (error) {
        console.error('注册错误:', error)
        throw error
      }
    }
  }
}) 