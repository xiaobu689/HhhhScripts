/**
 * @平行绳 飞机频道：https://t.me/tigerorrose
 * 变量：ownerId: 自己二维码里面的 inviterId 字段
 * 变量：ELE_FANLI_TIME：配置 邀请好友的间隔时间，格式 1-10，随机延时1到 10 秒
 * 变量：ELE_UA：饿了么域名请求头里面的 user-agent
 * 定时随意，每天跑一遍就可以
 * cron: 7 6 * * *
 * 2023.6.26 更新：修复User-Agent 错误，需要自己设置环境变量ELE_UA；
 * 2023.6.30 更新：修复User-Agent 错误，删除环境变量ELE_UA；
 * 2023.7.7 更新：增加检测账号的有效性，解决 Header 中 cookie 报错
 * 2023.7.9 更新：修复Error: getaddrinfo EAI_ AGAIN
 */
const {
    sign,
    getToken,
    wait,
    checkCk,
    validateCarmeWithType,
    User_Agent,
    getCookies,
    checkCarmeCount,
    getUserInfo,
    tryCatchPromise
} = require("./common.js");
const request = require("request");
const GAME_TYEP = 2;
let CookieEles = getCookies();
const kami = process.env.ELE_CARME;
async function fridensHelper(_0x44fa34, _0x3ca75c) {
    _0x44fa34 = await checkCk(_0x44fa34);
    const _0x51fd6d = {
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        Cookie: _0x44fa34,
        "User-Agent": User_Agent
    };
    const _0x9900e7 = new Date().getTime();
    const _0x4ae8f4 = 12574478;
    const _0x5f17d6 = {
        sceneCode: "RECOMMEND_SUPPORT",
        params: "{\"ownerId\":\"" + _0x3ca75c + "\",\"fromOfficialAccount\":false,\"channel\":\"1\",\"referUserId\":\"\",\"restaurantId\":\"\",\"referCode\":\"\",\"referChannelCode\":\"\",\"referChannelType\":\"\",\"fromWeChatApp\":false,\"bizType\":\"1\",\"v\":\"4.3\",\"chInfo\":\"ch_app_chsub_Photo\",\"from\":\"hjb_app_xbb\",\"actId\":\"1\",\"longitude\":\"120.22057268768549\",\"latitude\":\"30.17862595617771\"}"
    };
    var _0x5ea933 = "data=" + encodeURIComponent(JSON.stringify(_0x5f17d6));
    const _0x3f65ea = getToken(_0x44fa34),
        _0x59ecd8 = _0x3f65ea.split("_")[0];
    const _0x3e43d = await sign(_0x59ecd8 + "&" + _0x9900e7 + "&" + _0x4ae8f4 + "&" + JSON.stringify(_0x5f17d6), kami);
    const _0x5f2fe9 = {
        url: "https://mtop.ele.me/h5/mtop.alibaba.o2o.alsc.union.coupon.track/1.0/?jsv=2.6.1&appKey=12574478&&ttid=1601274958480%40eleme_android_10.14.3&t=" + _0x9900e7 + "&sign=" + _0x3e43d + "&api=mtop.alibaba.o2o.alsc.union.coupon.track",
        method: "POST",
        headers: _0x51fd6d,
        body: _0x5ea933
    };
    return tryCatchPromise(_0x3646fc => {
        request(_0x5f2fe9, async (_0x540129, _0x40bcb1, _0x52637b) => {
            if (!_0x540129 && _0x40bcb1.statusCode == 200) {
                try {
                    const _0x6c9838 = JSON.parse(_0x52637b);
                    _0x3646fc(_0x6c9838);
                } catch (_0x53998e) {
                    console.log(_0x53998e);
                    _0x3646fc(null);
                }
            } else {
                _0x3646fc(null);
            }
        });
    });
}
function getRandom(_0xf39232, _0x3b47cc) {
    var _0x378d8b = Math.floor(Math.random() * (_0x3b47cc - _0xf39232 + 1) + _0xf39232);
    return _0x378d8b;
}
async function start() {
    const _0x5828a4 = process.env.ELE_FANLI_TIME;
    await validateCarmeWithType(kami, 1);
    const _0x37acb9 = process.env.ownerId;
    if (!_0x37acb9) {
        console.log("请先配置环境变量ownerId！！");
        process.exit(0);
    }
    for (let _0x1208f8 = 0; _0x1208f8 < CookieEles.length; _0x1208f8++) {
        let _0x164c60 = CookieEles[_0x1208f8];
        _0x164c60 = await checkCk(_0x164c60, _0x1208f8);
        if (!_0x164c60) {
            continue;
        }
        let _0x43401a = await getUserInfo(_0x164c60);
        if (!_0x43401a.username) {
            console.log("第", _0x1208f8 + 1, "账号失效！请重新登录！！！😭");
            continue;
        }
        const _0x52ce8f = _0x43401a.user_id;
        await checkCarmeCount(kami, _0x52ce8f, GAME_TYEP);
        console.log("******开始【饿了么账号", _0x1208f8 + 1, "】", _0x43401a.username, "*********");
        res = await fridensHelper(_0x164c60, _0x37acb9);
        if (res.data.code == 0) {
            if (res.data.message == "SUCCESS") {
                amount = res.data.data.couponAmount / 100;
                couponCondition = res.data.data.couponCondition / 100;
                console.log("第", _0x1208f8 + 1, "账号,邀请成功", "被邀请人领取的红包为:满" + couponCondition + "减" + amount + "元");
            }
        } else {
            console.log(res.data.message || "邀请失败");
        }
        if (_0x5828a4 && _0x5828a4.indexOf("-") != -1) {
            console.log("防止黑号延时" + _0x5828a4 + "秒");
            const _0x2c394a = _0x5828a4.split("-");
            await wait(getRandom(_0x2c394a[0], _0x2c394a[1]));
        } else {
            console.log("防止黑号延时10-30秒");
            await wait(getRandom(10, 30));
        }
    }
    process.exit(0);
}
start();
function Env(t, e) {
    "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0);
    class s {
        constructor(t) {
            this.env = t;
        }
        send(t, e = "GET") {
            t = "string" == typeof t ? {
                url: t
            } : t;
            let s = this.get;
            "POST" === e && (s = this.post);
            return new Promise((e, i) => {
                s.call(this, t, (t, s, r) => {
                    t ? i(t) : e(s);
                });
            });
        }
        get(t) {
            return this.send.call(this.env, t);
        }
        post(t) {
            return this.send.call(this.env, t, "POST");
        }
    }
    return new class {
        constructor(t, e) {
            this.name = t;
            this.http = new s(this);
            this.data = null;
            this.dataFile = "box.dat";
            this.logs = [];
            this.isMute = !1;
            this.isNeedRewrite = !1;
            this.logSeparator = "\n";
            this.startTime = new Date().getTime();
            Object.assign(this, e);
            this.log("", `🔔${this.name}, 开始!`);
        }
        isNode() {
            return "undefined" != typeof module && !!module.exports;
        }
        isQuanX() {
            return "undefined" != typeof $task;
        }
        isSurge() {
            return "undefined" != typeof $httpClient && "undefined" == typeof $loon;
        }
        isLoon() {
            return "undefined" != typeof $loon;
        }
        toObj(t, e = null) {
            try {
                return JSON.parse(t);
            } catch {
                return e;
            }
        }
        toStr(t, e = null) {
            try {
                return JSON.stringify(t);
            } catch {
                return e;
            }
        }
        getjson(t, e) {
            let s = e;
            const i = this.getdata(t);
            if (i) {
                try {
                    s = JSON.parse(this.getdata(t));
                } catch { }
            }
            return s;
        }
        setjson(t, e) {
            try {
                return this.setdata(JSON.stringify(t), e);
            } catch {
                return !1;
            }
        }
        getScript(t) {
            return new Promise(e => {
                this.get({
                    url: t
                }, (t, s, i) => e(i));
            });
        }
        runScript(t, e) {
            return new Promise(s => {
                let i = this.getdata("@chavy_boxjs_userCfgs.httpapi");
                i = i ? i.replace(/\n/g, "").trim() : i;
                let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout");
                r = r ? 1 * r : 20;
                r = e && e.timeout ? e.timeout : r;
                const [o, h] = i.split("@"),
                    n = {
                        url: `http://${h}/v1/scripting/evaluate`,
                        body: {
                            script_text: t,
                            mock_type: "cron",
                            timeout: r
                        },
                        headers: {
                            "X-Key": o,
                            Accept: "*/*"
                        }
                    };
                this.post(n, (t, e, i) => s(i));
            }).catch(t => this.logErr(t));
        }
        loaddata() {
            if (!this.isNode()) {
                return {};
            }
            {
                this.fs = this.fs ? this.fs : require("fs");
                this.path = this.path ? this.path : require("path");
                const t = this.path.resolve(this.dataFile),
                    e = this.path.resolve(process.cwd(), this.dataFile),
                    s = this.fs.existsSync(t),
                    i = !s && this.fs.existsSync(e);
                if (!s && !i) {
                    return {};
                }
                {
                    const i = s ? t : e;
                    try {
                        return JSON.parse(this.fs.readFileSync(i));
                    } catch (t) {
                        return {};
                    }
                }
            }
        }
        writedata() {
            if (this.isNode()) {
                this.fs = this.fs ? this.fs : require("fs");
                this.path = this.path ? this.path : require("path");
                const t = this.path.resolve(this.dataFile),
                    e = this.path.resolve(process.cwd(), this.dataFile),
                    s = this.fs.existsSync(t),
                    i = !s && this.fs.existsSync(e),
                    r = JSON.stringify(this.data);
                s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r);
            }
        }
        lodash_get(t, e, s) {
            const i = e.replace(/\[(\d+)\]/g, ".$1").split(".");
            let r = t;
            for (const t of i) if (r = Object(r)[t], void 0 === r) {
                return s;
            }
            return r;
        }
        lodash_set(t, e, s) {
            return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t);
        }
        getdata(t) {
            let e = this.getval(t);
            if (/^@/.test(t)) {
                const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t),
                    r = s ? this.getval(s) : "";
                if (r) {
                    try {
                        const t = JSON.parse(r);
                        e = t ? this.lodash_get(t, i, "") : e;
                    } catch (t) {
                        e = "";
                    }
                }
            }
            return e;
        }
        setdata(t, e) {
            let s = !1;
            if (/^@/.test(e)) {
                const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e),
                    o = this.getval(i),
                    h = i ? "null" === o ? null : o || "{}" : "{}";
                try {
                    const e = JSON.parse(h);
                    this.lodash_set(e, r, t);
                    s = this.setval(JSON.stringify(e), i);
                } catch (e) {
                    const o = {};
                    this.lodash_set(o, r, t);
                    s = this.setval(JSON.stringify(o), i);
                }
            } else {
                s = this.setval(t, e);
            }
            return s;
        }
        getval(t) {
            return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null;
        }
        setval(t, e) {
            return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null;
        }
        initGotEnv(t) {
            this.got = this.got ? this.got : require("got");
            this.cktough = this.cktough ? this.cktough : require("tough-cookie");
            this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar();
            t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar));
        }
        get(t, e = () => { }) {
            t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]);
            this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, {
                "X-Surge-Skip-Scripting": !1
            })), $httpClient.get(t, (t, s, i) => {
                !t && s && (s.body = i, s.statusCode = s.status);
                e(t, s, i);
            })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, {
                hints: !1
            })), $task.fetch(t).then(t => {
                const {
                    statusCode: s,
                    statusCode: i,
                    headers: r,
                    body: o
                } = t;
                e(null, {
                    status: s,
                    statusCode: i,
                    headers: r,
                    body: o
                }, o);
            }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => {
                try {
                    if (t.headers["set-cookie"]) {
                        const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString();
                        s && this.ckjar.setCookieSync(s, null);
                        e.cookieJar = this.ckjar;
                    }
                } catch (t) {
                    this.logErr(t);
                }
            }).then(t => {
                const {
                    statusCode: s,
                    statusCode: i,
                    headers: r,
                    body: o
                } = t;
                e(null, {
                    status: s,
                    statusCode: i,
                    headers: r,
                    body: o
                }, o);
            }, t => {
                const {
                    message: s,
                    response: i
                } = t;
                e(s, i, i && i.body);
            }));
        }
        post(t, e = () => { }) {
            if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) {
                this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, {
                    "X-Surge-Skip-Scripting": !1
                }));
                $httpClient.post(t, (t, s, i) => {
                    !t && s && (s.body = i, s.statusCode = s.status);
                    e(t, s, i);
                });
            } else {
                if (this.isQuanX()) {
                    t.method = "POST";
                    this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, {
                        hints: !1
                    }));
                    $task.fetch(t).then(t => {
                        const {
                            statusCode: s,
                            statusCode: i,
                            headers: r,
                            body: o
                        } = t;
                        e(null, {
                            status: s,
                            statusCode: i,
                            headers: r,
                            body: o
                        }, o);
                    }, t => e(t));
                } else {
                    if (this.isNode()) {
                        this.initGotEnv(t);
                        const {
                            url: s,
                            ...i
                        } = t;
                        this.got.post(s, i).then(t => {
                            const {
                                statusCode: s,
                                statusCode: i,
                                headers: r,
                                body: o
                            } = t;
                            e(null, {
                                status: s,
                                statusCode: i,
                                headers: r,
                                body: o
                            }, o);
                        }, t => {
                            const {
                                message: s,
                                response: i
                            } = t;
                            e(s, i, i && i.body);
                        });
                    }
                }
            }
        }
        time(t, e = null) {
            const s = e ? new Date(e) : new Date();
            let i = {
                "M+": s.getMonth() + 1,
                "d+": s.getDate(),
                "H+": s.getHours(),
                "m+": s.getMinutes(),
                "s+": s.getSeconds(),
                "q+": Math.floor((s.getMonth() + 3) / 3),
                S: s.getMilliseconds()
            };
            /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length)));
            for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length)));
            return t;
        }
        msg(e = t, s = "", i = "", r) {
            const o = t => {
                if (!t) {
                    return t;
                }
                if ("string" == typeof t) {
                    return this.isLoon() ? t : this.isQuanX() ? {
                        "open-url": t
                    } : this.isSurge() ? {
                        url: t
                    } : void 0;
                }
                if ("object" == typeof t) {
                    if (this.isLoon()) {
                        let e = t.openUrl || t.url || t["open-url"],
                            s = t.mediaUrl || t["media-url"];
                        return {
                            openUrl: e,
                            mediaUrl: s
                        };
                    }
                    if (this.isQuanX()) {
                        let e = t["open-url"] || t.url || t.openUrl,
                            s = t["media-url"] || t.mediaUrl;
                        return {
                            "open-url": e,
                            "media-url": s
                        };
                    }
                    if (this.isSurge()) {
                        let e = t.url || t.openUrl || t["open-url"];
                        return {
                            url: e
                        };
                    }
                }
            };
            if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) {
                let t = ["", "==============📣系统通知📣=============="];
                t.push(e);
                s && t.push(s);
                i && t.push(i);
                console.log(t.join("\n"));
                this.logs = this.logs.concat(t);
            }
        }
        log(...t) {
            t.length > 0 && (this.logs = [...this.logs, ...t]);
            console.log(t.join(this.logSeparator));
        }
        logErr(t, e) {
            const s = !this.isSurge() && !this.isQuanX() && !this.isLoon();
            s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t);
        }
        wait(t) {
            return new Promise(e => setTimeout(e, t));
        }
        done(t = {}) {
            const e = new Date().getTime(),
                s = (e - this.startTime) / 1000;
            this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`);
            this.log();
            (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t);
        }
    }(t, e);
}