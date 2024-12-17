import axios from "axios"
import dayjs from "dayjs"
import { JSDOM } from 'jsdom'
import iconv from 'iconv-lite'
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

// 创建Supabase客户端实例
const supabase = createClient(supabaseUrl, supabaseAnonKey)


const config = {
    maxRepaly: 10,
    rarbg: 'https://rargb.to/search/?search=xxxadult',
    btsearch: 'https://en.btdig.com/search?order=0&q=xxxadult'
}


//  axios - get 请求 最多尝试10次
const retryAxiosRequestGet = async (url, options = {}) => {
    let retryCount = 0
    while (retryCount < config.maxRepaly) {
        try {
            const response = await axios.get(url, options)
            return response
        } catch (error) {
            console.log(`Get 请求重试中...  (${retryCount + 1}/10)`)
            retryCount++
        }
    }
    // throw new Error('Max retry attempts reached, request still failed.')
    console.error('已经重试 10 次，仍然失败，请检查代理网络')
    return null
}

function retryAxiosRequestGetPrimise(url) {
    return new Promise((resolve, reject) => {
        // 这里可以放置具体的axios请求以及重试逻辑等代码
        // 例如：
        let retryCount = 0
        const doRequest = async () => {
            try {
                const response = await axios.get(url)
                resolve(response.data)
            } catch (error) {
                if (retryCount < 10) {
                    retryCount++
                    doRequest()
                } else {
                    reject(error)
                }
            }
        }
        doRequest()
    })
}


const jav_10mu_paco = async (series) => {
    console.log('系列', series)
    let url
    let result
    if (series == 'jav-10mu') {
        url = 'https://www.10musume.com/dyn/phpauto/movie_lists/series/list_313_0.json'
        result = {
            "title": "秘蔵マンコセレクション",
            "home_page_url": url,
            "description": "10mu 秘蔵 阴道图鉴",
        }
    } else if (series == 'jav-paco') {
        url = 'https://www.pacopacomama.com/dyn/phpauto/movie_lists/series/list_589_0.json'
        result = {
            "title": "人妻マンコ図鑑",
            "home_page_url": url,
            "description": "paco 人妻 阴道图鉴",
        }
    } else {
        return null
    }
    let res = await retryAxiosRequestGet(url)
    if (!res.data) {
        return null
    }
    let data = res.data

    let child = []
    for (let item of data.Rows) {
        let obj = {}
        obj.id = series.replace('jav-', '') + '_' + item.MovieID
        obj.title = item.Title
        obj.content_text = `时间：${item.Release} \n 番号：${item.MovieID}  \n 描述：${item.Desc}`
        obj.url = config.btsearch.replace('xxxadult', item.MovieID)
        let date = dayjs(item.Release)
        obj.date_published = date.toISOString()
        obj.external_url = `https://www.10musume.com/movies/${item.MovieID}/`
        obj.summary = `时间：${item.Release} 番号：${item.MovieID} `
        obj.image = item.ThumbHigh
        child.push(obj)
    }
    result.items = child
    return result
}

const jav_carib = async (series) => {
    let url
    let result
    if (series == 'jav-carib-pussy') {
        url = 'https://www.caribbeancom.com/series/989/index.html'
        result = {
            "title": "マンコ図鑑(阴道)",
            "home_page_url": url,
            "description": "carib マンコ図鑑 阴道图鉴",
        }
    } else if (series == 'jav-carib-anal') {
        url = 'https://www.caribbeancom.com/series/1076/index.html'
        result = {
            "title": "アナル図鑑(肛门)",
            "home_page_url": url,
            "description": "carib アナル図鑑 肛门图鉴",
        }
    } else if (series == 'jav-carib-bodyCheck') {
        url = 'https://www.caribbeancom.com/series/1091/index.html'
        result = {
            "title": "セクシー女優エンサイクロペディア(女优测量)",
            "home_page_url": url,
            "description": "carib セクシー女優エンサイクロペディア 女优测量",
        }
    } else {
        return null
    }
    let res = await retryAxiosRequestGet(url, { responseType: 'arraybuffer' })
    if (!res.data) {
        return null
    }

    const jpHtml = iconv.decode(res.data, 'euc-jp')
    const dom = new JSDOM(jpHtml)
    const document = dom.window.document

    let child = []

    document.querySelectorAll('.entry').forEach((element, index) => {
        let obj = {}
        let link = element.querySelector('a')
        if (!link.href) {
            return
        }
        let title = element.querySelector('.meta-title').textContent.trim()
        let MovieID = link.href.replace(/\/moviepages\/([^\/]+)\/index.html/, (match, captured) => {
            return captured
        })
        // let ThumbHigh = element.querySelector('.media-image').src
        let ThumbHigh = `https://www.caribbeancom.com/moviepages/${MovieID}/images/l_l.jpg`
        let Release = element.querySelector('.meta-data').textContent.trim()

        obj.id = 'carib_' + MovieID
        obj.title = title
        obj.content_text = `时间：${Release} \n 番号：${MovieID}  \n 描述：${title}`
        obj.url = config.btsearch.replace('xxxadult', MovieID)
        let date = dayjs(Release)
        obj.date_published = date.toISOString()
        obj.external_url = `https://www.caribbeancom.com/moviepages/${link}/`
        obj.summary = `时间：${Release} 番号：${MovieID} `
        obj.image = ThumbHigh
        child.push(obj)
    })
    result.items = child
    return result
}

