import { Link } from 'react-router-dom'
import { useState } from 'react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-2xl font-bold text-blue-600">
            AI Hub
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-8">
            <Link to="/tools" className="nav-link">
              工具
            </Link>
            <Link to="/categories" className="nav-link">
              分类
            </Link>
            <Link to="/login" className="nav-link">
              登录
            </Link>
            <Link to="/register" className="btn btn-primary">
              注册
            </Link>
          </div>

          {/* Mobile Navigation Button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-600 hover:text-blue-600"
            >
              {isOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-4">
            <Link to="/tools" className="block nav-link">
              工具
            </Link>
            <Link to="/categories" className="block nav-link">
              分类
            </Link>
            <Link to="/login" className="block nav-link">
              登录
            </Link>
            <Link to="/register" className="block btn btn-primary">
              注册
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar 