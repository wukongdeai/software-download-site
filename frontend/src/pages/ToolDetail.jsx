import { useParams } from 'react-router-dom'
import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import axios from 'axios'
import ToolComments from '../components/ToolComments'
import ToolFavorite from '../components/ToolFavorite'
import ToolRating from '../components/ToolRating'
import ToolShare from '../components/ToolShare'

const ToolDetail = () => {
  const { id } = useParams()

  const { data: tool, isLoading } = useQuery(
    ['tool', id],
    async () => {
      const response = await axios.get(`/api/tools/${id}`)
      return response.data
    }
  )

  if (isLoading) {
    return (
      <div className="space-y-8">
        <div className="card animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="card animate-pulse">
            <div className="h-64 bg-gray-200 rounded-md mb-4"></div>
            <div className="space-y-4">
              <div className="h-6 bg-gray-200 rounded w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded w-full"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
            </div>
          </div>
          <div className="card animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
            <div className="space-y-2">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-4 bg-gray-200 rounded w-full"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!tool) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-600">工具未找到</h2>
        <Link to="/tools" className="text-blue-600 hover:text-blue-800 mt-4 inline-block">
          返回工具列表
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="card">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <img
              src={tool.icon}
              alt={tool.name}
              className="w-16 h-16"
            />
            <div>
              <h1 className="text-2xl font-bold">{tool.name}</h1>
              <div className="flex items-center gap-4 mt-2">
                <span className="text-sm text-gray-500">
                  {tool.is_free ? '免费' : '付费'}
                </span>
                <span className="text-sm text-gray-500">
                  分类：{tool.category?.name}
                </span>
                <ToolRating toolId={id} />
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <ToolFavorite toolId={id} />
            <ToolShare toolName={tool.name} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="card">
          <img
            src={tool.screenshot}
            alt={tool.name}
            className="w-full h-64 object-cover rounded-md mb-4"
          />
          <div className="prose max-w-none">
            <h3 className="text-lg font-semibold">工具介绍</h3>
            <p className="text-gray-600">{tool.description}</p>
            
            <h3 className="text-lg font-semibold mt-6">主要功能</h3>
            <ul className="list-disc list-inside text-gray-600">
              {tool.features?.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>

            <h3 className="text-lg font-semibold mt-6">使用场景</h3>
            <ul className="list-disc list-inside text-gray-600">
              {tool.use_cases?.map((useCase, index) => (
                <li key={index}>{useCase}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">基本信息</h3>
            <div className="space-y-4">
              <div>
                <span className="text-gray-500">官方网站：</span>
                <a
                  href={tool.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800"
                >
                  {tool.website}
                </a>
              </div>
              <div>
                <span className="text-gray-500">价格：</span>
                <span>{tool.pricing || (tool.is_free ? '免费' : '付费')}</span>
              </div>
              <div>
                <span className="text-gray-500">支持平台：</span>
                <span>{tool.platforms?.join('、')}</span>
              </div>
              <div>
                <span className="text-gray-500">标签：</span>
                <div className="flex flex-wrap gap-2 mt-2">
                  {tool.tags?.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-sm"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold mb-4">相关工具</h3>
            <div className="space-y-4">
              {tool.related_tools?.map((relatedTool) => (
                <Link
                  key={relatedTool._id}
                  to={`/tools/${relatedTool._id}`}
                  className="flex items-center gap-4 hover:bg-gray-50 p-2 rounded-md"
                >
                  <img
                    src={relatedTool.icon}
                    alt={relatedTool.name}
                    className="w-10 h-10"
                  />
                  <div>
                    <h4 className="font-medium">{relatedTool.name}</h4>
                    <p className="text-sm text-gray-600 line-clamp-1">
                      {relatedTool.description}
                    </p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>

      <ToolComments toolId={id} />
    </div>
  )
}

export default ToolDetail 