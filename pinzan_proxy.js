// pinzan.js

const crypto = require('crypto');
const axios = require('axios');

const env_name = 'PZ_CONFIG';
// const pinzan_config = process.env[env_name];
const pinzan_config = {
    "password": "Admin201404293",
    "no": "20240524952954587395",
    "tiqu_secret": "63ho0v8i55tnvc",
    "sig_secret": "s8j1aolvgkobpq81"
}
if (!pinzan_config) {
    console.log(`⛔️未获取到配置变量：请检查变量 ${env_name} 是否填写`);
    process.exit(0);
}

// 套餐余量查询
async function getProxiesUsage() {
    const url = 'https://service.ipzan.com/userProduct-get?no=20240524952954587395&userId=7B5L7LBGUS';
    try {
        const response = await axios.get(url);
        const balance = response.data.data.balance;
        console.log(`🚀代理来源: 品赞代理 | 💰套餐余额: ${balance}`);
        return balance;
    } catch (error) {
        console.error("套餐余量查询失败", error);
        return null;
    }
}

// IP提取
async function generateIP(num, minute) {
    let ip = '';
    let ipApi = [];
    let addWhiteList = false;
    const params = {
        num: num,
        no: pinzan_config.no,
        minute: minute,
        format: 'json',
        protocol: '1',  // 使用协议：http/https: 1
        pool: 'quality',  // 优质IP: quality | 普通IP池: ordinary
        mode: 'auth',  // whitelist: 白名单授权方式 | auth: 账号密码授权
        secret: pinzan_config.tiqu_secret
    };
    const url = 'https://service.ipzan.com/core-extract';
    try {
        const response = await axios.get(url, { params });
        if (response.data.code === 0) {
            ipApi = response.data.data.list;
        } else {
            if (response.data.message.includes("加入到白名单再进行提取")) {
                ip = response.data.message.split("将")[1].split("加入")[0];
                console.log(`⛔️需要将${ip}加入白名单授权后才能进行提取`);
                addWhiteList = true;
            }
        }
        return { ipApi, addWhiteList, ip };
    } catch (error) {
        console.error("IP提取失败", error);
        return { ipApi, addWhiteList, ip };
    }
}

// 加入白名单
async function whiteListAdd(ip) {
    console.log('💤开始加入白名单......');
    const data = `${pinzan_config.password}:${pinzan_config.tiqu_secret}:${Math.floor(Date.now() / 1000)}`;
    const key = Buffer.from(pinzan_config.sig_secret, 'utf-8');
    const cipher = crypto.createCipheriv('aes-128-ecb', key, Buffer.alloc(0));
    let sign = cipher.update(data, 'utf-8', 'hex');
    sign += cipher.final('hex');
    const url = "https://service.ipzan.com/whiteList-add";
    const payload = {
        no: pinzan_config.no,
        ip: ip,
        sign: sign
    };
    try {
        const response = await axios.post(url, payload);
        console.log(`🥰${response.data.data}`);
    } catch (error) {
        console.error("加入白名单失败", error);
    }
}

// 生成代理
function createProxies(ipApis) {
    const apiProxies = [];
    ipApis.forEach(item => {
        const proxyHost = item.ip;
        const proxyPort = item.port;
        const proxyMeta = `http://${item.account}:${item.password}@${proxyHost}:${proxyPort}`;
        const proxies = {
            http: proxyMeta,
            https: proxyMeta
        };
        console.log(`🍄${item.net} | ${proxyHost}:${proxyPort}`);
        apiProxies.push(proxies);
    });
    return apiProxies;
}

async function pinzanProxy(num, minute) {
    console.log(`\n---------------- 代理INFO区域 ----------------`);
    console.log(`🍳本脚本使用代理 | 提取数量: ${num}个 | 有效期: ${minute}分钟`);
    let httpProxies = [];
    // 查余额
    const balance = await getProxiesUsage();
    if (balance <= 0) {
        console.log("套餐余额不足");
        return null;
    }
    // 提取IP
    let { ipApi, addWhiteList, ip } = await generateIP(num, minute);
    if (ip !== "") {
        while (true) {
            // 添加白名单
            await whiteListAdd(ip);
            await new Promise(resolve => setTimeout(resolve, 1000));  // 等待1秒
            // 再次尝试提取IP
            ({ ipApi, addWhiteList, ip } = await generateIP(num, minute));
            if (ipApi.length > 0) {
                httpProxies = createProxies(ipApi);
                break;
            }
        }
    } else if (ipApi.length > 0 && !addWhiteList) {
        httpProxies = createProxies(ipApi);
    }

    console.log(`---------------- 代理INFO区域 ----------------\n`);
    return httpProxies;
}

module.exports = {
    pinzanProxy
};
