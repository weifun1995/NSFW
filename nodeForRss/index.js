import Koa from 'koa'
import serve from 'koa-static'
import Router from 'koa-router'
import json from 'koa-json'
import { uploadFileToGitHub } from './utils/github.js'
import { appConfig } from './scripts/config.js'
global.appConfig = appConfig
import { javHub } from './scripts/scrapyer.js'
// 添加环境变量处理
const isProd = process.env.NODE_ENV === 'production'
if (!isProd) {
    import('dotenv').then(({ config }) => config()) // 加载 .env 文件中的变量
}

const app = new Koa()
const router = new Router()

app.use(serve('.'))

// 定义一个简单的中间件，记录请求的日志
app.use(async (ctx, next) => {
    console.log(`当前请求路径： ${ctx.url}`)
    if (ctx.path === '/') {
        ctx.type = 'html'
        ctx.body = await new Promise((resolve, reject) => {
            // 使用fs模块读取index.html文件内容（此处需导入fs模块）
            import('fs').then(({ default: fs }) => {
                fs.readFile('index.html', 'utf8', (err, data) => {
                    if (err) {
                        reject(err)
                    } else {
                        resolve(data)
                    }
                })
            })
        })
    }
    await next()
})


router.get('/scrapyer', async (ctx) => {
    const series = ctx.query.series
    if (series) {
        // 调用内部方法获取返回值
        const result = await javHub(series)
        if (result.success) {       
            result.version = "https://jsonfeed.org/version/1.1"
            result.feed_url = `${appConfig.storeRaw}/${series}.json`

            console.log(result)

            let github = await uploadFileToGitHub(`${series}.json`, JSON.stringify(result))
            ctx.body = github
        } else {
            ctx.body = {
                'success': false,
                'data': result.message
            }
        }
    } else {
        ctx.body = {
            'success': false,
            'data': '请传入series参数'
        }
    }
})

router.get('/link', async (ctx) => {
    let list = appConfig.list
    list.map((item)=> {
        item.link = `${global.appConfig.storeRaw}/${item.value}.json`
    })
    console.log(list)
    ctx.body = list
})


router.get('/github', async (ctx) => {
    const series = ctx.query.series
    return await uploadFileToGitHub('a.txt', '这是测试文本')
})

app.use(json())
app.use(router.routes()).use(router.allowedMethods())

// 创建一个处理函数
const handler = app.callback()

// 修改服务器启动逻辑
if (!isProd) {
    const port = process.env.PORT || 4090
    app.listen(port, () => {
        console.log(`Server running on http://localhost:${port}`)
    })
}

// 导出处理函数
export default handler