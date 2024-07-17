/**
cron: 10 8 * * *
 * 需要安装依赖sm-crypto
 * 科技工作者之家APP
 *
 *
 * ========= 青龙--配置文件 =========
 * 先手动进APP开启连签180天活动，并且自己创建一个部落,抓包拿到自己部落的group_id
 * 自己设置  本脚本内  的变量mygroupId为自己部落的id
 *
 * 变量格式: export keji_ck='手机号&密码'   ,多账号用 换行 或 @ 分割
 * 定时每天一次
 */

const { log } = require("console");
const sm3 = require('sm-crypto').sm3;


const $ = new Env("科技工作者之家");
const notify = $.isNode() ? require("../../sendNotify") : "";
const Notify = 1 		//0为关闭通知,1为打开通知,默认为1
const debug = 0			//0为关闭调试,1为打开调试,默认为0
//---------------------------------------------------------------------------------------------------------
let ckStr = ($.isNode() ? process.env.keji_ck : $.getdata('keji_ck')) || '';
let msg, ck;
var _token; //登录获取的token
var ctid; //分享文章的id
var _poem; //诗词ID
var uid; //randomcode

//部落id//部落id//部落id//部落id //部落id//部落id
var mygroupId = '3706'; //部落id



var randomdisscusarr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];    //评论随机数组
var _weiboid;  //删除的id
let host = 'api-kejia.scimall.org.cn';
//文章ID
//---------------------------------------------------------------------------------------------------------
var sharebox = ['6155236', '6155515', '6158826', '6158717', '6155234', '6155231', '6158824', '6158571', '6158031', '6158461', '6158001', '6157997', '6157926', '6157432', '6157074'];
//---------------------------------------------------------------------------------------------------------
//诗词用
//---------------------------------------------------------------------------------------------------------
var poemtxt = ['人人仰望在何处生怕河梁分袂处', '人间信有白头痴生贤特也涓良日', '保得重重翠碧衣安乐常思病苦时', '成由勤俭破由奢器远况曾师旧德', '里中巴客半归乡路入烟霞草木香', '读书谁料转家贫万里桥头独越吟', '卷帷上床喜不定书沈寒雁云边影', '给与烦襟作冷风力尽不得抛杵声', '行道才人斗射飞万全身出百重围', '诗人浪作水仙歌生平素志惟丘壑', '诗盟岂止寻宗派生涯闻已半蒿莱', '城头夜半声哑哑素手春溪罢浣纱', '城傍牧马驱未过素淡堪移入卧屏', '真王未许久从容实用人材即至公', '本无背面与初终来成方面保厘功', '本作耕耘意若何来君回唱竹枝歌', '省多少闲是闲非上品功能甘露味', '省得蔡州今日事上古初闻出尧世', '落在深泥谁复怜地坼天开总是闲', '落霞语好终伤绮地暖应知穴处狸', '名山长似有人催师门念旧如相问', '名压西川旧海棠师承有法古韦康', '珍重故人知我者珠团绿锦趁晴摊', '珍重诗人频管领珠玑影冷偏粘草', '鸟睡花林绣羽香眉间画得山两点',]
//---------------------------------------------------------------------------------------------------------
//评论用
//---------------------------------------------------------------------------------------------------------
var discusstxt = ['坐游船翠柳岸边飘临小径南湖陶我醉', '山鸟群飞日隐轻霞登车上马倏忽雨散', '静守时光以待流年易水人去明月如霜', '生能尽欢死亦无憾静水流深沧笙踏歌', '家山乡眷兮会时稀今朝设宴兮觥散飞', '单感觉轻风拂面来怎安知夕日云霞坠', '对花对酒落梅成愁十里长亭水悠悠兮', '养怡之福可得永年幸甚至哉歌以咏志', '有生一日皆报恩时有生一日皆伴亲时', '俯仰自得游心太玄目送归鸿手挥五弦', '北风其凉雨雪其滂惠而好我携手同行', '将子无怒秋以为期乘彼垝垣以望复关', '置酒高堂悲歌临觞人寿几何逝如朝霜', '地列酒泉天垂酒池杜康妙识仪狄先知', '苹以春晖兰以秋芳来日苦短去日苦长', '信誓旦旦不思其反反是不思亦已焉哉', '育吾兄弟艰辛备历摧折作磨因此遭疾', '爱力所及原本真诚不作诳言不存欺心', '有志未伸有求不获精神痛苦以此为卓', '日月之行若出其中星汉灿烂若出其里', '思从二女适彼湘沅灵幽听微谁观玉颜'];
//---------------------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------------------
let Change = '无'

//---------------------------------------------------------------------------------------------------------

async function tips(ckArr) {
	let Version = `\n📌 微信公众号：老司机上线 📌`
	DoubleLog(`${Version}\n📌 🆙 更新内容: ${Change}`);
	// DoubleLog(`${thank}`);

	DoubleLog(`\n========== 共找到 ${ckArr.length} 个账号 ==========`);
	debugLog(`【debug】 这是你的账号数组:\n ${ckArr}`);
}


!(async () => {
	let ckArr = await checkEnv(ckStr, "keji_ck");
	await tips(ckArr);
	for (let index = 0; index < ckArr.length; index++) {
		let num = index + 1;
		DoubleLog(`\n-------- 开始【第 ${num} 个账号】--------`);
		ck = ckArr[index].split("&");
		debugLog(`【debug】 这是你第 ${num} 账号信息:\n ${ck}`);
		await start();
	}
	await SendMsg(msg);

})()
	.catch((e) => $.logErr(e))
	.finally(() => $.done());


