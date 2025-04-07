import { useMutation, useQuery, useQueryClient } from 'react-query'
import axios from 'axios'

const ToolFavorite = ({ toolId }) => {
  const queryClient = useQueryClient()

  const { data: isFavorite } = useQuery(
    ['favorite', toolId],
    async () => {
      try {
        const response = await axios.get(`/api/tools/${toolId}/favorite`)
        return response.data.is_favorite
      } catch (error) {
        return false
      }
    }
  )

  const toggleFavoriteMutation = useMutation(
    async () => {
      if (isFavorite) {
        await axios.delete(`/api/tools/${toolId}/favorite`)
      } else {
        await axios.post(`/api/tools/${toolId}/favorite`)
      }
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['favorite', toolId])
        queryClient.invalidateQueries('user')
      },
    }
  )

  const handleToggleFavorite = () => {
    toggleFavoriteMutation.mutate()
  }

  return (
    <button
      onClick={handleToggleFavorite}
      disabled={toggleFavoriteMutation.isLoading}
      className={`flex items-center gap-2 px-4 py-2 rounded-md ${
        isFavorite
          ? 'bg-red-100 text-red-700 hover:bg-red-200'
          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      }`}
    >
      {toggleFavoriteMutation.isLoading ? (
        <svg
          className="animate-spin h-5 w-5"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      ) : (
        <svg
          className="h-5 w-5"
          fill={isFavorite ? 'currentColor' : 'none'}
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
          />
        </svg>
      )}
      <span>{isFavorite ? '取消收藏' : '收藏'}</span>
    </button>
  )
}

export default ToolFavorite 