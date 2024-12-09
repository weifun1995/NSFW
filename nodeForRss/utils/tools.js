import { JSDOM } from 'jsdom'
import fs from 'fs'


const create_rss_xml = (data) => {
    const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>')
    const document = dom.window.document

    // 创建RSS根元素，并设置版本属性
    const rss = document.createElement('rss')
    rss.setAttribute('version', '2.0')

    // 创建channel元素
    const channel = document.createElement('channel')

    // 添加channel下的基本元素（title、link、description）
    const title = document.createElement('title')
    title.textContent = data.title

    channel.appendChild(title)

    const link = document.createElement('xxxlink')
    link.textContent = data.link
    channel.appendChild(link)

    const description = document.createElement('description')
    description.textContent = data.desc
    channel.appendChild(description)

    // 遍历新闻数据，构建新闻条目并添加到channel元素下
    data.item.forEach((item) => {
        const itemElem = document.createElement('item')
        const itemTitle = document.createElement('title')
        itemTitle.textContent = item.itemTitle
        itemElem.appendChild(itemTitle)

        const itemLink = document.createElement('xxxlink')
        itemLink.textContent = item.itemLink
        itemElem.appendChild(itemLink)

        const itemDescription = document.createElement('description')
        itemDescription.textContent = item.itemDesc
        itemElem.appendChild(itemDescription)

        // 假设这里有个函数 convertToRSSDate 可将日期转换为 RSS 格式，如前文所述用 dayjs 等工具实现
        const pubDate = document.createElement('pubDate')
        pubDate.textContent = item.itemPubDate
        itemElem.appendChild(pubDate)

        channel.appendChild(itemElem)
    })

    // 将channel元素添加到rss元素下
    rss.appendChild(channel)

    // 将构建好的rss元素添加到虚拟DOM的body元素中（这一步非必要，只是为了完整模拟DOM结构）
    document.body.appendChild(rss)

    // 获取最终的XML字符串
    const xml = dom.serialize()
    const startIndex = xml.indexOf('<rss')
    const endIndex = xml.lastIndexOf('</rss>') + '</rss>'.length
    const rssXml = xml.substring(startIndex, endIndex).replaceAll('xxxlink', 'link')
    file_write('n.xml', rssXml)
    return rssXml
}

const file_write = (filename, filedata) => {
    fs.writeFile(filename, filedata, 'utf8', (err) => {
        if (err) {
            console.error('文件异步写入失败:', err)
        } else {
            console.log('文件异步写入成功')
        }
    })
}

export {
    create_rss_xml,
    file_write
}