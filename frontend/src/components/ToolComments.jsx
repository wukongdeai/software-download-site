import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import axios from 'axios'

const ToolComments = ({ toolId }) => {
  const [comment, setComment] = useState('')
  const [error, setError] = useState('')

  const queryClient = useQueryClient()

  const { data: comments, isLoading } = useQuery(
    ['comments', toolId],
    async () => {
      const response = await axios.get(`/api/tools/${toolId}/comments`)
      return response.data
    }
  )

  const addCommentMutation = useMutation(
    async (content) => {
      const response = await axios.post(`/api/tools/${toolId}/comments`, {
        content,
      })
      return response.data
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['comments', toolId])
        setComment('')
        setError('')
      },
      onError: (error) => {
        setError(error.response?.data?.detail || '发表评论失败')
      },
    }
  )

  const deleteCommentMutation = useMutation(
    async (commentId) => {
      await axios.delete(`/api/tools/${toolId}/comments/${commentId}`)
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['comments', toolId])
      },
    }
  )

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!comment.trim()) {
      setError('评论内容不能为空')
      return
    }
    addCommentMutation.mutate(comment.trim())
  }

  const handleDelete = (commentId) => {
    if (window.confirm('确定要删除这条评论吗？')) {
      deleteCommentMutation.mutate(commentId)
    }
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">发表评论</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-3 bg-red-100 text-red-700 rounded-md">
              {error}
            </div>
          )}
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="写下你的评论..."
            className="w-full h-32 p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={addCommentMutation.isLoading}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {addCommentMutation.isLoading ? '发表中...' : '发表评论'}
            </button>
          </div>
        </form>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-semibold">评论列表</h3>
        {isLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-1/4 mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-full"></div>
              </div>
            ))}
          </div>
        ) : comments?.length > 0 ? (
          <div className="space-y-4">
            {comments.map((comment) => (
              <div key={comment._id} className="card">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                      <span className="text-sm text-gray-500">
                        {comment.user.username[0].toUpperCase()}
                      </span>
                    </div>
                    <span className="font-medium">{comment.user.username}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-500">
                      {new Date(comment.created_at).toLocaleString()}
                    </span>
                    {comment.user._id === queryClient.getQueryData('user')?._id && (
                      <button
                        onClick={() => handleDelete(comment._id)}
                        className="text-sm text-red-600 hover:text-red-800"
                      >
                        删除
                      </button>
                    )}
                  </div>
                </div>
                <p className="text-gray-600 mt-2">{comment.content}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            暂无评论
          </div>
        )}
      </div>
    </div>
  )
}

export default ToolComments 