async function start() {

	console.log("\n开始 任务");

	uid = RandeCode();


	await $.wait(3 * 1000);
	await login();


	await $.wait(4 * 1000);
	await SignIn(); //先签到
	await $.wait(4 * 1000);

	//分享
	for (var i = 0; i < 10; i++) {
		let tt = randomInt(3, 6); //随机暂停时间
		GetCtid(i);
		await share();
		await $.wait(tt * 1000);
	}

	//两次视频
	let c;
	c = randomInt(4, 8);  //随机暂停时间
	await lookVideo();  //看视频
	await $.wait(c * 1000);
	await lookVideo();  //看视频
	c = randomInt(10, 15);
	await $.wait(c * 1000);
	randomsort(randomdisscusarr);

	//发表话题并且评论
	for (var i = 0; i < 5; i++) {
		GetPoem(i);
		await PublishTitle();
		c = randomInt(3, 7);
		await $.wait(c * 1000);
		await GetTitleID();
		c = randomInt(3, 7);
		await $.wait(c * 1000);
		await DiscussTitle(i);
		c = randomInt(3, 7);
		await $.wait(c * 1000);
		await DiscussTitle(randomdisscusarr.length - 1 - i);
		c = randomInt(3, 7);
		await $.wait(c * 1000);

	}


	await LuckyDraw();
	c = randomInt(3, 6);
	await $.wait(c * 1000);
	await ShareLuckyDraw();
	c = randomInt(4, 6);
	await $.wait(c * 1000);
	await LuckyDraw();
	c = randomInt(2, 6);
	await $.wait(c * 1000);


	await Update_wallet();

	await $.wait(2 * 1000);

}





/**
 * 分享    httpPost
 */


async function share() {

	let t = ts10();   //时间
	let bd = 'content_id=' + ctid + '&content_type=1&share_source=';
	let encry_str = 'channel=baidu&content_id=' + ctid + '&content_type=1&device_model=MIX2&from=android&path=/share/statistic&sdk_int=28&share_source=&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + '&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/share/statistic?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;
	//console.log("加密段   "+encry_str);
	//console.log("sn    "+snstr);
	//console.log("地址     :"+str);

	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Length': '47',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},
			body: bd

		};

		let result = await httpPost(pack, `分享`);

		//console.log(result);
		if (result.code == 0) {
			DoubleLog(result.data.msg);
			await wait(3);
		}
		else if (result.code == 60024) {
			DoubleLog(result.msg);
			await wait(3);
		}
		else {
			//DoubleLog(`分享失败了,原因未知!`);
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}

//登录
async function login() {
	let t = ts10();   //时间

	let bd = 'username=' + ck[0] + '&password=' + ck[1] + '&country_code=86';
	let encry_str = 'channel=baidu&country_code=86&device_model=MIX2&from=android&password=' + ck[1] + '&path=/account/loginByPass&sdk_int=28&system_version=android9&timestamp=' + t + '&token=&tourist_token=' + uid + '&username=' + ck[0] + '&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/account/loginByPass?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=&sn=' + snstr;

	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Length': '55',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},
			body: bd

		};
		let result = await httpPost(pack, `登录`);
		_token = result.data.token;

		//console.log(result.data.token);
		if (result.code == 0) {
			DoubleLog('登录' + result.msg);
			await wait(3);
		} else {
			//DoubleLog(`登录失败了,原因未知!`);
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}


//退出登录
async function logout() {
	let t = ts10();   //时间
	let encry_str = 'channel=baidu&device_model=MIX2&from=android&path=/account/logout&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/account/logout?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=&token=' + _token + '&sn=' + snstr;

	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Length': '0',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},

		};
		let result = await httpPost(pack, `退出登录`);

		console.log(result);
		if (result.code == 0) {
			DoubleLog('退出登录' + result.msg);
			await wait(3);
		} else {
			DoubleLog(`退出登录失败了,原因未知!`);
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}




/**
 * 签到    httpPost
 */
