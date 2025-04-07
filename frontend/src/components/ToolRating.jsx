import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from 'react-query'
import axios from 'axios'

const ToolRating = ({ toolId }) => {
  const [hoverRating, setHoverRating] = useState(0)
  const queryClient = useQueryClient()

  const { data: rating } = useQuery(
    ['rating', toolId],
    async () => {
      const response = await axios.get(`/api/tools/${toolId}/rating`)
      return response.data
    }
  )

  const rateMutation = useMutation(
    async (newRating) => {
      await axios.post(`/api/tools/${toolId}/rating`, { rating: newRating })
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['rating', toolId])
      },
    }
  )

  const handleRating = (newRating) => {
    rateMutation.mutate(newRating)
  }

  return (
    <div className="flex items-center gap-2">
      <div className="flex">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            className="focus:outline-none"
            onMouseEnter={() => setHoverRating(star)}
            onMouseLeave={() => setHoverRating(0)}
            onClick={() => handleRating(star)}
          >
            <svg
              className={`w-6 h-6 ${
                star <= (hoverRating || rating?.user_rating || 0)
                  ? 'text-yellow-400'
                  : 'text-gray-300'
              }`}
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
        ))}
      </div>
      <div className="text-sm text-gray-600">
        {rating?.average_rating ? (
          <span>
            平均评分：{rating.average_rating.toFixed(1)} ({rating.total_ratings} 人评分)
          </span>
        ) : (
          <span>暂无评分</span>
        )}
      </div>
    </div>
  )
}

export default ToolRating 