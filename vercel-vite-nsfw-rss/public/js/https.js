 
import axios from "axios"
 
 const maxRepaly = 10
 
 

//  axios - get 请求 最多尝试10次
 const retryAxiosRequestGet = async (url, options = {}) => {
    let retryCount = 0
    while (retryCount < maxRepaly) {
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

// 

export {
    retryAxiosRequestGet
}