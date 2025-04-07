import { useState } from 'react'
import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import axios from 'axios'
import EditProfileModal from '../components/EditProfileModal'
import ChangePasswordModal from '../components/ChangePasswordModal'

const Profile = () => {
  const [activeTab, setActiveTab] = useState('favorites')
  const [isEditProfileOpen, setIsEditProfileOpen] = useState(false)
  const [isChangePasswordOpen, setIsChangePasswordOpen] = useState(false)

  const { data: user, isLoading: isUserLoading } = useQuery(
    'user',
    async () => {
      const response = await axios.get('/api/users/me')
      return response.data
    }
  )

  const { data: favorites, isLoading: isFavoritesLoading } = useQuery(
    ['favorites', activeTab],
    async () => {
      if (activeTab === 'favorites') {
        const response = await axios.get('/api/users/me/favorites')
        return response.data
      }
      return []
    }
  )

  const { data: comments, isLoading: isCommentsLoading } = useQuery(
    ['comments', activeTab],
    async () => {
      if (activeTab === 'comments') {
        const response = await axios.get('/api/users/me/comments')
        return response.data
      }
      return []
    }
  )

  if (isUserLoading) {
    return (
      <div className="space-y-8">
        <div className="card animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="card">
        <div className="flex items-center gap-6">
          <div className="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center">
            <span className="text-2xl text-gray-500">
              {user?.username?.[0]?.toUpperCase()}
            </span>
          </div>
          <div>
            <h1 className="text-2xl font-bold">{user?.username}</h1>
            <p className="text-gray-600 mt-1">{user?.email}</p>
            <div className="flex gap-4 mt-4">
              <button
                onClick={() => setIsEditProfileOpen(true)}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                编辑资料
              </button>
              <button
                onClick={() => setIsChangePasswordOpen(true)}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                修改密码
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => setActiveTab('favorites')}
              className={`py-4 px-6 text-sm font-medium ${
                activeTab === 'favorites'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              我的收藏
            </button>
            <button
              onClick={() => setActiveTab('comments')}
              className={`py-4 px-6 text-sm font-medium ${
                activeTab === 'comments'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              我的评论
            </button>
          </nav>
        </div>

        <div className="mt-6">
          {activeTab === 'favorites' ? (
            isFavoritesLoading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="card animate-pulse">
                    <div className="h-48 bg-gray-200 rounded-md mb-4"></div>
                    <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded w-full"></div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {favorites?.map((tool) => (
                  <Link
                    key={tool._id}
                    to={`/tools/${tool._id}`}
                    className="card hover:shadow-lg transition-shadow"
                  >
                    <img
                      src={tool.icon}
                      alt={tool.name}
                      className="w-full h-48 object-cover rounded-md mb-4"
                    />
                    <h3 className="font-semibold">{tool.name}</h3>
                    <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                      {tool.description}
                    </p>
                    <div className="mt-4 flex items-center justify-between">
                      <span className="text-sm text-gray-500">
                        {tool.is_free ? '免费' : '付费'}
                      </span>
                      <span className="text-sm text-blue-600">查看详情</span>
                    </div>
                  </Link>
                ))}
              </div>
            )
          ) : (
            isCommentsLoading ? (
              <div className="space-y-4">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="card animate-pulse">
                    <div className="h-6 bg-gray-200 rounded w-1/4 mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded w-full"></div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="space-y-4">
                {comments?.map((comment) => (
                  <div key={comment._id} className="card">
                    <div className="flex items-center justify-between">
                      <Link
                        to={`/tools/${comment.tool._id}`}
                        className="font-medium hover:text-blue-600"
                      >
                        {comment.tool.name}
                      </Link>
                      <span className="text-sm text-gray-500">
                        {new Date(comment.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="text-gray-600 mt-2">{comment.content}</p>
                  </div>
                ))}
              </div>
            )
          )}
        </div>
      </div>

      <EditProfileModal
        isOpen={isEditProfileOpen}
        onClose={() => setIsEditProfileOpen(false)}
        user={user}
      />

      <ChangePasswordModal
        isOpen={isChangePasswordOpen}
        onClose={() => setIsChangePasswordOpen(false)}
      />
    </div>
  )
}

export default Profile 