//Sat Aug 17 2024 12:11:17 GMT+0800 (中国标准时间)
//Base:https://github.com/echo094/decode-js
//Modify:https://github.com/smallfawn/decode_action
/**
 * 测试-增加进度显示
 * 卡密变量：ELE_TTCJ_CARME 填自己购买的卡密。
 * 需要设置环境变量 ownCookie 这个是需要助力账号的 cookie。
 */
const {
    "sign": sign,
    "getToken": getToken,
    "wait": wait,
    "checkCk": checkCk,
    "getCookies": getCookies,
    "getUserInfo": getUserInfo,
    "tryCatchPromise": tryCatchPromise,
    "checkMasterCk": checkMasterCk
} = require("./common.js");
const request = require("request"),
    https = require("https"),
    cheerio = require("cheerio");
let CookieEles = [];
const kami = process["env"]["ELE_TTCJ_CARME"],
    carmiType = 4;
let count_num = 0;
async function getCoordinates() {
    return new Promise((_0x813bfd, _0x2ac624) => {
        https["get"]("https://zh-hans.ipshu.com/my_info", _0x4d31ba => {
            let _0x33a9bb = "";
            _0x4d31ba["on"]("data", _0x2406e4 => {
                _0x33a9bb += _0x2406e4;
            });
            _0x4d31ba["on"]("end", () => {
                const _0x149ccd = cheerio["load"](_0x33a9bb),
                    _0x212588 = _0x149ccd(".widget_box.p-xs.small"),
                    _0x4dd909 = _0x212588["find"]("li")["eq"](4)["text"]()["trim"]()["split"](":")[1],
                    _0x47ab2d = _0x212588["find"]("li")["eq"](5)["text"]()["trim"]()["split"](":")[1],
                    _0x1fb96c = {
                        "latitude": _0x4dd909,
                        "longitude": _0x47ab2d
                    };
                _0x813bfd(_0x1fb96c);
            });
        });
    });
}
async function commonRequest(_0x58da2c, _0x339772, _0x583ff1) {
    const _0x1fb7c8 = {
        "authority": "shopping.ele.me",
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": _0x58da2c,
        "x-miniapp-id-taobao": "2021002148648263",
        "x-miniapp-version": "3.20230627.141210",
        "appid": "2021002148648263"
    };
    const _0x46776b = new Date()["getTime"](),
        _0x520319 = 12574478;
    var _0x5db75e = "data=" + encodeURIComponent(JSON["stringify"](_0x583ff1));
    const _0x3f666e = getToken(_0x58da2c),
        _0x20490f = _0x3f666e["split"]("_")[0],
        _0x165d57 = await sign(_0x20490f + "&" + _0x46776b + "&" + _0x520319 + "&" + JSON["stringify"](_0x583ff1), kami, carmiType),
        _0xaa0b27 = {
            "url": "https://shopping.ele.me/h5/mtop.alsc.growth.tangram.gateway/1.0/?jsv=2.6.1&appKey=12574478&asac=" + _0x339772 + "&ttid=1601274958480%40eleme_android_10.14.3&t=" + _0x46776b + "&sign=" + _0x165d57 + "&api=mtop.alsc.growth.tangram.gateway",
            "method": "POST",
            "headers": _0x1fb7c8,
            "body": _0x5db75e
        };
    return tryCatchPromise(_0x3df110 => {
        request(_0xaa0b27, async (_0x13f362, _0x41bfd9, _0x550cbe) => {
            if (!_0x13f362 && _0x41bfd9["statusCode"] == 200) {
                try {
                    const _0x429e6a = JSON["parse"](_0x550cbe);
                    _0x3df110(_0x429e6a);
                } catch (_0x36fe09) {
                    console["log"](_0x36fe09);
                    _0x3df110(null);
                }
            } else {
                _0x3df110(null);
            }
        });
    });
}
function processUrl(_0xedab75) {
    const _0x470318 = new Map();
    const _0x524766 = _0xedab75["split"]("?")[1]["split"]("&");
    for (let _0x476483 = 0; _0x476483 < _0x524766["length"]; _0x476483++) {
        const [_0x946150, _0x207453] = _0x524766[_0x476483]["split"]("=");
        _0x470318["set"](_0x946150, _0x207453);
    }
    return _0x470318;
}
async function getShareId(_0x2572fb, _0x2e1e63, _0xd46322) {
    _0x2572fb = await checkMasterCk(_0x2572fb, kami, carmiType);
    !_0x2572fb && (console["log"]("\u9700\u8981\u52A9\u529B\u7684\u8D26\u53F7\u5931\u6548\uFF01\u8BF7\u91CD\u65B0\u767B\u5F55\uFF01\uFF01\uFF01"), process["exit"](0));
    var _0x39b939;
    const _0x13f964 = {
        "api": "fissionDrawShare",
        "asac": "2A22C21KPW8PSOH8QMD4LM",
        "bizScene": "growth_fission_coupon",
        "instance": "INNER",
        "params": "{\"latitude\":\"" + _0xd46322 + "\",\"longitude\":\"" + _0x2e1e63 + "\",\"cityId\":\"\"}",
        "scene": "fissionDraw001"
    },
        _0x5f2c64 = await commonRequest(_0x2572fb, "2A22C21KPW8PSOH8QMD4LM", _0x13f964);
    if (_0x5f2c64["data"] && _0x5f2c64["data"]["result"]) {
        const _0x578798 = _0x5f2c64["data"]["result"];
        _0x39b939 = processUrl(_0x578798["url"])["get"]("shareId");
        console["log"]("\u83B7\u53D6\u5230\u7684\u52A9\u529B id \u4E3A", _0x39b939);
        return _0x39b939;
    } else {
        console["log"]("\u83B7\u53D6\u5230\u52A9\u529B id \u5931\u8D25\uFF0C\u7A0B\u5E8F\u9000\u51FA");
        process["exit"](0);
    }
}
async function jindu(_0x4b1643, _0x5bad07, _0x236d3a, _0x3f1a5a) {
    _0x4b1643 = await checkMasterCk(_0x4b1643, kami, carmiType);
    !_0x4b1643 && (console["log"]("\u9700\u8981\u52A9\u529B\u7684\u8D26\u53F7\u5931\u6548\uFF01\u8BF7\u91CD\u65B0\u767B\u5F55\uFF01\uFF01\uFF01"), process["exit"](0));
    const _0x5e5682 = {
        "api": "fissionDrawHomePage",
        "asac": "2A22C216PW8PSO7H6J9G63",
        "bizScene": "growth_fission_coupon",
        "instance": "INNER",
        "params": "{\"latitude\":\"" + _0x236d3a + "\",\"longitude\":\"" + _0x5bad07 + "\",\"cityId\":\"\",\"shareId\":\"" + _0x3f1a5a + "\"}",
        "scene": "fissionDraw001"
    },
        _0x17b2e0 = await commonRequest(_0x4b1643, "2A22C216PW8PSO7H6J9G63", _0x5e5682);
    if (_0x17b2e0["data"] && _0x17b2e0["data"]["result"]) {
        let _0x2674d9 = _0x17b2e0["data"]["result"]["fixedPrize"];
        console["log"](_0x2674d9["title"], _0x2674d9["reduction"], _0x2674d9["threshold"], "\u5F53\u524D\u8FDB\u5EA6\uFF1A\u3010" + _0x2674d9["amount"] + "\u3011");
        Number(_0x2674d9["amount"]) >= Number(_0x2674d9["maxAmount"]) && (console["log"]("\uD83C\uDF89\uD83C\uDF89 \u4EFB\u52A1\u5B8C\u6210\uFF0C\u5DF2\u83B7\u5F97", _0x2674d9["reduction"], _0x2674d9["threshold"]), process["exit"](0));
    }
}
async function fridensHelper(index, _0x100366, _0x33fd64, _0x5bef69, _0x28211e, _0xe77133) {
    try {
        _0x33fd64 = await checkMasterCk(_0x33fd64, kami, carmiType);
        const _0x52038f = {
            "api": "support",
            "bizScene": "growth_fission_coupon",
            "instance": "INNER",
            "params": "{\"latitude\":\"" + _0xe77133 + "\",\"longitude\":\"" + _0x28211e + "\",\"cityId\":\"\",\"shareId\":\"" + _0x5bef69 + "\"}",
            "scene": "fissionDraw001"
        },
            _0x2060c8 = await commonRequest(_0x100366, "2A22C21RPW8PSOJ9OFOQGY", _0x52038f);
        if (_0x2060c8["data"] && _0x2060c8["data"]["result"]) {
            const _0x9fffaf = _0x2060c8["data"]["result"];
            console["log"]("\u7B2C\u3010" + index + "\u3011\u4E2A\u53F7" + _0x9fffaf["title"] + "\uFF1A" + _0x9fffaf["subTitle"]);
            if (_0x9fffaf["title"]["indexOf"]("\u65E0\u6CD5\u52A9\u529B") !== -1) {
                console["log"]("\u9632\u6B62\u9ED1\u53F7\u5EF6\u65F61-3\u79D2");
                await wait(getRandom(1, 3));
            } else {
                if (_0x9fffaf["title"]["indexOf"]("\u8C22\u8C22\u4F60\u4E3A\u6211\u52A9\u529B") !== -1) {
                    const _0x47a9b4 = {
                        "api": "drawAction",
                        "asac": "2A22C21FPW8PSO7U202V54",
                        "bizScene": "growth_fission_coupon",
                        "instance": "INNER",
                        "params": "{\"latitude\":\"" + _0xe77133 + "\",\"longitude\":\"" + _0x28211e + "\",\"cityId\":\"\"}",
                        "scene": "fissionDraw001"
                    },
                        _0x3eaef6 = await commonRequest(_0x33fd64, "2A22C21FPW8PSO7U202V54", _0x47a9b4);
                    if (_0x3eaef6["data"] && _0x3eaef6["data"]["result"]) {
                        const _0x3970f8 = _0x3eaef6["data"]["result"],
                            _0x1ad23f = _0x3970f8["popWindow"]["content"][0]["amount"];
                        console["log"](_0x3970f8["popWindow"]["title"] + "\uFF1A" + _0x1ad23f);
                        if (_0x3eaef6["data"]["success"]) {
                            const _0x24e52b = {
                                "api": "withdrawAction",
                                "bizScene": "growth_fission_coupon",
                                "instance": "INNER",
                                "params": "{\"latitude\":\"" + _0xe77133 + "\",\"longitude\":\"" + _0x28211e + "\",\"cityId\":\"\",\"amount\":\"" + _0x1ad23f + "\"}",
                                "scene": "fissionDraw001"
                            },
                                _0x275336 = await commonRequest(_0x33fd64, "", _0x24e52b);
                            if (_0x275336["data"] && _0x275336["data"]["result"]) {
                                const _0x2214c6 = _0x275336["data"]["result"];
                                console["log"](_0x2214c6["popWindow"]["title"] + "\uFF1A\u91D1\u989D", _0x2214c6["popWindow"]["content"][0]["amount"]);
                                let amount = parseFloat(_0x2214c6["popWindow"]["content"][0]["amount"]); // 转换为浮点数
                                count_num += amount; // 累加到总额
                                console.log("\u672C\u6B21\u8FD0\u884C\u603B\u73B0\u91D1\uFF1A\u3010" + count_num.toFixed(2) + "\u3011"); // 输出保留两位小数的总额

                                console["log"](_0x2214c6["popWindow"]["content"][0]["step2"]);
                                await jindu(_0x33fd64, _0x28211e, _0xe77133, _0x5bef69);
                            } else {
                                console["log"]("\u63D0\u73B0\uFF1A" + _0x3eaef6["ret"][0]);
                            }
                        } else {
                            console["log"]("\u62BD\u5956\uFF1A" + _0x3eaef6["ret"][0]);
                        }
                    } else {
                        console["log"]("\u62BD\u5956\uFF1A" + _0x3eaef6["ret"][0]);
                    }
                    console["log"]("\u9632\u6B62\u9ED1\u53F7\u5EF6\u65F65-10\u79D2");
                    await wait(getRandom(5, 10));
                }
            }
        } else {
            console["log"]("\u52A9\u529B\uFF1A" + drawRes["ret"][0]);
        }
    } catch (_0xd3d10c) { }
}
(async function () {
    const _0x319386 = process["env"]["ownCookie"];
    !_0x319386 && (console["log"]("\u672A\u8BBE\u7F6E\u9700\u52A9\u529B\u7684 ck\uFF0C\u7A0B\u5E8F\u7ED3\u675F!"), process["exit"](0));
    CookieEles = getCookies();
    const _0x560964 = await getCoordinates(),
        _0x5d3e42 = await getShareId(_0x319386, _0x560964["longitude"], _0x560964["latitude"]);
    for (let _0x3afecd = 0; _0x3afecd < CookieEles["length"]; _0x3afecd++) {
        let _0x3ba257 = CookieEles[_0x3afecd];
        _0x3ba257 = await checkCk(_0x3ba257, _0x3afecd, kami, carmiType);
        if (!_0x3ba257) {
            continue;
        }
        let _0x31e014 = await getUserInfo(_0x3ba257);
        if (!_0x31e014["username"]) {
            console["log"]("\u7B2C\u3010", _0x3afecd + 1, "\u3011\u8D26\u53F7\u5931\u6548\uFF01\u8BF7\u91CD\u65B0\u767B\u5F55\uFF01\uFF01\uFF01\uD83D\uDE2D");
            continue;
        }
        await fridensHelper(_0x3afecd + 1, _0x3ba257, _0x319386, _0x5d3e42, _0x560964["longitude"], _0x560964["latitude"]);
    }
    process["exit"](0);
})();
function getRandom(_0x483f0c, _0x4c71e1) {
    return Math["floor"](Math["random"]() * (_0x4c71e1 - _0x483f0c + 1) + _0x483f0c);
}