const gyno_dollshub = async (series) => {
    let url
    let result
    if (series == 'gyno-gynoexclusive') {
        url = 'https://www.gynoexclusive.com/scenes'
        result = {
            "title": "妇科检查 - gynoexclusive(4K)",
            "home_page_url": url,
        }
    } else if (series == 'gyno-maturegynoexam') {
        url = 'https://www.maturegynoexam.com/scenes'
        result = {
            "title": "妇科检查 - maturegynoexam",
            "home_page_url": url,
        }
    }

    const parseData = (data) => {
        const dom = new JSDOM(data)
        const document = dom.window.document
        let child = []

        document.querySelectorAll('.sence-box').forEach((element, index) => {
            let obj = {}
            let link = element.querySelector('a')
            let title = element.querySelector('h3').textContent.trim()
            let ThumbHigh = element.querySelector('img').src

            obj.id = series.replace('gyno-', '') + '_' + title
            obj.title = title
            obj.content_text = title
            obj.url = obj.url = config.rarbg.replace('xxxadult', series)
            obj.external_url = link.href
            obj.image = ThumbHigh
            child.push(obj)
        })
        return child
    }

    const url1 = url
    const url2 = `${url}?page=2`
    const url3 = `${url}?page=3`


    let child = []
    try {
        // 使用await等待所有接口请求完成
        const results = await Promise.all([
            retryAxiosRequestGetPrimise(url1),
            retryAxiosRequestGetPrimise(url2),
            retryAxiosRequestGetPrimise(url3)
        ])

        results.forEach(item => {
            let temp = parseData(item)
            child = child.concat(temp)
        })
    } catch (error) {
        console.error('有接口请求失败：', error)
    }
    result.items = child
    return result

}

const bdsm_hucows = async (series) => {
    let url = 'https://www.hucows.com/updatespage/'

    const url1 = url
    const url2 = `${url}page/2/`
    const url3 = `${url}page/3/`

    let result = {
        "title": "BDSM - hucows(吸奶器)",
        "home_page_url": url,
    }

    const parseData = (data) => {
        let child = []
        const dom = new JSDOM(res.data)
        const document = dom.window.document
        document.querySelectorAll('.row article').forEach((element, index) => {
            let obj = {}
            let link = element.querySelector('a')
            let title = element.querySelector('h1').textContent.trim()
            let desc = element.querySelector('.entry-content p').textContent.trim()
            let Release = element.querySelector('.postmeta').textContent.replaceAll('\n', '').trim()
            // 去掉多余空格
            Release = Release.split(' ').filter(Boolean).join(' ')
            // 转为一般时间格式
            Release = dayjs(Release, 'D MMM YYYY').format('YYYY-MM-DD')
            let ThumbHigh = element.querySelector('img').src
    
            obj.id = 'hucows_' + Release.replaceAll('-', '')
            obj.title = title
            obj.content_text = `时间：${Release}  \n 描述：${title}`
            obj.url = config.rarbg.replace('xxxadult', 'hucows')
            let date = dayjs(Release)
            obj.date_published = date.toISOString()
            obj.external_url = link.href
            obj.summary = `时间：${Release} 描述：${title} `
            obj.image = ThumbHigh
            child.push(obj)
        })
        return child
    }

    let child = []
    try {
        // 使用await等待所有接口请求完成
        const results = await Promise.all([
            retryAxiosRequestGetPrimise(url1),
            retryAxiosRequestGetPrimise(url2),
            retryAxiosRequestGetPrimise(url3)
        ])
        results.forEach(item => {
            let temp = parseData(item)
            child = child.concat(temp)
        })
    } catch (error) {
        console.error('有接口请求失败：', error)
    }

    result.items = child
    return result
}

export default async (request, response) => {
    let { series } = request.query
    let result = null

    try {
        if (['jav-10mu', 'jav-paco'].includes(series)) {
            result = await jav_10mu_paco(series)
        }

        if (['jav-carib-pussy', 'jav-carib-anal', 'jav-carib-bodyCheck'].includes(series)) {
            result = await jav_carib(series)
        }

        if (['gyno-gynoexclusive', 'gyno-maturegynoexam'].includes(series)) {
            result = await gyno_dollshub(series)
        }

        if (['bdsm-hucows'].includes(series)) {
            result = await bdsm_hucows(series)
        }

        console.log('result', result)

        if (result) {
            let rows = result.items
            rows.map(item => {
                item.series = series
            })

            console.log('rows', rows.length)

            // 进行数据保存
            if (rows.length > 0) {
                console.log('开始保存数据到Supabase')
                try {
                    // 数据保存到rss
                    const { data, error } = await supabase
                        .from('rss')
                        .upsert(rows, { onConflict: 'id' })
                        .select()

                    console.log('Supabase-tabel-rss数据保存成功:', data, error)


                    // 更新时间到 home
                    let now = dayjs().format('YYYY-MM-DD')
                    const { dataT, errorT } = await supabase
                        .from('home')
                        .update({ 'last_update_time': now })
                        .eq('id', series)
                        .select()
                    if (!errorT) {
                        console.log('Supabase-tabel-home数据更新成功:')
                    }
                    response.status(200).json({ 'success': true, 'data': data })

                } catch (error) {
                    console.error('连接Supabase出现错误:', error)
                    response.status(500).json({ 'success': false, 'data': error })
                }
            }
        } else {
            response.status(200).json({ 'success': false, 'message': '查询数据失败' })
        }
    } catch (error) {
        response.status(500).json({ 'success': false, 'message': error })
    }


}