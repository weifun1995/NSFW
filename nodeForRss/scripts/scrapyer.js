import { retryAxiosRequestGet } from '../utils/https.js'
import dayjs from 'dayjs'
import { JSDOM } from 'jsdom'
import iconv from 'iconv-lite'


class AdultHub {
    constructor() {
        this.jav_10mu_paco = this.jav_10mu_paco.bind(this)
        this.jav_carib = this.jav_carib.bind(this)
        this.rarbg = 'https://rargb.to/search/?search=xxxadult'
        this.btsearch = 'https://en.btdig.com/search?order=0&q=xxxadult'
    }

    jav_10mu_paco = async (series) => {
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
        } else if (series == 'jav-paco'){
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
            obj.id = item.MovieID
            obj.title = item.Title
            obj.content_text = `时间：${item.Release} \n 番号：${item.MovieID}  \n 描述：${item.Desc}`
            obj.url = this.btsearch.replace('xxxadult', item.MovieID)
            let date = dayjs(item.Release)
            obj.date_published = date.toISOString()
            obj.external_url = `https://www.10musume.com/movies/${item.MovieID}/`
            obj.summary = `时间：${item.Release} 番号：${item.MovieID} `
            obj.image = item.ThumbHigh
            obj.tags = [item.Release, item.MovieID]
            child.push(obj)
        }
        result.items = child
        return result
    }

    jav_carib = async (series) => {
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
        let res = await retryAxiosRequestGet(url,{ responseType: 'arraybuffer' })
        if (!res.data) {
            return null
        }
     
        const jpHtml = iconv.decode(res.data, 'euc-jp')
        const dom = new JSDOM(jpHtml)
        const document = dom.window.document
      
        let child = []
        
        document.querySelectorAll('.entry').forEach((element, index)=> {
            let obj = {}
            let link = element.querySelector('a')
            if (!link.href) {
                return
            }
            let title = element.querySelector('.meta-title').textContent.trim()
            let ThumbHigh = element.querySelector('.media-image').src
            let MovieID = link.href.replace(/\/moviepages\/([^\/]+)\/index.html/, (match, captured) => {
                return captured
            })
            let Release = element.querySelector('.meta-data').textContent.trim()

            obj.id = link.href
            obj.title = title
            obj.content_text = `时间：${Release} \n 番号：${MovieID}  \n 描述：${title}`
            obj.url =this.btsearch.replace('xxxadult', MovieID)
            let date = dayjs(Release)
            obj.date_published = date.toISOString()
            obj.external_url = `https://www.caribbeancom.com/moviepages/${link}/`
            obj.summary = `时间：${Release} 番号：${MovieID} `
            obj.image = ThumbHigh
            obj.tags = [Release, MovieID]
            child.push(obj)
        })
        result.items = child
        return result
    }

    bdsm_hucows = async (series) => {
        console.log('执行')
        let url = 'https://www.hucows.com/updatespage/'
        let result = {
            "title": "BDSM - hucows(吸奶器)",
            "home_page_url": url,
        }
        let res = await retryAxiosRequestGet(url)
        if (!res.data) {
            return null
        }
        const dom = new JSDOM(res.data)
        const document = dom.window.document
              
        let child = []
        
        document.querySelectorAll('.row article').forEach((element, index)=> {
            let link = element.querySelector('a')
            let title = element.querySelector('h1').textContent.trim()
            let desc = element.querySelector('.entry-content p').textContent.trim()
            let Release = element.querySelector('.postmeta').textContent.replaceAll('\n', '').trim()
            // 去掉多余空格
            Release = Release.split(' ').filter(Boolean).join(' ')
            // 转为一般时间格式
            Release = dayjs(trimmedStr, 'D MMM YYYY').format('YYYY-MM-DD')
            let ThumbHigh = element.querySelector('img').src

            obj.id = link.href
            obj.title = title
            obj.content_text = `时间：${Release} \n 番号：${MovieID}  \n 描述：${title}`
            obj.url = this.rarbg.replace('xxxadult', 'hucows')
            let date = dayjs(Release)
            obj.date_published = date.toISOString()
            obj.external_url = link.href
            obj.summary = `时间：${Release} 番号：${MovieID} `
            obj.image = ThumbHigh
            obj.tags = [Release, MovieID]
            child.push(obj)
        })
        result.items = child
        return result
    }
    

    gyno_dollshub = async (series) => {
        let url
        let result
        if (series == 'gyno-gynoexclusive') {
            url = 'https://www.gynoexclusive.com/scenes'
            result = {
                "title": "妇科检查 - gynoexclusive(4K)",
                "home_page_url": url,
            }
        } else if ( series == 'gyno-maturegynoexam') {
            url = 'https://www.maturegynoexam.com/scenes'
            result = {
                "title": "妇科检查 - maturegynoexam",
                "home_page_url": url,
            }
        }

        let res = await retryAxiosRequestGet(url)
        if (!res.data) {
            return null
        }
        const dom = new JSDOM(res.data)
        const document = dom.window.document
              
        let child = []
        
        document.querySelectorAll('.sence-box').forEach((element, index)=> {
            let obj = {}
            let link = element.querySelector('a')
            let title = element.querySelector('h3').textContent.trim()
            let ThumbHigh = element.querySelector('img').src

            obj.id = link.href
            obj.title = title
            obj.content_text = title
            obj.url = obj.url = this.rarbg.replace('xxxadult', series)
            obj.external_url = link.href
            obj.image = ThumbHigh
            child.push(obj)
        })
        result.items = child
        return result

    }
}

const javHub = async (series) => {
    let avhub = new AdultHub()
    if (['jav-10mu', 'jav-paco'].includes(series)) {
        console.log('10mu and paco')
        return await avhub.jav_10mu_paco(series)
    }

    if (['jav-carib-pussy', 'jav-carib-anal', 'jav-carib-bodyCheck'].includes(series)) {
        console.log('carib')
        return await avhub.jav_carib(series)
    }

    if (['gyno-gynoexclusive', 'gyno-maturegynoexam'].includes(series)) {
        console.log('gyno_dollshub')
        return await avhub.gyno_dollshub(series)
    }

    if (typeof avhub[series] == 'function') {
        console.log('其它series')
        return await avhub[series]()
    } else {
        console.error(`不存在名为 ${series} 的方法`)
        return null
    }
}


export {
    javHub
}