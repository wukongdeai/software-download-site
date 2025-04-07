import { useParams } from 'react-router-dom'
import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import axios from 'axios'

const CategoryDetail = () => {
  const { id } = useParams()

  const { data: category, isLoading: isCategoryLoading } = useQuery(
    ['category', id],
    async () => {
      const response = await axios.get(`/api/categories/${id}`)
      return response.data
    }
  )

  const { data: tools, isLoading: isToolsLoading } = useQuery(
    ['category-tools', id],
    async () => {
      const response = await axios.get(`/api/tools?category_id=${id}`)
      return response.data
    }
  )

  if (isCategoryLoading || isToolsLoading) {
    return (
      <div className="space-y-8">
        <div className="card animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-48 bg-gray-200 rounded-md mb-4"></div>
              <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-full"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (!category) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-600">分类未找到</h2>
        <Link to="/categories" className="text-blue-600 hover:text-blue-800 mt-4 inline-block">
          返回分类列表
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="card">
        <div className="flex items-center gap-4">
          <img
            src={category.icon}
            alt={category.name}
            className="w-16 h-16"
          />
          <div>
            <h1 className="text-2xl font-bold">{category.name}</h1>
            <p className="text-gray-600 mt-2">{category.description}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tools?.map((tool) => (
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

      {tools?.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600">该分类下暂无工具</p>
        </div>
      )}
    </div>
  )
}

export default CategoryDetail 