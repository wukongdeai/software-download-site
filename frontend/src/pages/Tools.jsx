import { useState } from 'react'
import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import axios from 'axios'

const Tools = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const pageSize = 12

  const { data: categories } = useQuery(
    'categories',
    async () => {
      const response = await axios.get('/api/categories')
      return response.data
    }
  )

  const { data: tools, isLoading } = useQuery(
    ['tools', searchQuery, selectedCategory, currentPage],
    async () => {
      const params = new URLSearchParams({
        page: currentPage,
        page_size: pageSize,
      })
      if (searchQuery) params.append('search', searchQuery)
      if (selectedCategory) params.append('category_id', selectedCategory)
      
      const response = await axios.get(`/api/tools?${params.toString()}`)
      return response.data
    }
  )

  const handleSearch = (e) => {
    e.preventDefault()
    setCurrentPage(1)
  }

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value)
    setCurrentPage(1)
  }

  const totalPages = Math.ceil((tools?.total || 0) / pageSize)

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">AI工具</h1>
      </div>

      <div className="card">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="flex flex-col md:flex-row gap-4">
            <input
              type="text"
              placeholder="搜索工具..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <select
              value={selectedCategory}
              onChange={handleCategoryChange}
              className="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">所有分类</option>
              {categories?.map((category) => (
                <option key={category._id} value={category._id}>
                  {category.name}
                </option>
              ))}
            </select>
            <button
              type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              搜索
            </button>
          </div>
        </form>
      </div>

      {isLoading ? (
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
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {tools?.items?.map((tool) => (
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

          {tools?.items?.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-600">未找到相关工具</p>
            </div>
          )}

          {totalPages > 1 && (
            <div className="flex justify-center mt-8">
              <div className="flex gap-2">
                <button
                  onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  className="px-4 py-2 border rounded-md disabled:opacity-50"
                >
                  上一页
                </button>
                <span className="px-4 py-2">
                  第 {currentPage} 页，共 {totalPages} 页
                </span>
                <button
                  onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  className="px-4 py-2 border rounded-md disabled:opacity-50"
                >
                  下一页
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default Tools 