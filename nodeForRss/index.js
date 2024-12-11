// 引入Express模块
import express from 'express'
import cors from 'cors'
import { myUploadFileToGitHub } from './utils/github.js'
import { appConfig } from './scripts/config.js'
global.appConfig = appConfig
import { javHub } from './scripts/scrapyer.js'
// 添加环境变量处理
const isProd = process.env.NODE_ENV === 'production'
if (!isProd) {
    import('dotenv').then(({ config }) => config()) // 加载 .env 文件中的变量
}

// 创建Express应用实例
const app = express()

// 配置静态文件服务（用于提供index.html等静态文件访问）
app.use(express.static('.'))

// 使用 CORS 中间件
app.use(cors())

// 创建 /hello 的GET接口，接受name参数
// app.get('/', (req, res) => {
//     res.sendFile('index.html')
//   })

app.get('/scrapyer', async (req, res) => {
    const { series } = req.query
    if (series) {
        const scrapyerRes = await javHub(series)
        console.log('爬取结果', scrapyerRes)
        if (!scrapyerRes) {
            ctx.body = {
                'success': false,
                'data': `爬取网站：${series} 失败 , ${scrapyerRes?.message}`
            }
            return
        }
        scrapyerRes.version = "https://jsonfeed.org/version/1.1"
        scrapyerRes.feed_url = `${appConfig.storeRaw}/${series}.json`

        let githubRes = await myUploadFileToGitHub(`${series}.json`, JSON.stringify(scrapyerRes))
        res.json(githubRes)
    } else {
        res.json = {
            'success': false,
            'data': '请传入series参数'
        }
    }
})

app.get('/link', (req, res) => {
    let list = appConfig.list
    list.map((item)=> {
        item.link = `${global.appConfig.storeRaw}/${item.value}.json`
    })
    res.json(list)
})


// 启动服务器，监听端口3100
let port = 3000
const server = app.listen(port, () => {
    console.log(`Server is running on port ${port}`)
})

// 检查端口是否被占用，如果被占用则端口自动+1
server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        port++
        server.listen(port)
    }
})