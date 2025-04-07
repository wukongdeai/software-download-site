import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios'

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    try {
      const response = await axios.post('/api/auth/token', {
        username: formData.username,
        password: formData.password,
      })

      // 存储token
      localStorage.setItem('token', response.data.access_token)
      
      // 重定向到首页
      navigate('/')
    } catch (err) {
      setError('用户名或密码错误')
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="card">
        <h2 className="text-2xl font-bold mb-6 text-center">登录</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
              用户名
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="input"
              required
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              密码
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="input"
              required
            />
          </div>

          <button type="submit" className="btn btn-primary w-full">
            登录
          </button>
        </form>

        <div className="mt-4 text-center">
          <p className="text-sm text-gray-600">
            还没有账号？{' '}
            <Link to="/register" className="text-blue-600 hover:text-blue-800">
              立即注册
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login 