async function SignIn() {
	let t = ts10();   //时间
	let bd = 'sign_day=' + local_year() + '-' + local_month_two() + '-' + local_day_two();
	let encry_str = 'channel=baidu&device_model=MIX2&from=android&path=/signin/doSign&sdk_int=28&' + bd + '&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + '&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/signin/doSign?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;

	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Length': '19',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},
			body: bd

		};
		let result = await httpPost(pack, `签到`);

		// console.log(result);
		if (result.code == 0) {
			DoubleLog('签到成功,获得积分' + result.data.point);
			await wait(3);
		}
		else if (result.code == 10082) {
			DoubleLog(result.msg);
			await wait(3);
		}
		else {
			// DoubleLog(`查询: 失败 ❌ 了呢,原因未知!`);
			// console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}


/**
 * 看视频   httpPost
 */
async function lookVideo() {
	let t = ts10();   //时间
	let bd = 'item_id=5376&type=2';
	let encry_str = 'channel=baidu&device_model=MIX2&from=android&item_id=5376&path=/point/addPoint&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + "&type=2" + '&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/point/addPoint?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;

	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Length': '19',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},
			body: bd

		};
		let result = await httpPost(pack, `看视频`);

		//console.log(result);
		if (result.code == 0) {
			DoubleLog('看视频成功,获得积分' + result.data.msg);
			await wait(3);
		}
		//else if(result.code ==10082)
		//{
		// DoubleLog(result.msg);
		// await wait(3);
		//}
		else {
			// DoubleLog('看视频错误，原因未知');
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}


/**
 * 发动态   httpPost
 */
async function PublishTitle() {
	let t = ts10();   //时间
	let poem_change = encodeURI(poemtxt[_poem]);
	//let poem_change=encodeURI('梦里寻他千百度,那人却在灯火阑珊处');
	let bd = 'content=' + poem_change + '&from=android&groupId=' + mygroupId + '&repostId=0&sourceId=0&sourceType=weibo&title=&type=3'
	let encry_str = 'channel=baidu&content=' + poemtxt[_poem] + '&device_model=MIX2&from=android&groupId=' + mygroupId + '&path=/weibo/issueWeibo&repostId=0&sdk_int=28&sourceId=0&sourceType=weibo&system_version=android9&timestamp=' + t + '&title=' + '&token=' + _token + '&tourist_token=' + uid + "&type=3" + '&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/weibo/issueWeibo?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;
	//console.log("发动态加密段   "+encry_str);
	//console.log("发动态sn    "+snstr);
	//console.log("发动态     :"+str);
	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Length': '213',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},
			body: bd

		};
		let result = await httpPost(pack, `发动态`);

		// console.log(result);
		if (result.code == 0) {
			DoubleLog(result.data.msg);
			await wait(3);
		}
		//else if(result.code ==10082)
		//{
		// DoubleLog(result.msg);
		// await wait(3);
		//}
		else {
			// DoubleLog('发动态错误，原因未知');
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}

/**
  * 发评论   httpPost
  */
async function DiscussTitle(id) {
	let t = ts10();   //时间
	let discuss_change = encodeURI(discusstxt[randomdisscusarr[id]]);
	//let poem_change=encodeURI('梦里寻他千百度,那人却在灯火阑珊处');
	let bd = 'content=' + discuss_change + '&fromId=' + _weiboid + '&pid=0&type=1&commentId=0&longitude=0.0&latitude=0.0';
	let encry_str = 'channel=baidu&commentId=0&content=' + discusstxt[randomdisscusarr[id]] + '&device_model=MIX2&from=android&fromId=' + _weiboid + '&latitude=0.0&longitude=0.0&path=/comment/addComment&pid=0&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + '&type=1&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/comment/addComment?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;

	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Length': '219',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},
			body: bd

		};
		let result = await httpPost(pack, `发评论`);

		// console.log(result);
		if (result.code == 0) {
			DoubleLog(result.data.msg);
			await wait(3);
		}
		//else if(result.code ==10082)
		//{
		// DoubleLog(result.msg);
		// await wait(3);
		//}
		else {
			// DoubleLog('发评论错误，原因未知');
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}



/**
  * 删动态
  */
async function DelTitle() {
	let t = ts10();   //时间
	let bd = 'weiBoId=' + _weiboid;
	let encry_str = 'channel=baidu&device_model=MIX2&from=android&path=/weibo/delWeibo&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + '&uuid=' + uid + '&v=5.5.1&weiBoId=' + _weiboid + '&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/weibo/delWeibo?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;

	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Length': '15',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},
			body: bd

		};
		let result = await httpPost(pack, `删动态`);

		//console.log(result);
		if (result.code == 0) {
			DoubleLog('删动态' + result.msg);
			await wait(3);
		}
		//else if(result.code ==10082)
		//{
		// DoubleLog(result.msg);
		// await wait(3);
		//}
		else {
			DoubleLog('删动态错误，原因未知');
			//console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}


//获取动态ID
async function GetTitleID() {
	let t = ts10();   //时间
	let encry_str = 'channel=baidu&device_model=MIX2&from=android&path=/weibo/getMyWeibolist&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + '&uuid=' + uid + '&v=5.5.1&weiBoId=0&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/weibo/getMyWeibolist?weiBoId=0&timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;
	// console.log("登录加密段   "+encry_str);
	//console.log("登录sn    "+snstr);
	//console.log("登录地址     :"+str);
	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},

		};
		let result = await httpGet(pack, `查ID`);

		if (result.code == 0) {
			_weiboid = result.data[0].id;
			DoubleLog('获取成功ID' + _weiboid);
			await wait(3);
		} else {
			// DoubleLog(`获取失败了,原因未知!`);
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}


//更新额度
async function Update_wallet() {
	let t = ts10();   //时间
	let encry_str = 'channel=baidu&device_model=MIX2&from=android&path=/point/exchangeRule&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + '&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/point/exchangeRule?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;
	// console.log("登录加密段   "+encry_str);
	//console.log("登录sn    "+snstr);
	//console.log("登录地址     :"+str);
	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},

		};
		let result = await httpGet(pack, `更新钱包额度`);
		//console.log(result);
		if (result.code == 0) {
			DoubleLog('额度为' + result.data.exchange_point);
			DoubleLog('积分为' + result.data.current_point);
			await wait(3);
		} else {
			// DoubleLog(`更新额度失败了,原因未知!`);
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}


/**
  * 设置Token   httpPost
  */
async function SetToken() {
	let t = ts10();   //时间
	let bd = 'device_token=AoaY6KKBmSipivfHjjW9bq9--MLsPLAZBm7ZRg1QkeYu';
	let encry_str = 'channel=huawei&device_model=MIX2&device_token=AoaY6KKBmSipivfHjjW9bq9--MLsPLAZBm7ZRg1QkeYu&from=android&path=/push/setToken&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	let snstr = sm3(encry_str);
	let str = 'https://api-kejia.scimall.org.cn/push/setToken?timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=huawei&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;

	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Content-Length': '57',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},
			body: bd

		};
		let result = await httpPost(pack, `设置Token`);

		console.log(result);
		if (result.code == 0) {
			DoubleLog(result.data.msg);
			await wait(3);
		}

		else {
			DoubleLog('设置Token错误，原因未知');
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}

