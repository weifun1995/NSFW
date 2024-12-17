// import {appConfig} from '../public/js/config.js'
// export default function handler(req, res) {
//     res.setHeader('Content-Type', 'application/json')
//     res.status(200).json(appConfig.homelist)
// }

import { createClient } from '@supabase/supabase-js'

// 使用环境变量来存储Supabase的配置信息更为安全，这里假设你已经在Vercel项目设置中配置好了对应的环境变量
const supabaseUrl = process.env.SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

// 创建Supabase客户端实例
const supabase = createClient(supabaseUrl, supabaseAnonKey)

export default async (req, res) => {
    try {
        let { data, error } = await supabase
            .from('home')
            .select('*')

        if (error) {
            console.error(error)
            res.status(500).json({ 'success': false, 'error': 'Failed to fetch home table' })
        } else {
            res.setHeader('Content-Type', 'application/json')
            res.status(200).json({ 'success': true, 'data': data })
        }
    } catch (error) {
        console.error(error)
        res.status(500).json({ 'success': false, 'error': 'Failed to fetch home table' })
    }
}
