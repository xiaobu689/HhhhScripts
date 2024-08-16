const https = require('https');
const base_desc = '这是一个选择题，请选择出正确答案后直接回答A或B或C或D，严格按照以下格式回答：芝麻开门#你的答案#芝麻开门\n'
let QIANWEN = process.env.QIANWEN;
function getGPTResponse(userContent) {
    return new Promise((resolve, reject) => {
        const model = 'qwen-turbo';
        const messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": base_desc + userContent
            }
        ];
        const options = {
            hostname: 'dashscope.aliyuncs.com',
            path: '/compatible-mode/v1/chat/completions',
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + QIANWEN,
                'Content-Type': 'application/json'
            }
        };
        const data = JSON.stringify({ model, messages });
        const req = https.request(options, res => {
            let response = '';
            res.on('data', chunk => {
                response += chunk;
            });
            res.on('end', () => {
                try {
                    const parsedResponse = JSON.parse(response);
                    if (parsedResponse.choices && parsedResponse.choices.length > 0) {
                        const content = parsedResponse.choices[0].message.content;
                        const reply = extractAnswer(content);
                        resolve(reply);
                    } else {
                        reject(new Error('No content found in the response'));
                    }
                } catch (error) {
                    reject(error);
                }
            });
        });
        req.on('error', error => {
            reject(error);
        });
        req.write(data);
        req.end();
    });
}


function extractAnswer(input) {
    // 使用正则表达式匹配两个##中间的数据
    const pattern = /芝麻开门#(.*?)#芝麻开门/;
    const match = input.match(pattern);
    // 如果找到匹配，返回中间的数据，否则返回null
    return match ? match[1] : null;
}

module.exports = {
    getGPTResponse
}