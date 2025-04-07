import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import axios from 'axios'

const Categories = () => {
  const { data: categories, isLoading } = useQuery(
    'categories',
    async () => {
      const response = await axios.get('/api/categories')
      return response.data
    }
  )

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="card animate-pulse">
            <div className="h-32 bg-gray-200 rounded-md"></div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">分类</h1>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {categories?.map((category) => (
          <Link
            key={category._id}
            to={`/categories/${category._id}`}
            className="card text-center hover:shadow-lg transition-shadow"
          >
            <img
              src={category.icon}
              alt={category.name}
              className="w-16 h-16 mx-auto mb-4"
            />
            <h3 className="font-semibold">{category.name}</h3>
            <p className="text-sm text-gray-600 mt-2">
              {category.description}
            </p>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default Categories 