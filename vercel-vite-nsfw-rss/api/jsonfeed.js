import { createClient } from '@supabase/supabase-js'
import {appConfig} from '../public/js/config.js'

// 使用环境变量来存储Supabase的配置信息更为安全，这里假设你已经在Vercel项目设置中配置好了对应的环境变量
const supabaseUrl = process.env.SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

// 创建Supabase客户端实例
const supabase = createClient(supabaseUrl, supabaseAnonKey)

export default async (req, res) => {
    const { series } = req.query
    const { data, error } = await supabase
        .from('rss')
        .select('*')
        .eq('series', series)
        .order('date_published', { ascending: false })

    if (error) {
        console.error(error)
        res.status(500).json({ error: 'Failed to fetch RSS feeds' })
    } else {
        let obj = {
            version: 'https://jsonfeed.org/version/1.1',
            title: '',
            home_page_url: '',  
            feed_url: `vercel-vite-nsfw-rss.vercel.app/api/jsonfeed?series=${series}`,
            items: data
        }
        console.log(appConfig)
        let row = appConfig.homelist.filter(item => item.value == series)
        if(row.length > 0){
            obj.title = row[0].title
            obj.home_page_url = row[0].home_page_url
        }
       
        res.setHeader('Content-Type', 'application/json')
        res.status(200).json(obj)
    }
}