//更新信息相关1  //0是signInfo 1是DAILYTASK 2-3是BAnner
async function UpdateInfoFirst(j) {
	let t = ts10();   //时间
	let encry_str;
	if (j == 0) {
		encry_str = 'channel=baidu&device_model=MIX2&from=android&path=/signin/getSignInfo&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + '&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	}
	else if (j == 1) {
		encry_str = 'channel=baidu&device_model=MIX2&from=android&path=/task/dailyTask&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + '&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	}
	else {
		encry_str = 'channel=baidu&device_model=MIX2&from=android&path=/banner/getBannerInfo&place=' + j + '&sdk_int=28&system_version=android9&timestamp=' + t + '&token=' + _token + '&tourist_token=' + uid + '&uuid=' + uid + '&v=5.5.1&secretkey=LH6064#!@&YTM';
	}
	let snstr = sm3(encry_str);
	let str;
	if (j == 0) {
		str = 'https://api-kejia.scimall.org.cn/signin/getSignInfo?&timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;
	}
	else if (j == 1) {
		str = 'https://api-kejia.scimall.org.cn/task/dailyTask?&timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;
	}
	else {
		str = 'https://api-kejia.scimall.org.cn/banner/getBannerInfo?place=' + j + '&timestamp=' + t + '&v=5.5.1&from=android&device_model=MIX2&channel=baidu&system_version=android9&sdk_int=28' + '&uuid=' + uid + '&tourist_token=' + uid + '&token=' + _token + '&sn=' + snstr;
	}
	// console.log("登录加密段   "+encry_str);
	//console.log("登录sn    "+snstr);
	//console.log("登录地址     :"+str);
	try {
		let pack = {
			url: str,
			headers: {
				'Host': host,
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'okhttp/4.2.2',
				'Connection': 'Keep-Alive'
			},

		};
		let result = await httpGet(pack, `更新信息`);
		console.log(result);
		if (result.code == 0) {
			DoubleLog('更新成功');
			await wait(3);
		} else {
			DoubleLog(`更新失败了,原因未知!`);
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}




//抽奖
async function LuckyDraw() {
	let t = ts10();   //时间
	let str = 'https://h5.scimall.org.cn/Signdraw/ajaxDraw?token=' + _token + '&lottery_id=165'
	try {
		let pack = {
			url: str,
			headers: {
				'Host': 'h5.scimall.org.cn',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MIX 2 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 SciMall/5.5.1;',
				'Cookie': 'PHPSESSION=4tb00jvd00m1i1oje1l8v9rrd3; acw_tc=2760820416611817117308644efdbb76b8441f45f9863fe145c30793d6a756;',
				'Connection': 'Keep-Alive'
			},

		};
		let result = await httpGet(pack, `抽奖`);

		if (result.code == 0) {
			//_weiboid=result.data[0].id;
			DoubleLog('抽奖获得' + result.data.msg);
			await wait(3);
		} else {
			// DoubleLog(`抽奖失败了,原因未知!`);
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}

//分享获取抽奖机会
async function ShareLuckyDraw() {
	let t = ts10();   //时间
	let str = 'https://h5.scimall.org.cn/Signdraw/ajaxShare?token=' + _token + '&lottery_id=165'

	try {
		let pack = {
			url: str,
			headers: {
				'Host': 'h5.scimall.org.cn',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json;charset=UTF-8',
				'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MIX 2 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 SciMall/5.5.1;',
				'Cookie': 'PHPSESSION=4tb00jvd00m1i1oje1l8v9rrd3;',
				'Connection': 'Keep-Alive'
			},

		};
		let result = await httpGet(pack, `分享抽奖`);
		// console.log(result);
		if (result.code == 0) {
			//_weiboid=result.data[0].id;
			DoubleLog('分享' + result.msg);
			await wait(3);
		} else {
			//DoubleLog(`分享失败了,原因未知!`);
			console.log(result);
		}
	} catch (error) {
		console.log(error);
	}

}









// #region ********************************************************  固定代码  ********************************************************
/**
 * 变量检查
 */
async function checkEnv(ck, Variables) {
	return new Promise((resolve) => {
		let ckArr = []
		if (ck) {
			if (ck.indexOf("@") !== -1) {

				ck.split("@").forEach((item) => {
					ckArr.push(item);
				});
			} else if (ck.indexOf("\n") !== -1) {

				ck.split("\n").forEach((item) => {
					ckArr.push(item);
				});
			} else {
				ckArr.push(ck);
			}
			resolve(ckArr)
		} else {
			console.log(` ${$.neme}:未填写变量 ${Variables} ,请仔细阅读脚本说明!`)
		}
	}
	)
}




/**
 * 发送消息
 */
async function SendMsg(message) {
	if (!message) return;
	if (Notify > 0) {
		if ($.isNode()) {
			var notify = require("../../sendNotify");
			await notify.sendNotify($.name, message);
		} else {
			// $.msg(message);
			$.msg($.name, '', message)
		}
	} else {
		console.log(message);
	}
}

/**
 * 双平台log输出
 */
function DoubleLog(data) {
	if ($.isNode()) {
		if (data) {
			console.log(`    ${data}`);
			msg += `\n    ${data}`;
		}
	} else {
		console.log(`    ${data}`);
		msg += `\n    ${data}`;
	}

}

/**
 * 随机 数字 + 大写字母 生成
 */
function randomszdx(e) {
	e = e || 32;
	var t = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890",
		a = t.length,
		n = "";

	for (i = 0; i < e; i++) n += t.charAt(Math.floor(Math.random() * a));
	return n;
}


/**
 * 随机 数字 + 小写字母 生成
 */
function randomszxx(e) {
	e = e || 32;
	var t = "qwertyuioplkjhgfdsazxcvbnm1234567890",
		a = t.length,
		n = "";

	for (i = 0; i < e; i++) n += t.charAt(Math.floor(Math.random() * a));
	return n;
}




/**
 * 随机整数生成
 */
function randomInt(min, max) {
	return Math.round(Math.random() * (max - min) + min);
}


/**
 * 时间戳 13位
 */
function ts13() {
	return Math.round(new Date().getTime()).toString();
}

/**
 * 时间戳 10位
 */
function ts10() {
	return Math.round(new Date().getTime() / 1000).toString();
}

/**
 * 获取当前小时数
 */
function local_hours() {
	let myDate = new Date();
	let h = myDate.getHours();
	return h;
}

/**
 * 获取当前分钟数
 */
function local_minutes() {
	let myDate = new Date();
	let m = myDate.getMinutes();
	return m;
}


/**
 * 获取当前年份 2022
 */
function local_year() {
	let myDate = new Date();
	y = myDate.getFullYear();
	return y;
}

/**
 * 获取当前月份(数字)  5月
 */
function local_month() {
	let myDate = new Date();
	let m = myDate.getMonth();
	return m;
}


/**
* 获取当前月份(数字)  05月 补零
*/
function local_month_two() {
	let myDate = new Date();
	let m = myDate.getMonth();
	m = m + 1;
	if (m.toString().length == 1) {
		m = `0${m}`
	}
	return m;
}

/**
* 获取当前天数(数字)  5日
*/
function local_day() {
	let myDate = new Date();
	let d = myDate.getDate();
	return d;
}


/**
* 获取当前天数  05日 补零
*/
function local_day_two() {
	let myDate = new Date();
	let d = myDate.getDate();
	if (d.toString().length == 1) {
		d = `0${d}`
	}
	return d;
}



/**
 * 等待 X 秒
 */
function wait(n) {
	return new Promise(function (resolve) {
		setTimeout(resolve, n * 1000);
	});
}


/**
 * 每日网抑云
 */
function wyy() {
	return new Promise((resolve) => {
		let url = {
			url: `http://ovooa.com/API/wyrp/api.php`,
		}
		$.get(url, async (err, resp, data) => {
			try {
				data = JSON.parse(data);
				// console.log(data);
				console.log(`网抑云时间: ${data.data.Content}  by--${data.data.Music}`)
				msg = `[网抑云时间]: ${data.data.Content}  by--${data.data.Music}`
				// DoubleLog(`[网抑云时间]: ${data.data.Content}  by--${data.data.Music}`);
			} catch (e) {
				$.logErr(e, resp);
			} finally {
				resolve()
			}
		}, timeout = 3)
	})
}

/**
 * get请求
 */
async function httpGet(getUrlObject, tip, timeout = 3) {
	return new Promise((resolve) => {
		let url = getUrlObject;
		if (!tip) {
			let tmp = arguments.callee.toString();
			let re = /function\s*(\w*)/i;
			let matches = re.exec(tmp);
			tip = matches[1];
		}
		if (debug) {
			console.log(`\n 【debug】=============== 这是 ${tip} 请求 url ===============`);
			console.log(url);
		}

		$.get(
			url,
			async (err, resp, data) => {
				try {
					if (debug) {
						console.log(`\n\n 【debug】===============这是 ${tip} 返回data==============`);
						console.log(data);
						console.log(`\n 【debug】=============这是 ${tip} json解析后数据============`);
						console.log(JSON.parse(data));
					}
					let result = JSON.parse(data);
					if (result == undefined) {
						return;
					} else {
						resolve(result);
					}

				} catch (e) {
					console.log(err, resp);
					console.log(`\n ${tip} 失败了!请稍后尝试!!`);
					msg = `\n ${tip} 失败了!请稍后尝试!!`
				} finally {
					resolve();
				}
			},
			timeout
		);
	});
}





//随机排序
function randomsort(arr) {
	arr.sort(function () {
		return Math.random() - 0.5
	})
}

//获取文章用
function GetCtid(j) {

	ctid = sharebox[j];
}


//获取诗词用
function GetPoem(j) {
	if (j == 0) _poem = randomInt(0, 4);
	if (j == 1) _poem = randomInt(5, 9);
	if (j == 2) _poem = randomInt(10, 14);
	if (j == 3) _poem = randomInt(15, 19);
	if (j == 4) _poem = randomInt(20, 24);
}



/**
 * post请求
 */
async function httpPost(postUrlObject, tip, timeout = 3) {
	return new Promise((resolve) => {
		let url = postUrlObject;
		if (!tip) {
			let tmp = arguments.callee.toString();
			let re = /function\s*(\w*)/i;
			let matches = re.exec(tmp);
			tip = matches[1];
		}
		if (debug) {
			console.log(`\n 【debug】=============== 这是 ${tip} 请求 url ===============`);
			console.log(url);
		}

		$.post(
			url,
			async (err, resp, data) => {
				try {
					if (debug) {
						console.log(`\n\n 【debug】===============这是 ${tip} 返回data==============`);
						console.log(data);
						console.log(`\n 【debug】=============这是 ${tip} json解析后数据============`);
						console.log(JSON.parse(data));
					}
					let result = JSON.parse(data);
					if (result == undefined) {
						return;
					} else {
						resolve(result);
					}

				} catch (e) {
					console.log(err, resp);
					console.log(`\n ${tip} 失败了!请稍后尝试!!`);
					msg = `\n ${tip} 失败了!请稍后尝试!!`
				} finally {
					resolve();
				}
			},
			timeout
		);
	});
}

/**
 * 网络请求 (get, post等)
 */
async function httpRequest(postOptionsObject, tip, timeout = 3) {
	return new Promise((resolve) => {

		let Options = postOptionsObject;
		let request = require('request');
		if (!tip) {
			let tmp = arguments.callee.toString();
			let re = /function\s*(\w*)/i;
			let matches = re.exec(tmp);
			tip = matches[1];
		}
		if (debug) {
			console.log(`\n 【debug】=============== 这是 ${tip} 请求 信息 ===============`);
			console.log(Options);
		}

		request(Options, async (err, resp, data) => {
			try {
				if (debug) {
					console.log(`\n\n 【debug】===============这是 ${tip} 返回数据==============`);
					console.log(data);
					console.log(`\n 【debug】=============这是 ${tip} json解析后数据============`);
					console.log(JSON.parse(data));
				}
				let result = JSON.parse(data);
				if (!result) return;
				resolve(result);
			} catch (e) {
				console.log(err, resp);
				console.log(`\n ${tip} 失败了!请稍后尝试!!`);
				msg = `\n ${tip} 失败了!请稍后尝试!!`
			} finally {
				resolve();
			}
		}), timeout

	});
}


/**
 * debug调试
 */
function debugLog(...args) {
	if (debug) {
		console.log(...args);
	}
}



// /**
//  *  单名字 Env
//  */
// function Env() {
//     return new class {
//         isNode() {
//             return "undefined" != typeof module && !!module.exports
//         }
//     }()
// }


// md5
function MD5Encrypt(a) { function b(a, b) { return a << b | a >>> 32 - b } function c(a, b) { var c, d, e, f, g; return e = 2147483648 & a, f = 2147483648 & b, c = 1073741824 & a, d = 1073741824 & b, g = (1073741823 & a) + (1073741823 & b), c & d ? 2147483648 ^ g ^ e ^ f : c | d ? 1073741824 & g ? 3221225472 ^ g ^ e ^ f : 1073741824 ^ g ^ e ^ f : g ^ e ^ f } function d(a, b, c) { return a & b | ~a & c } function e(a, b, c) { return a & c | b & ~c } function f(a, b, c) { return a ^ b ^ c } function g(a, b, c) { return b ^ (a | ~c) } function h(a, e, f, g, h, i, j) { return a = c(a, c(c(d(e, f, g), h), j)), c(b(a, i), e) } function i(a, d, f, g, h, i, j) { return a = c(a, c(c(e(d, f, g), h), j)), c(b(a, i), d) } function j(a, d, e, g, h, i, j) { return a = c(a, c(c(f(d, e, g), h), j)), c(b(a, i), d) } function k(a, d, e, f, h, i, j) { return a = c(a, c(c(g(d, e, f), h), j)), c(b(a, i), d) } function l(a) { for (var b, c = a.length, d = c + 8, e = (d - d % 64) / 64, f = 16 * (e + 1), g = new Array(f - 1), h = 0, i = 0; c > i;)b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | a.charCodeAt(i) << h, i++; return b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | 128 << h, g[f - 2] = c << 3, g[f - 1] = c >>> 29, g } function m(a) { var b, c, d = "", e = ""; for (c = 0; 3 >= c; c++)b = a >>> 8 * c & 255, e = "0" + b.toString(16), d += e.substr(e.length - 2, 2); return d } function n(a) { a = a.replace(/\r\n/g, "\n"); for (var b = "", c = 0; c < a.length; c++) { var d = a.charCodeAt(c); 128 > d ? b += String.fromCharCode(d) : d > 127 && 2048 > d ? (b += String.fromCharCode(d >> 6 | 192), b += String.fromCharCode(63 & d | 128)) : (b += String.fromCharCode(d >> 12 | 224), b += String.fromCharCode(d >> 6 & 63 | 128), b += String.fromCharCode(63 & d | 128)) } return b } var o, p, q, r, s, t, u, v, w, x = [], y = 7, z = 12, A = 17, B = 22, C = 5, D = 9, E = 14, F = 20, G = 4, H = 11, I = 16, J = 23, K = 6, L = 10, M = 15, N = 21; for (a = n(a), x = l(a), t = 1732584193, u = 4023233417, v = 2562383102, w = 271733878, o = 0; o < x.length; o += 16)p = t, q = u, r = v, s = w, t = h(t, u, v, w, x[o + 0], y, 3614090360), w = h(w, t, u, v, x[o + 1], z, 3905402710), v = h(v, w, t, u, x[o + 2], A, 606105819), u = h(u, v, w, t, x[o + 3], B, 3250441966), t = h(t, u, v, w, x[o + 4], y, 4118548399), w = h(w, t, u, v, x[o + 5], z, 1200080426), v = h(v, w, t, u, x[o + 6], A, 2821735955), u = h(u, v, w, t, x[o + 7], B, 4249261313), t = h(t, u, v, w, x[o + 8], y, 1770035416), w = h(w, t, u, v, x[o + 9], z, 2336552879), v = h(v, w, t, u, x[o + 10], A, 4294925233), u = h(u, v, w, t, x[o + 11], B, 2304563134), t = h(t, u, v, w, x[o + 12], y, 1804603682), w = h(w, t, u, v, x[o + 13], z, 4254626195), v = h(v, w, t, u, x[o + 14], A, 2792965006), u = h(u, v, w, t, x[o + 15], B, 1236535329), t = i(t, u, v, w, x[o + 1], C, 4129170786), w = i(w, t, u, v, x[o + 6], D, 3225465664), v = i(v, w, t, u, x[o + 11], E, 643717713), u = i(u, v, w, t, x[o + 0], F, 3921069994), t = i(t, u, v, w, x[o + 5], C, 3593408605), w = i(w, t, u, v, x[o + 10], D, 38016083), v = i(v, w, t, u, x[o + 15], E, 3634488961), u = i(u, v, w, t, x[o + 4], F, 3889429448), t = i(t, u, v, w, x[o + 9], C, 568446438), w = i(w, t, u, v, x[o + 14], D, 3275163606), v = i(v, w, t, u, x[o + 3], E, 4107603335), u = i(u, v, w, t, x[o + 8], F, 1163531501), t = i(t, u, v, w, x[o + 13], C, 2850285829), w = i(w, t, u, v, x[o + 2], D, 4243563512), v = i(v, w, t, u, x[o + 7], E, 1735328473), u = i(u, v, w, t, x[o + 12], F, 2368359562), t = j(t, u, v, w, x[o + 5], G, 4294588738), w = j(w, t, u, v, x[o + 8], H, 2272392833), v = j(v, w, t, u, x[o + 11], I, 1839030562), u = j(u, v, w, t, x[o + 14], J, 4259657740), t = j(t, u, v, w, x[o + 1], G, 2763975236), w = j(w, t, u, v, x[o + 4], H, 1272893353), v = j(v, w, t, u, x[o + 7], I, 4139469664), u = j(u, v, w, t, x[o + 10], J, 3200236656), t = j(t, u, v, w, x[o + 13], G, 681279174), w = j(w, t, u, v, x[o + 0], H, 3936430074), v = j(v, w, t, u, x[o + 3], I, 3572445317), u = j(u, v, w, t, x[o + 6], J, 76029189), t = j(t, u, v, w, x[o + 9], G, 3654602809), w = j(w, t, u, v, x[o + 12], H, 3873151461), v = j(v, w, t, u, x[o + 15], I, 530742520), u = j(u, v, w, t, x[o + 2], J, 3299628645), t = k(t, u, v, w, x[o + 0], K, 4096336452), w = k(w, t, u, v, x[o + 7], L, 1126891415), v = k(v, w, t, u, x[o + 14], M, 2878612391), u = k(u, v, w, t, x[o + 5], N, 4237533241), t = k(t, u, v, w, x[o + 12], K, 1700485571), w = k(w, t, u, v, x[o + 3], L, 2399980690), v = k(v, w, t, u, x[o + 10], M, 4293915773), u = k(u, v, w, t, x[o + 1], N, 2240044497), t = k(t, u, v, w, x[o + 8], K, 1873313359), w = k(w, t, u, v, x[o + 15], L, 4264355552), v = k(v, w, t, u, x[o + 6], M, 2734768916), u = k(u, v, w, t, x[o + 13], N, 1309151649), t = k(t, u, v, w, x[o + 4], K, 4149444226), w = k(w, t, u, v, x[o + 11], L, 3174756917), v = k(v, w, t, u, x[o + 2], M, 718787259), u = k(u, v, w, t, x[o + 9], N, 3951481745), t = c(t, p), u = c(u, q), v = c(v, r), w = c(w, s); var O = m(t) + m(u) + m(v) + m(w); return O.toLowerCase() }




/* SHA256 logical functions */
function rotateRight(n, x) {
	return ((x >>> n) | (x << (32 - n)));
}
function choice(x, y, z) {
	return ((x & y) ^ (~x & z));
}
function majority(x, y, z) {
	return ((x & y) ^ (x & z) ^ (y & z));
}
function sha256_Sigma0(x) {
	return (rotateRight(2, x) ^ rotateRight(13, x) ^ rotateRight(22, x));
}
function sha256_Sigma1(x) {
	return (rotateRight(6, x) ^ rotateRight(11, x) ^ rotateRight(25, x));
}
function sha256_sigma0(x) {
	return (rotateRight(7, x) ^ rotateRight(18, x) ^ (x >>> 3));
}
function sha256_sigma1(x) {
	return (rotateRight(17, x) ^ rotateRight(19, x) ^ (x >>> 10));
}
function sha256_expand(W, j) {
	return (W[j & 0x0f] += sha256_sigma1(W[(j + 14) & 0x0f]) + W[(j + 9) & 0x0f] +
		sha256_sigma0(W[(j + 1) & 0x0f]));
}

/* Hash constant words K: */
var K256 = new Array(
	0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
	0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
	0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
	0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
	0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
	0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
	0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
	0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
	0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
	0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
	0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
	0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
	0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
	0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
	0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
	0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
);

/* global arrays */
var ihash, count, buffer;
var sha256_hex_digits = "0123456789abcdef";

/* Add 32-bit integers with 16-bit operations (bug in some JS-interpreters:
overflow) */
function safe_add(x, y) {
	var lsw = (x & 0xffff) + (y & 0xffff);
	var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
	return (msw << 16) | (lsw & 0xffff);
}

/* Initialise the SHA256 computation */
function sha256_init() {
	ihash = new Array(8);
	count = new Array(2);
	buffer = new Array(64);
	count[0] = count[1] = 0;
	ihash[0] = 0x6a09e667;
	ihash[1] = 0xbb67ae85;
	ihash[2] = 0x3c6ef372;
	ihash[3] = 0xa54ff53a;
	ihash[4] = 0x510e527f;
	ihash[5] = 0x9b05688c;
	ihash[6] = 0x1f83d9ab;
	ihash[7] = 0x5be0cd19;
}

/* Transform a 512-bit message block */
function sha256_transform() {
	var a, b, c, d, e, f, g, h, T1, T2;
	var W = new Array(16);

	/* Initialize registers with the previous intermediate value */
	a = ihash[0];
	b = ihash[1];
	c = ihash[2];
	d = ihash[3];
	e = ihash[4];
	f = ihash[5];
	g = ihash[6];
	h = ihash[7];

	/* make 32-bit words */
	for (var i = 0; i < 16; i++)
		W[i] = ((buffer[(i << 2) + 3]) | (buffer[(i << 2) + 2] << 8) | (buffer[(i << 2) + 1]
			<< 16) | (buffer[i << 2] << 24));

	for (var j = 0; j < 64; j++) {
		T1 = h + sha256_Sigma1(e) + choice(e, f, g) + K256[j];
		if (j < 16) T1 += W[j];
		else T1 += sha256_expand(W, j);
		T2 = sha256_Sigma0(a) + majority(a, b, c);
		h = g;
		g = f;
		f = e;
		e = safe_add(d, T1);
		d = c;
		c = b;
		b = a;
		a = safe_add(T1, T2);
	}

	/* Compute the current intermediate hash value */
	ihash[0] += a;
	ihash[1] += b;
	ihash[2] += c;
	ihash[3] += d;
	ihash[4] += e;
	ihash[5] += f;
	ihash[6] += g;
	ihash[7] += h;
}

/* Read the next chunk of data and update the SHA256 computation */
function sha256_update(data, inputLen) {
	var i, index, curpos = 0;
	/* Compute number of bytes mod 64 */
	index = ((count[0] >> 3) & 0x3f);
	var remainder = (inputLen & 0x3f);

	/* Update number of bits */
	if ((count[0] += (inputLen << 3)) < (inputLen << 3)) count[1]++;
	count[1] += (inputLen >> 29);

	/* Transform as many times as possible */
	for (i = 0; i + 63 < inputLen; i += 64) {
		for (var j = index; j < 64; j++)
			buffer[j] = data.charCodeAt(curpos++);
		sha256_transform();
		index = 0;
	}

	/* Buffer remaining input */
	for (var j = 0; j < remainder; j++)
		buffer[j] = data.charCodeAt(curpos++);
}

/* Finish the computation by operations such as padding */
function sha256_final() {
	var index = ((count[0] >> 3) & 0x3f);
	buffer[index++] = 0x80;
	if (index <= 56) {
		for (var i = index; i < 56; i++)
			buffer[i] = 0;
	} else {
		for (var i = index; i < 64; i++)
			buffer[i] = 0;
		sha256_transform();
		for (var i = 0; i < 56; i++)
			buffer[i] = 0;
	}
	buffer[56] = (count[1] >>> 24) & 0xff;
	buffer[57] = (count[1] >>> 16) & 0xff;
	buffer[58] = (count[1] >>> 8) & 0xff;
	buffer[59] = count[1] & 0xff;
	buffer[60] = (count[0] >>> 24) & 0xff;
	buffer[61] = (count[0] >>> 16) & 0xff;
	buffer[62] = (count[0] >>> 8) & 0xff;
	buffer[63] = count[0] & 0xff;
	sha256_transform();
}



function RandeCode() {
	var d = new Date().getTime();
	var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
		var r = (d + Math.random() * 16) % 16 | 0;
		d = Math.floor(d / 16);
		return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
	});

	return uuid;

};






/* Split the internal hash values into an array of bytes */
function sha256_encode_bytes() {
	var j = 0;
	var output = new Array(32);
	for (var i = 0; i < 8; i++) {
		output[j++] = ((ihash[i] >>> 24) & 0xff);
		output[j++] = ((ihash[i] >>> 16) & 0xff);
		output[j++] = ((ihash[i] >>> 8) & 0xff);
		output[j++] = (ihash[i] & 0xff);
	}
	return output;
}

/* Get the internal hash as a hex string */
function sha256_encode_hex() {
	var output = new String();
	for (var i = 0; i < 8; i++) {
		for (var j = 28; j >= 0; j -= 4)
			output += sha256_hex_digits.charAt((ihash[i] >>> j) & 0x0f);
	}
	return output;
}

/* Main function: returns a hex string representing the SHA256 value of the
given data */
function sha256_Encrypt(data) {
	sha256_init();
	sha256_update(data, data.length);
	sha256_final();
	return sha256_encode_hex();
}



// 完整 Env
function Env(t, e) { "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0); class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return "POST" === e && (s = this.post), new Promise((e, i) => { s.call(this, t, (t, s, r) => { t ? i(t) : e(s) }) }) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new class { constructor(t, e) { this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const i = this.getdata(t); if (i) try { s = JSON.parse(this.getdata(t)) } catch { } return s } setjson(t, e) { try { return this.setdata(JSON.stringify(t), e) } catch { return !1 } } getScript(t) { return new Promise(e => { this.get({ url: t }, (t, s, i) => e(i)) }) } runScript(t, e) { return new Promise(s => { let i = this.getdata("@chavy_boxjs_userCfgs.httpapi"); i = i ? i.replace(/\n/g, "").trim() : i; let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout"); r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r; const [o, h] = i.split("@"), n = { url: `http://${h}/v1/scripting/evaluate`, body: { script_text: t, mock_type: "cron", timeout: r }, headers: { "X-Key": o, Accept: "*/*" } }; this.post(n, (t, e, i) => s(i)) }).catch(t => this.logErr(t)) } loaddata() { if (!this.isNode()) return {}; { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e); if (!s && !i) return {}; { const i = s ? t : e; try { return JSON.parse(this.fs.readFileSync(i)) } catch (t) { return {} } } } } writedata() { if (this.isNode()) { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data); s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r) } } lodash_get(t, e, s) { const i = e.replace(/\[(\d+)\]/g, ".$1").split("."); let r = t; for (const t of i) if (r = Object(r)[t], void 0 === r) return s; return r } lodash_set(t, e, s) { return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t) } getdata(t) { let e = this.getval(t); if (/^@/.test(t)) { const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : ""; if (r) try { const t = JSON.parse(r); e = t ? this.lodash_get(t, i, "") : e } catch (t) { e = "" } } return e } setdata(t, e) { let s = !1; if (/^@/.test(e)) { const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i), h = i ? "null" === o ? null : o || "{}" : "{}"; try { const e = JSON.parse(h); this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i) } catch (e) { const o = {}; this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i) } } else s = this.setval(t, e); return s } getval(t) { return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null } setval(t, e) { return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null } initGotEnv(t) { this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar)) } get(t, e = (() => { })) { t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.get(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => { try { if (t.headers["set-cookie"]) { const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString(); s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar } } catch (t) { this.logErr(t) } }).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) })) } post(t, e = (() => { })) { if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.post(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t)); else if (this.isNode()) { this.initGotEnv(t); const { url: s, ...i } = t; this.got.post(s, i).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) }) } } time(t, e = null) { const s = e ? new Date(e) : new Date; let i = { "M+": s.getMonth() + 1, "d+": s.getDate(), "H+": s.getHours(), "m+": s.getMinutes(), "s+": s.getSeconds(), "q+": Math.floor((s.getMonth() + 3) / 3), S: s.getMilliseconds() }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length))); return t } msg(e = t, s = "", i = "", r) { const o = t => { if (!t) return t; if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? { "open-url": t } : this.isSurge() ? { url: t } : void 0; if ("object" == typeof t) { if (this.isLoon()) { let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"]; return { openUrl: e, mediaUrl: s } } if (this.isQuanX()) { let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl; return { "open-url": e, "media-url": s } } if (this.isSurge()) { let e = t.url || t.openUrl || t["open-url"]; return { url: e } } } }; if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) { let t = ["", "==============📣系统通知📣=============="]; t.push(e), s && t.push(s), i && t.push(i), console.log(t.join("\n")), this.logs = this.logs.concat(t) } } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator)) } logErr(t, e) { const s = !this.isSurge() && !this.isQuanX() && !this.isLoon(); s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t) } wait(t) { return new Promise(e => setTimeout(e, t)) } done(t = {}) { const e = (new Date).getTime(), s = (e - this.startTime) / 1e3; this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t) } }(t, e) }

	 //#endregion
