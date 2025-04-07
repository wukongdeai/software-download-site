import { useState } from 'react'
import { useLocation } from 'react-router-dom'

const ToolShare = ({ toolName }) => {
  const [copied, setCopied] = useState(false)
  const location = useLocation()
  const shareUrl = `${window.location.origin}${location.pathname}`

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('复制失败:', err)
    }
  }

  const shareToSocial = (platform) => {
    const text = `推荐一个AI工具：${toolName}`
    let url = ''

    switch (platform) {
      case 'weibo':
        url = `https://service.weibo.com/share/share.php?url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(text)}`
        break
      case 'wechat':
        // 这里需要集成微信分享SDK
        console.log('微信分享')
        return
      case 'qq':
        url = `https://connect.qq.com/widget/shareqq/index.html?url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(text)}`
        break
      default:
        return
    }

    window.open(url, '_blank', 'width=600,height=400')
  }

  return (
    <div className="flex items-center gap-2">
      <button
        onClick={handleCopy}
        className="flex items-center gap-1 px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
      >
        <svg
          className="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"
          />
        </svg>
        {copied ? '已复制' : '复制链接'}
      </button>

      <button
        onClick={() => shareToSocial('weibo')}
        className="flex items-center gap-1 px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
      >
        <svg
          className="w-4 h-4"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M10.096 19.927c-4.87 0-8.82-3.95-8.82-8.82s3.95-8.82 8.82-8.82 8.82 3.95 8.82 8.82-3.95 8.82-8.82 8.82zm0-16.24c-4.1 0-7.42 3.32-7.42 7.42s3.32 7.42 7.42 7.42 7.42-3.32 7.42-7.42-3.32-7.42-7.42-7.42zm-1.1 11.9l-1.1-1.1 2.2-2.2-2.2-2.2 1.1-1.1 2.2 2.2 2.2-2.2 1.1 1.1-2.2 2.2 2.2 2.2-1.1 1.1-2.2-2.2-2.2 2.2z" />
        </svg>
        分享到微博
      </button>

      <button
        onClick={() => shareToSocial('qq')}
        className="flex items-center gap-1 px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
      >
        <svg
          className="w-4 h-4"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" />
        </svg>
        分享到QQ
      </button>
    </div>
  )
}

export default ToolShare 