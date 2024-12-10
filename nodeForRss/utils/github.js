import { Octokit } from "@octokit/rest"
import axios from "axios"
import https from 'https'
import path from 'path'
import dayjs from 'dayjs'

// 创建一个可以忽略证书错误的代理
const ignoreCertificateAgent = new https.Agent({
    rejectUnauthorized: false
})


class GitHub {
    constructor() {
        this.octokit = this.init()
        this.uploadFileToGitHub = this.uploadFileToGitHub.bind(this)
    }
    // 初始化 octokit
    init() {
        let octokit = new Octokit({
            auth: process.env.GITHUB_SECRET_KEY,
            Accept: 'application/vnd.github.v3+json',
            httpsAgent: ignoreCertificateAgent,
            log: {
                debug: (message) => console.log('Octokit Debug:', message),
                info: (message) => console.log('Octokit Info:', message),
                warn: (message) => console.log('Octokit Warning:', message),
                error: (message) => console.log('Octokit Error:', message)
            }
        })
        return octokit
    }

    // 测试令牌
    async validateGitHubToken() {
        try {
            // 测试令牌基本信息
            console.log('当前使用的令牌前缀：', process.env.GITHUB_SECRET_KEY?.substring(0, 4) + '...')

            // 验证用户身份
            const { data: user } = await this.octokit.rest.users.getAuthenticated()
            console.log('认证成功，当前用户：', user.login)

            // 验证仓库访问权限
            const { data: repo } = await this.octokit.rest.repos.get({
                owner: global.appConfig.owner,
                repo: global.appConfig.repo
            })
            console.log('仓库访问权限：', {
                hasAdminAccess: repo.permissions?.admin || false,
                hasPushAccess: repo.permissions?.push || false,
                hasPullAccess: repo.permissions?.pull || false
            })

            return true
        } catch (error) {
            if (error.status === 401) {
                console.error('令牌无效或已过期')
            } else if (error.status === 403) {
                console.error('令牌权限不足')
            } else if (error.status === 404) {
                console.error('找不到仓库或无权访问')
            } else {
                console.error('验证令牌时出错：', error.message)
            }

            console.error('详细错误信息：', {
                status: error.status,
                message: error.message,
                response: error.response?.data
            })

            return false
        }
    }

    // 在文件开头添加一个测试函数
    async testGitHubAccess() {
        try {
            console.log('测试 GitHub 令牌权限...')

            // 测试令牌基本信息
            const { data: rateLimit } = await this.octokit.rest.rateLimit.get();
            console.log('令牌信息：', {
                limit: rateLimit.limit,
                remaining: rateLimit.remaining,
                reset: new Date(rateLimit.reset * 1000).toLocaleString()
            });

            // 测试仓库权限
            const { data: repo } = await this.octokit.rest.repos.get({
                owner: global.appConfig.owner,
                repo: global.appConfig.repo
            });

            // 测试写入权限
            const testContent = 'test content';
            try {
                await this.octokit.rest.repos.createOrUpdateFileContents({
                    owner: global.appConfig.owner,
                    repo: global.appConfig.repo,
                    path: 'test.txt',
                    message: 'test commit',
                    content: Buffer.from(testContent).toString('base64')
                });
                console.log('写入权限测试成功');
            } catch (error) {
                console.log('写入权限测试失败：', error.message);
            }

        } catch (error) {
            console.log('权限测试失败：', error.message);
        }
    }

    async uploadFileToGitHub(filename, filedata) {
        console.log('令牌', process.env.GITHUB_SECRET_KEY)
        // const isTokenValid = await this.validateGitHubToken()
        // if (!isTokenValid) {
        //     throw new Error('GitHub 令牌验证失败，请检查令牌配置')
        // }

        if (!filedata) {
            console.error('没有传入数据')
            return null
        }
        let suffix = path.extname(filename)
        let typeList = {
            '.txt': 'text/plain,charset=utf-8',
            '.json': 'application/json,charset=utf-8',
        }
        let type = typeList[suffix]
        if (!type) {
            console.error('不支持的格式', suffix)
            return null
        }

        let owner = global.appConfig.owner
        let repo = global.appConfig.repo
        let filepath = global.appConfig.filepath

        // 构建完整的文件路径，不要进行URL编码
        const fullPath = `${filepath}/${filename}`

        const base64EncodedData = Buffer.from(filedata).toString('base64')

        try {
            let fileSha = null

            try {
                console.log('正在获取文件信息...')
                const fileInfo = await this.octokit.rest.repos.getContent({
                    owner,
                    repo,
                    path: fullPath,
                })

                if (fileInfo.data) {
                    fileSha = fileInfo.data.sha
                    console.log('获取到文件SHA：', fileSha)
                }
            } catch (error) {
                if (error.status === 404) {
                    console.log('文件不存在，将创建新文件')
                } else {
                    console.log('获取文件信息时出错：', error)
                    throw error
                }
            }

            console.log('准备更新/创建文件...')
            // 使用 this.octokit.rest.repos.createOrUpdateFileContents 替代 request
            const currentTime = dayjs();
            const formattedTime = currentTime.format('YYYY-MM-DD (HH:mm)')
            const response = await this.octokit.rest.repos.createOrUpdateFileContents({
                owner,
                repo,
                path: fullPath,
                message: fileSha ? `更新文件 ${filename} @ ${formattedTime}` : `创建文件 ${filename} @ ${formattedTime}`,
                content: base64EncodedData,
                sha: fileSha
            })

            console.log('操作成功完成')
            return response.data

        } catch (err) {
            console.log('详细错误信息：', {
                message: err.message,
                status: err.status,
                response: err.response?.data,
                fullPath,
                owner,
                repo
            })
            return {
                'success': false,
                'data': err,
                'message': '上传到github失败'
            }
        }
    }
}


const myUploadFileToGitHub = (filename, filedata) => {
    console.log('令牌', process.env.GITHUB_SECRET_KEY)
    let updateRes = new GitHub().uploadFileToGitHub(filename, filedata)
    console.log('updateRes', updateRes)
    if (!updateRes) {
        return {
            'success': false,
            'data': updateRes
        }
    } else {
        return {
            'success': true,
            'data': '上传成功'
        }
    }
}

// const myUploadFileToGitHub = (filename, filedata) => {
//     console.log('1111111')
//     console.log('令牌', process.env.GITHUB_SECRET_KEY)
//     return 111
// }


export {
    myUploadFileToGitHub
}