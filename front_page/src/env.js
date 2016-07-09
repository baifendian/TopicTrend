/**
 * 开发环境、线上环境的不同配置
 */

var env = {}

if (process.env.NODE_ENV === 'production') {

  /**
   * 线上环境
   */
  
  // 数据接口基础 URL
  env.baseUrl = '/api'

  // 页面根路径
  env.basePath = '/web-demo'

} else {

  /**
   * 开发环境
   */

  // 数据接口基础 URL
  env.baseUrl = 'http://192.168.188.166:8080/api'

  // 页面根路径
  env.basePath = '/'

}

module.exports = env