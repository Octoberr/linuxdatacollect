Easemob.im.config = {
    xmppURL: 'im-api.easemob.com',
    apiURL: 'http://a1.easemob.com',
    appkey: "ehand#ehand",
    https: false,
    multiResources: true
}
Date.prototype.ToFormat = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "h+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S": this.getMilliseconds()
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ?
				(o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
var layim = { easemob: {} };
layim.easemob.conn = new Easemob.im.Connection({
    multiResources: Easemob.im.config.multiResources,
    https: Easemob.im.config.https,
    url: Easemob.im.config.xmppURL
});
//初始化连接
layim.easemob.conn.init({
    https: Easemob.im.config.https,
    url: Easemob.im.config.xmppURL,
    //当连接成功时的回调方法
    onOpened: function () {
        if (layim.easemob.conn.isOpened())
            layim.easemob.conn.heartBeat(layim.easemob.conn);
        layim.easemob.xxim.online();
        layim.easemob.conn.setPresence();
        layim.easemob.conn.getRoster({
            success: function (roster) {
                layim.easemob.xxim.showuser(roster);
            }
        });
    },
    //当连接关闭时的回调方法
    onClosed: function () {
        layim.easemob.xxim.offline();
    },
    //收到文本消息时的回调方法
    onTextMessage: function (message) {
        if (message.ext && message.ext.time) message.time = message.ext.time;
        layim.easemob.xxim.showhistory(message);
    },
    //收到表情消息时的回调方法
    onEmotionMessage: function (message) {
        if (message.ext && message.ext.time) message.time = message.ext.time;
        var h = '';
        $(message.data).each(function (i, item) {
            if (item.type = 'emotion')
                h += '<img src="' + item.data + '" />';
            else if (item.type = 'txt')
                h += item.data;
        });
        message.data = h;
        layim.easemob.xxim.showhistory(message);
    },
    //收到图片消息时的回调方法
    onPictureMessage: function (message) {
        if (message.ext && message.ext.time) message.time = message.ext.time;
        message.data = '<a href="' + message.url + '" target="_blank"><img src="' + message.url + '" /></a>';
        layim.easemob.xxim.showhistory(message);
    },
    //收到音频消息的回调方法
    onAudioMessage: function (message) { },
    //收到位置消息的回调方法
    onLocationMessage: function (message) { },
    //收到文件消息的回调方法
    onFileMessage: function (message) { },
    //收到视频消息的回调方法
    onVideoMessage: function (message) { },
    //收到联系人订阅请求的回调方法
    onPresence: function (message) {
        layim.easemob.xxim.showpresence(message);
    },
    //收到联系人消息的回调方法
    onRoster: function (message) {
        layim.easemob.conn.getRoster({
            success: function (roster) {
                layim.easemob.xxim.showuser(roster);
            }
        });
    },
    //收到群组邀请时的回调方法
    onInviteMessage: function (message) { },
    //异常时的回调方法
    onError: function (message) {
        layim.easemob.conn.curError = message;
    },
    //发送接收到消息
    onSendReceiptsMessage: function (message) {
        return false;
    },
    //透传消息
    onCmdMessage: function (message) {
        if (message.ext && message.ext.time) message.time = message.ext.time;
        for (var key in message.ext) {
            var value = message.ext[key];
            if (key == 'orderno')
                message.action = message.action.replace('[orderno]', '[<a href="/Shop/Order/Info?bllno=' + value + '" class="color-main" target="_blank">' + value + '</a>]');
            else if (key == 'refundno')
                message.action = message.action.replace('[refundno]', '[<a href="/Shop/Order/Refund?bllno=' + message.ext['orderno'] + '" class="color-main" target="_blank">' + value + '</a>]');
            else if (key == 'returnno')
                message.action = message.action.replace('[returnno]', '[<a href="/Shop/Order/Return?bllno=' + message.ext['orderno'] + '&bcd=' + message.ext['bcd'] + '" class="color-main" target="_blank">' + value + '</a>]');
            else if (key == 'sendno')
                message.action = message.action.replace('[sendno]', '[<a href="/Shop/Order/Send?bllno=' + message.ext['orderno'] + '&bcd=' + message.ext['bcd'] + '" class="color-main" target="_blank">' + value + '</a>]');
        }
        message.data = message.action;
        layim.easemob.xxim.showhistory(message);
    }
});
layim.easemob.conn.login = function (user, pwd) {
    layim.easemob.conn.open({
        apiUrl: Easemob.im.config.apiURL,
        user: user,
        pwd: pwd,
        appKey: Easemob.im.config.appkey
    });
    layim.easemob.conn.lastuser = user;
    layim.easemob.conn.lastpwd = pwd;
    layim.easemob.conn.stopInterval();
    layim.easemob.conn.myInterval = window.setInterval(function () {
        if (!layim.easemob.conn.isOpened() && !layim.easemob.conn.isOpening()) {
            layim.easemob.xxim.rconnect();
        }
    }, 2000);
}
layim.easemob.conn.logout = function () {
    layim.easemob.conn.stopHeartBeat(layim.easemob.conn);
    layim.easemob.conn.close();
}
layim.easemob.conn.stopInterval = function () {
    if (layim.easemob.conn.myInterval) {
        window.clearInterval(layim.easemob.conn.myInterval);
        layim.easemob.conn.myInterval = null;
    }
}
layim.easemob.init = function (id, appkey, token, name, photo) {
    Easemob.im.config.appkey = appkey;
    layim.easemob.conn.login(id, token);
    var config = {
        msgurl: 'mailbox.html?msg=',
        chatlogurl: 'mailbox.html?user=',
        aniTime: 200,
        right: -230,
        api: {
            friend: 'js/plugins/layer/layim/data/friend.json', //好友列表接口
            group: 'js/plugins/layer/layim/data/group.json', //群组列表接口
            chatlog: 'js/plugins/layer/layim/data/chatlog.json', //聊天记录接口
            groups: 'js/plugins/layer/layim/data/groups.json', //群组成员接口
            sendurl: '' //发送消息接口
        },
        user: { //当前用户信息
            name: name,
            face: photo
        },
        //自动回复内置文案，也可动态读取数据库配置
        autoReplay: [
            '您好，我现在有事不在，一会再和您联系。',
            '你没发错吧？',
            '洗澡中，请勿打扰，偷窥请购票，个体四十，团体八折，订票电话：一般人我不告诉他！',
            '你好，我是主人的美女秘书，有什么事就跟我说吧，等他回来我会转告他的。',
            '我正在拉磨，没法招呼您，因为我们家毛驴去动物保护协会把我告了，说我剥夺它休产假的权利。',
            '<（@￣︶￣@）>',
            '你要和我说话？你真的要和我说话？你确定自己想说吗？你一定非说不可吗？那你说吧，这是自动回复。',
            '主人正在开机自检，键盘鼠标看好机会出去凉快去了，我是他的电冰箱，我打字比较慢，你慢慢说，别急……',
            '(*^__^*) 嘻嘻，是贤心吗？'
        ],
        chating: {},
        chatmsg: {},
        chatuser: {},
        presences: [],
        hosts: (function () {
            var dk = location.href.match(/\:\d+/);
            dk = dk ? dk[0] : '';
            return 'http://' + document.domain + dk + '/';
        })(),
        json: function (url, data, callback, error) {
            return $.ajax({
                type: 'POST',
                url: url,
                data: data,
                dataType: 'json',
                success: callback,
                error: error
            });
        },
        stopMP: function (e) {
            e ? e.stopPropagation() : e.cancelBubble = true;
        }
    }, dom = [$(window), $(document), $('html'), $('body')], xxim = {};
    layim.easemob.xxim = xxim;
    xxim.rconnect = function () {
        xxim.node.rconnect.html('').addClass('loading');
        layim.easemob.conn.login(id, token);
    }
    xxim.offline = function () {
        xxim.node.onlinetex.html('离线');
        xxim.node.online.addClass('xxim_offline');
        xxim.node.rconnect.removeClass('loading').html('重连');
        xxim.node.layimMin.parent().addClass('xxim_bottom_offline')
        if (xxim.layimNode.attr('state') != '1') xxim.expend();
        if (xxim.chatbox) xxim.chatbox.find('.layim_close').click();
        if (xxim.presencebox) layer.close(xxim.presencebox.parent().parent().attr('times'));
        xxim.node.list.find('.xxim_chatlist').html('');
        config.chatmsg = {};
        config.presences = [];
        xxim.showcount();
    }
    xxim.online = function () {
        xxim.node.onlinetex.html('在线');
        xxim.node.online.removeClass('xxim_offline');
        xxim.node.list.removeClass('loading');
        xxim.node.layimMin.parent().removeClass('xxim_bottom_offline');
        xxim.gochat();
    }
    //主界面tab
    xxim.tabs = function (index) {
        var node = xxim.node;
        node.tabs.eq(index).addClass('xxim_tabnow').siblings().removeClass('xxim_tabnow');
        node.list.eq(index).show().siblings('.xxim_list').hide();
        if (node.list.eq(index).find('li').length === 0) {
        }
    };

    //节点
    xxim.renode = function () {
        var node = xxim.node = {
            tabs: $('#xxim_tabs>span'),
            list: $('.xxim_list'),
            online: $('.xxim_online'),
            setonline: $('.xxim_setonline'),
            onlinetex: $('#xxim_onlinetex'),
            xximon: $('#xxim_on'),
            layimFooter: $('#xxim_bottom'),
            xximHide: $('#xxim_hide'),
            xximSearch: $('#xxim_searchkey'),
            searchMian: $('#xxim_searchmain'),
            closeSearch: $('#xxim_closesearch'),
            layimMin: $('#xxim_mymsg'),
            rconnect: $('#xxim_rconnect')
        };
    };

    //主界面缩放
    xxim.expend = function () {
        if (layim.easemob.noexpend) return;
        var node = xxim.node;
        if (xxim.layimNode.attr('state') !== '1') {
            xxim.layimNode.stop().animate({ right: config.right }, config.aniTime, function () {
                node.xximon.addClass('xxim_off');
                try {
                    localStorage.layimState = 1;
                } catch (e) { }
                xxim.layimNode.attr({ state: 1 });
                node.xximHide.addClass('xxim_show');
            });
            node.layimFooter.addClass('xxim_expend').stop().animate({ marginLeft: config.right }, config.aniTime);
        } else {
            xxim.layimNode.stop().animate({ right: 0 }, config.aniTime, function () {
                node.xximon.removeClass('xxim_off');
                try {
                    localStorage.layimState = 2;
                } catch (e) { }
                xxim.layimNode.removeAttr('state');
                node.layimFooter.removeClass('xxim_expend');
                node.xximHide.removeClass('xxim_show');
            });
            node.layimFooter.stop().animate({ marginLeft: 0 }, config.aniTime);
        }
    };

    //初始化窗口格局
    xxim.layinit = function () {
        if (!layim.easemob.noexpend) {
            var node = xxim.node;
            xxim.layimNode.attr({ state: 1 }).css({ right: config.right });
            node.xximon.addClass('xxim_off');
            node.layimFooter.addClass('xxim_expend').css({ marginLeft: config.right });
            node.xximHide.addClass('xxim_show');
        }
        ////主界面
        //try {
        //    if (!localStorage.layimState)
        //        localStorage.layimState = 1;
        //    if (localStorage.layimState === '1') {
        //        xxim.layimNode.attr({ state: 1 }).css({ right: config.right });
        //        node.xximon.addClass('xxim_off');
        //        node.layimFooter.addClass('xxim_expend').css({ marginLeft: config.right });
        //        node.xximHide.addClass('xxim_show');
        //    }
        //} catch (e) {
        //}
        xxim.tabs(2);
    };
    xxim.getobjecturl = function (file) {
        var url = null;
        if (window.createObjectURL != undefined) { // basic
            url = window.createObjectURL(file);
        } else if (window.URL != undefined) { // mozilla(firefox)
            url = window.URL.createObjectURL(file);
        } else if (window.webkitURL != undefined) { // webkit or chrome
            url = window.webkitURL.createObjectURL(file);
        }
        return url;
    };
    //聊天窗口
    xxim.popchat = function (param) {
        var node = xxim.node, log = {};

        log.success = function (layero) {
            xxim.chatbox = layero.find('#layim_chatbox');
            log.chatlist = xxim.chatbox.find('.layim_chatmore>ul');

            log.chatlist.html('<li data-id="' + param.id + '" type="' + param.type + '"  id="layim_user' + param.type + param.id + '"><span>' + param.name + '</span><em>×</em></li>')
            xxim.tabchat(param, xxim.chatbox);

            //最小化聊天窗
            xxim.chatbox.find('.layer_setmin').on('click', function () {
                layero.hide();
                node.layimMin.parent().removeClass('xxim_bottom_3');
                //node.layimMin.show();
                xxim.ischating = false;
            });

            //关闭窗口
            xxim.chatbox.find('.layim_close').on('click', function () {
                layer.close(layero.attr('times'));
                xxim.chatbox = null;
                config.chating = {};
                config.chatings = 0;
                xxim.ischating = false;
            });
            var addimage = xxim.chatbox.find('.layim_addimage');
            if (!Easemob.im.Helper.isCanUploadFileAsync) addimage.hide();
            //图片
            addimage.on('click', function () {
                if (!config.imageinput) {
                    config.imageinput = $('<input type="file" id="layim_imageinput" style="display:none;"/>');
                    $(document.body).append(config.imageinput);
                    config.imageinput.on('change', function () {
                        var fileObj = Easemob.im.Helper.getFileUrl('layim_imageinput');
                        if (!fileObj.url) return common.msg('请先选择图片！');
                        if (['jpg', 'gif', 'png', 'bmp'].indexOf(fileObj.filetype) < 0) return common.msg('不支持此图片类型' + fileObj.filetype + '！');
                        var layerindex = common.load();
                        var time = xxim.gettime();
                        var opt = {
                            type: 'chat',
                            fileInputId: 'layim_imageinput',
                            filename: fileObj.filename,
                            to: xxim.nowchat.id,
                            apiUrl: Easemob.im.config.apiURL,
                            onFileUploadError: function (error) {
                                layer.close(layerindex);
                                common.msg('发送图片失败！');
                            },
                            onFileUploadComplete: function (data) {
                                console.log(data);
                                layer.close(layerindex);
                                var file = document.getElementById('layim_imageinput');
                                var url = xxim.getobjecturl(file.files[0]);
                                xxim.showmsg({
                                    id: xxim.nowchat.id,
                                    type: xxim.nowchat.type,
                                    time: time,
                                    name: config.user.name,
                                    face: config.user.face,
                                    content: '<a href="' + data.uri + '/' + data.entities[0].uuid + '" target="_blank"><img src="' + url + '" /></a>'
                                }, 'me');
                            }, ext: { time: time }
                        };
                        layim.easemob.conn.sendPicture(opt);
                    });
                }
                config.imageinput.click();
            });
            //表情
            xxim.chatbox.find('.layim_addface').on('click', function () {
                //var offset = $(layero).offset();
                var color = 'transparent';
                if (navigator.appName == 'Microsoft Internet Explorer' && navigator.appVersion.split(';')[1].replace(/[ ]/g, '') == 'MSIE9.0') {
                    color = '#ddd';
                }
                var top = parseFloat(layero.css('top'));
                var left = parseFloat(layero.css('left'));
                if (!config.facehtml) {
                    var h = '<ul class="layim_face_list">';
                    var data = Easemob.im.EMOTIONS.map;
                    var path = Easemob.im.EMOTIONS.path;
                    for (var key in data) {
                        var src = path + data[key];
                        h += '<li class="layim_face_item" data-face="' + key + '" data-src="' + src + '"><img src="' + src + '"/></li>';
                    }
                    h += '</ul>';
                    config.facehtml = h;
                }
                layer.open({
                    type: 1,
                    title: false,
                    skin: 'layui-layerim-face',
                    closeBtn: false, //不显示关闭按钮
                    shift: 0,
                    move: false,
                    shade: [0.1, color],
                    shadeClose: true, //开启遮罩关闭
                    offset: [(top + 356) + 'px', left + 'px'],
                    area: ['432px', '135px'],
                    border: false,
                    content: config.facehtml,
                    success: function (facelayer) {
                        facelayer.on('click', '.layim_face_item', function () {
                            layer.close(facelayer.attr('times'));
                            var face = $(this).attr('data-face');
                            var time = xxim.gettime();
                            var src = $(this).attr('data-src');
                            layim.easemob.conn.sendTextMessage({ to: xxim.nowchat.id, msg: face, type: "chat", ext: { time: time } });
                            xxim.showmsg({
                                id: xxim.nowchat.id,
                                type: xxim.nowchat.type,
                                time: time,
                                name: config.user.name,
                                face: config.user.face,
                                content: '<img src="' + src + '" />'
                            }, 'me');
                        });
                    }
                });
            });
            //关闭某个聊天
            log.chatlist.on('mouseenter', 'li', function () {
                $(this).find('em').show();
            }).on('mouseleave', 'li', function () {
                $(this).find('em').hide();
            });
            log.chatlist.on('click', 'li em', function (e) {
                var parents = $(this).parent(), dataType = parents.attr('type');
                var dataId = parents.attr('data-id'), index = parents.index();
                var chatlist = log.chatlist.find('li'), indexs;

                config.stopMP(e);

                delete config.chating[dataType + dataId];
                config.chatings--;

                parents.remove();
                $('#layim_area' + dataType + dataId).remove();
                if (dataType === 'group') {
                    $('#layim_group' + dataType + dataId).remove();
                }

                if (parents.hasClass('layim_chatnow')) {
                    if (index === config.chatings) {
                        indexs = index - 1;
                    } else {
                        indexs = index + 1;
                    }
                    xxim.tabchat(config.chating[chatlist.eq(indexs).attr('type') + chatlist.eq(indexs).attr('data-id')]);
                }

                if (log.chatlist.find('li').length === 1) {
                    log.chatlist.parent().hide();
                }
            });

            //聊天选项卡
            log.chatlist.on('click', 'li', function () {
                var othis = $(this), dataType = othis.attr('type'), dataId = othis.attr('data-id');
                xxim.tabchat(config.chating[dataType + dataId]);
            });

            //发送热键切换
            log.sendType = $('#layim_sendtype'), log.sendTypes = log.sendType.find('span');
            $('#layim_enter').on('click', function (e) {
                config.stopMP(e);
                log.sendType.show();
            });
            log.sendTypes.on('click', function () {
                log.sendTypes.find('i').removeClass('fa-check');
                $(this).find('i').addClass('fa-check');
            });

            xxim.transmit();
        };

        log.html = '<div class="layim_chatbox" id="layim_chatbox">'
                + '<h6>'
                + '<span class="layim_move"></span>'
                + '    <a href="javascript:layim.easemob.xxim.showuserinfo(layim.easemob.xxim.nowchat.id);" class="layim_face" target="_blank"><img src="' + param.face + '" ></a>'
                + '    <a href="javascript:layim.easemob.xxim.showuserinfo(layim.easemob.xxim.nowchat.id);" class="layim_names" target="_blank">' + param.name + '</a>'
                + '    <span class="layim_rightbtn">'
                + '        <i class="layer_setmin">—</i>'
                + '        <i class="layim_close">&times;</i>'
                + '    </span>'
                + '</h6>'
                + '<div class="layim_chatmore" id="layim_chatmore">'
                + '    <ul class="layim_chatlist"></ul>'
                + '</div>'
                + '<div class="layim_groups" id="layim_groups"></div>'
                + '<div class="layim_chat">'
                + '    <div class="layim_chatarea" id="layim_chatarea">'
                + '        <ul class="layim_chatview layim_chatthis"  id="layim_area' + param.type + param.id + '"></ul>'
                + '    </div>'
                + '    <div class="layim_tool">'
                + '        <i class="layim_addface fa fa-meh-o" title="发送表情"></i>'
                + '        <i class="layim_addimage fa fa-picture-o" title="上传图片"></i>'
                //+ '        <a href="javascript:void(0);"><i class="layim_addfile fa fa-paperclip" title="上传附件"></i></a>'
                //+ '        <a href="javascript:void(0);" target="_blank" class="layim_seechatlog"><i class="fa fa-comment-o"></i>聊天记录</a>'
                + '    </div>'
                + '    <textarea class="layim_write" id="layim_write"></textarea>'
                + '    <div class="layim_send">'
                + '        <div class="layim_sendbtn" id="layim_sendbtn">发送<span class="layim_enter" id="layim_enter"><em class="layim_zero"></em></span></div>'
                + '        <div class="layim_sendtype" id="layim_sendtype">'
                + '            <span><i class="fa fa-check"></i>按Enter键发送</span>'
                + '            <span><i class="fa"></i>按Ctrl+Enter键发送</span>'
                + '        </div>'
                + '    </div>'
                + '</div>'
                + '</div>';
        if (config.chatings < 1) {
            layer.open({
                type: 1,
                border: [0],
                title: false,
                shade: false,
                skin: 'layui-layerim',
                area: ['620px', '492px'],
                move: '.layim_chatbox .layim_move',
                moveType: 1,
                closeBtn: false,
                zIndex: layer.zIndex,
                offset: [(($(window).height() - 493) / 2) + 'px', ''],
                content: log.html,
                success: function (layero) {
                    log.success(layero);
                }
            });
        } else {
            log.chatmore = xxim.chatbox.find('#layim_chatmore');
            log.chatarea = xxim.chatbox.find('#layim_chatarea');

            log.chatmore.show();

            log.chatmore.find('ul>li').removeClass('layim_chatnow');
            log.chatmore.find('ul').append('<li data-id="' + param.id + '" type="' + param.type + '" id="layim_user' + param.type + param.id + '" class="layim_chatnow"><span>' + param.name + '</span><em>×</em></li>');

            log.chatarea.find('.layim_chatview').removeClass('layim_chatthis');
            log.chatarea.append('<ul class="layim_chatview layim_chatthis" id="layim_area' + param.type + param.id + '"></ul>');

            xxim.tabchat(param);
        }

        //群组
        log.chatgroup = xxim.chatbox.find('#layim_groups');
        if (param.type === 'group') {
            log.chatgroup.find('ul').removeClass('layim_groupthis');
            log.chatgroup.append('<ul class="layim_groupthis" id="layim_group' + param.type + param.id + '"></ul>');
            xxim.getGroups(param);
        }
        //点击群员切换聊天窗
        log.chatgroup.on('click', 'ul>li', function () {
            xxim.popchatbox($(this));
        });
    };
    xxim.settop = function ($obj) {
        layer.zIndex++;
        $obj.css('z-index', layer.zIndex);
    };
    //显示用户信息
    xxim.showuserinfo = function (id) {
        var $infobox = $('#layim_chatbox_info_' + id);
        if ($infobox.length) return xxim.settop($infobox.parent().parent());
        var node = xxim.node, log = {};
        var param = $.extend({ from: id }, xxim.getinfo(id, function (id, info) {
            xxim.setuserinfo(id, info);
        }));
        log.success = function (layero) {
            xxim.setuserinfo(id, $.extend({ from: id }, xxim.getinfo(id)));
            layero.find('.layim_close').on('click', function () {
                layer.close(layero.attr('times'));
            });
            layero.find('.layim_chatinfo_chatuser').on('click', function () {
                xxim.inchat($.extend({ from: id }, xxim.getinfo(id)));
                if (xxim.chatbox) xxim.settop(xxim.chatbox.parent().parent());
            });
            layero.find('.layim_chatinfo_adduser').on('click', function () {
                layer.confirm('<input class="layui-layer-text" type="text" placeholder="验证信息" />', {
                    title: '添加好友',
                    btn: ['确定', '取消'],
                    zIndex: layer.zIndex,
                    skin: 'layui-layerim-dialog',
                    shade: false,
                    moveType: 1
                }, function (i, obj) {
                    var val = obj.find('.layui-layer-text').val();
                    layim.easemob.conn.subscribe({
                        to: id,
                        message: val
                    });
                    layer.msg('请求发送成功！', { zIndex: layer.zIndex });
                });
            });
            layero.find('.layim_chatinfo_deleteuser').on('click', function () {
                layer.confirm('是否删除好友？', {
                    btn: ['删除', '取消'],
                    zIndex: layer.zIndex,
                    skin: 'layui-layerim-dialog',
                    shade: false,
                    moveType: 1
                }, function () {
                    layim.easemob.conn.removeRoster({
                        to: id,
                        success: function () {
                            layer.msg('删除成功！', { zIndex: layer.zIndex });
                            layim.easemob.conn.unsubscribed({
                                to: id
                            });
                        }
                    });
                });
            });
        };
        log.html = '<div class="layim_chatbox layim_chatbox_info" id="layim_chatbox_info_' + id + '">'
                + '<h6>'
                + '<span class="layim_move"></span>'
                + '    <a href="javascript:void(0);" class="layim_face" target="_blank"><img class="layim_chatinfo_face" src="' + param.face + '" ></a>'
                + '    <div class="layim_rightinfos">'
                + '        <div><span class="layim_chatinfo_name">' + param.name + '</span><i class="fa fa-user layim_chatinfo_sex" style="color:#4CAE4C;line-height:1.33em;margin-left:5px;display:none;"></i></div>'
                + '        <div>用户号：<span class="layim_chatinfo_id">' + id + '</span></div>'
                + '        <div>积分：<span class="layim_chatinfo_intg">' + (param.intg || 0) + '</span></div>'
                + '    </div>'
                + '    <span class="layim_rightbtn">'
                + '        <i class="layim_close">&times;</i>'
                + '    </span>'
                + '</h6>'
                + '<div class="layim_chatinfo">'
                + '    <div>电话号码：<span class="layim_chatinfo_phone">' + (param.phone || '') + '</span></div>'
                + '    <div>地&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;区：<span class="layim_chatinfo_city">' + (param.province || '') + (param.city || '') + (param.district || '') + '</span></div>'
                + '</div>'
                + '<div class="layim_chatinfo_bottom">'
                + '    <div class="layim_chatinfo_btn layim_chatinfo_chatuser">发送消息</div>'
                + '    <div class="layim_chatinfo_btn layim_chatinfo_adduser">添加好友</div>'
                + '    <div class="layim_chatinfo_btn layim_chatinfo_deleteuser" style="display:none;">删除好友</div>'
                + '</div>'
                + '</div>';
        layer.open({
            type: 1,
            border: [0],
            title: false,
            shade: false,
            skin: 'layui-layerim',
            area: ['300px', '492px'],
            move: '.layim_chatbox .layim_move',
            zIndex: layer.zIndex,
            moveType: 1,
            closeBtn: false,
            offset: [(($(window).height() - 493) / 2) + 'px', ''],
            content: log.html,
            success: function (layero) {
                log.success(layero);
            }
        });
    };
    //得到好友信息
    xxim.getuserinfo = function (id) {
        var info = null;
        $(xxim.userlist).each(function (i, item) {
            if (item.subscription == 'both' || item.subscription == 'to') {
                if (item.name == id) info = item;
            }
        });
        return info;
    };
    //设置用户信息
    xxim.setuserinfo = function (id, info) {
        var $infobox = $('#layim_chatbox_info_' + id);
        if (!$infobox.length) return;
        $infobox.find('.layim_chatinfo_name').html(info.name);
        $infobox.find('.layim_chatinfo_face').attr('src', info.face);
        var $sex = $infobox.find('.layim_chatinfo_sex').hide();
        if (info.sex == 'M') $sex.css('color', '#4CAE4C').show();
        if (info.sex == 'F') $sex.css('color', '#FF808E').show();
        $infobox.find('.layim_chatinfo_intg').html(info.intg || 0);
        $infobox.find('.layim_chatinfo_phone').html(info.phone || '');
        $infobox.find('.layim_chatinfo_city').html((info.Province || '') + (info.city || '') + (info.district || ''));
        if (xxim.getuserinfo(id)) $infobox.find('.layim_chatinfo_deleteuser').show().siblings('.layim_chatinfo_adduser').hide();
        else $infobox.find('.layim_chatinfo_deleteuser').hide().siblings('.layim_chatinfo_adduser').show();
    };
    //缓存用户信息
    xxim.setinfo = function (info) {
        var chatuseritem = {
            name: info.MbrName,
            face: info.MbrPhoto,
            sex: info.Sex,
            intg: info.UseIntg,
            phone: info.Phone,
            province: info.Province,
            city: info.City,
            district: info.District
        };
        config.chatuser[info.MbrID] = chatuseritem;
        return chatuseritem;
    };
    //定位到某个聊天队列
    xxim.tabchat = function (param) {
        var node = xxim.node, log = {}, keys = param.type + param.id;
        xxim.nowchat = param;

        xxim.chatbox.find('#layim_user' + keys).addClass('layim_chatnow').siblings().removeClass('layim_chatnow');
        xxim.chatbox.find('#layim_area' + keys).addClass('layim_chatthis').siblings().removeClass('layim_chatthis');
        xxim.chatbox.find('#layim_group' + keys).addClass('layim_groupthis').siblings().removeClass('layim_groupthis');

        xxim.chatbox.find('.layim_face>img').attr('src', param.face).attr('class', 'layim_chatface_' + param.id);
        //xxim.chatbox.find('.layim_face, .layim_names').attr('href', param.href);
        xxim.chatbox.find('.layim_names').text(param.name).attr('class', 'layim_names layim_chatname_' + param.id);

        //xxim.chatbox.find('.layim_seechatlog').attr('href', config.chatlogurl + param.id);

        log.groups = xxim.chatbox.find('.layim_groups');
        if (param.type === 'group') {
            log.groups.show();
        } else {
            log.groups.hide();
        }
        $('#layim_write').focus();
        xxim.showusermsg(param.id, param.type);
        xxim.ischating = true;
        xxim.showcount(param.id);
    };
    xxim.getinfo = function (id, fn) {
        var info = config.chatuser[id];
        if (info) return info;
        else {
            if (id == 'admin') {
                info = { name: '物品在线助手', face: '/Files/Common/logo_80x80.png' };
                config.chatuser[id] = info;
                return info;
            }
            info = { name: id, face: '/Files/Shop/mbr-photo-default.png' };
            config.chatuser[id] = info;
            common.post('/Api/Shop/ShopMbrBLL/GetMbrChatInfo', { MbrID: id }, function (data) {
                var chatuseritem = xxim.setinfo(data.ResponseContent);
                if (xxim.node && xxim.node.list) {
                    xxim.node.list.find('.layim_chatname_' + id).html(chatuseritem.name);
                    xxim.node.list.find('.layim_chatface_' + id).attr('src', chatuseritem.face);
                }
                if (xxim.chatbox) {
                    xxim.chatbox.find('.layim_chatname_' + id).html(chatuseritem.name);
                    xxim.chatbox.find('.layim_chatface_' + id).attr('src', chatuseritem.face);
                }
                if (xxim.presencebox) {
                    xxim.presencebox.find('.layim_chatname_' + id).html(chatuseritem.name);
                    xxim.presencebox.find('.layim_chatface_' + id).attr('src', chatuseritem.face);
                }
                if (fn) fn(id, chatuseritem);
            }, null, { autologin: false, mask: false });
            return info
        }
    };
    xxim.showusermsg = function (id, type) {
        $(config.chatmsg[id]).each(function (i, item) {
            xxim.showmsg($.extend({
                time: item.time,
                name: item.from,
                face: config.user.face,
                content: item.data,
                type: type,
                id: id
            }, xxim.getinfo(id)));
            layim.easemob.conn.sendReceiptsMessage({ id: item.id });
        });
        config.chatmsg[id] = [];
    }
    xxim.showmsg = function (param, type) {
        var keys = param.type + param.id;
        var h = '<li class="' + (type === 'me' ? 'layim_chateme' : '') + '">'
            + '<div class="layim_chatuser">'
                + function () {
                    if (type === 'me') {
                        //return '<span class="layim_chattime">' + param.time + '</span>'
                        //       + '<span class="layim_chatname">' + param.name + '</span>'
                        //       + '<img src="' + param.face + '" >';
                        return '<img src="' + param.face + '" >';
                    } else {
                        //return '<img src="' + param.face + '" class="layim_chatface_' + param.id + '">'
                        //       + '<span class="layim_chatname layim_chatname_' + param.id + '">' + param.name + '</span>'
                        //       + '<span class="layim_chattime">' + param.time + '</span>';
                        return '<img src="' + param.face + '" class="layim_chatface_' + param.id + '">';
                    }
                }()
            + '</div>'
            + '<div class="layim_chatsay">' + param.content + '<em class="layim_zero"></em></div>'
        + '</li>';
        var imarea = xxim.chatbox.find('#layim_area' + keys);

        var time = param.time ? param.time.substring(0, 16) : '';
        if (imarea[0].lasttime != time) {
            imarea[0].lasttime = time;
            imarea.append('<div class="layim_chatarea_time"><span>' + time + '</span></div>');
        }

        imarea.append(h);
        imarea.scrollTop(imarea[0].scrollHeight);
    };
    //弹出聊天窗
    xxim.popchatbox = function (othis) {
        var node = xxim.node, dataId = othis.attr('data-id'), param = {
            id: dataId, //用户ID
            type: othis.attr('type'),
            name: othis.find('.xxim_onename').text(),  //用户名
            face: othis.find('.xxim_oneface').attr('src'),  //用户头像
            href: 'profile.html?user=' + dataId //用户主页
        }, key = param.type + dataId;
        if (!config.chating[key]) {
            xxim.popchat(param);
            config.chatings++;
        } else {
            xxim.tabchat(param);
        }
        config.chating[key] = param;

        var chatbox = $('#layim_chatbox');
        if (chatbox[0]) {
            //node.layimMin.hide();
            node.layimMin.parent().addClass('xxim_bottom_3');
            chatbox.parents('.layui-layerim').show();
        }

    };
    xxim.setpresence = function (info) {
        if (!xxim.presencebox) return;
        var hid = 'layim_presencebox_item_' + info.from;
        var hitem = xxim.presencebox.find('#' + hid);
        if (hitem.length) hitem.remove();
        var param = $.extend({ from: info.from }, xxim.getinfo(info.from));
        var h = '<div class="layim_presencebox_item" id="' + hid + '"><div class="layim_presencebox_item_left" onclick="layim.easemob.xxim.showuserinfo(\'' + param.from + '\')"><img class="layim_chatface_' + param.from + '" src="' + param.face + '"><div class="layim_chatname_' + param.from + '">' + param.name + '</div><div>' + (info.status || '申请加为好友') + '</div></div><div class="layim_presencebox_item_right"><div class="layim_presencebox_accept_btn" onclick="layim.easemob.xxim.presenceaccept(\'' + param.from + '\')">接受</div><div class="layim_presencebox_reject_btn" onclick="layim.easemob.xxim.presencereject(\'' + param.from + '\')">拒绝</div></div></div>';
        xxim.presencebox.find('.layim_presencebox_content').append(h);
    };
    xxim.presenceaccept = function (id) {
        $('#layim_presencebox_item_' + id + ' .layim_presencebox_item_right').html('已接受');
        layim.easemob.conn.subscribed({
            to: id,
            message: "[resp:true]"
        });
        layim.easemob.conn.subscribe({
            to: id,
            message: "[resp:true]"
        });
    };
    xxim.presencereject = function (id) {
        $('#layim_presencebox_item_' + id + ' .layim_presencebox_item_right').html('已拒绝');
        layim.easemob.conn.unsubscribed({
            to: id
        });
    };
    //弹出新的联系人
    xxim.poppresencebox = function () {
        if (xxim.presencebox) return xxim.settop(xxim.presencebox.parent().parent());
        var log = {};
        log.success = function (layero) {
            xxim.presencebox = layero.find('#layim_presencebox');
            xxim.presencebox.find('.layim_presencebox_search_keyword').on('keyup', function (e) {
                if (e.which == 13) xxim.searchuser();
            });
            $(config.presences).each(function (i, item) {
                xxim.setpresence(item);
            });
            config.presences = [];
            xxim.showcount();
        };
        log.html = '<div class="layim_presencebox" id="layim_presencebox">'
                + '    <div class="layim_presencebox_search">'
                + '        <input class="layui-layer-text layim_presencebox_search_keyword" type="text" placeholder="昵称/手机号/邮箱" />'
                + '        <div class="layim_presencebox_search_btn" onclick="layim.easemob.xxim.searchuser()">查找</div>'
                + '    </div>'
                + '    <div class="layim_presencebox_content">'
                + '    </div>'
                + '</div>';
        layer.open({
            type: 1,
            title: '新的联系人',
            shade: false,
            moveType: 1,
            skin: 'layui-layerim',
            area: ['600px', '400px'],
            zIndex: layer.zIndex,
            offset: [(($(window).height() - 400) / 2) + 'px', ''],
            content: log.html,
            cancel: function (index) {
                xxim.presencebox = null;
            },
            success: function (layero) {
                log.success(layero);
            }
        });
    };
    //请求群员
    xxim.getGroups = function (param) {
        var keys = param.type + param.id, str = '',
        groupss = xxim.chatbox.find('#layim_group' + keys);
        groupss.addClass('loading');
        config.json(config.api.groups, {}, function (datas) {
            if (datas.status === 1) {
                var ii = 0, lens = datas.data.length;
                if (lens > 0) {
                    for (; ii < lens; ii++) {
                        str += '<li data-id="' + datas.data[ii].id + '" type="one"><img src="' + datas.data[ii].face + '" class="xxim_oneface"><span class="xxim_onename">' + datas.data[ii].name + '</span></li>';
                    }
                } else {
                    str = '<li class="layim_errors">没有群员</li>';
                }

            } else {
                str = '<li class="layim_errors">' + datas.msg + '</li>';
            }
            groupss.removeClass('loading');
            groupss.html(str);
        }, function () {
            groupss.removeClass('loading');
            groupss.html('<li class="layim_errors">请求异常</li>');
        });
    };

    //消息传输
    xxim.transmit = function () {
        var node = xxim.node, log = {};
        node.sendbtn = $('#layim_sendbtn');
        node.imwrite = $('#layim_write');
        //发送
        log.send = function () {
            var data = {
                content: node.imwrite.val(),
                id: xxim.nowchat.id,
                sign_key: '', //密匙
                _: +new Date
            };

            if (data.content.replace(/\s/g, '') === '') {
                layer.tips('说点啥呗！', '#layim_write', 2);
                node.imwrite.focus();
            } else {
                var time = xxim.gettime();
                layim.easemob.conn.sendTextMessage({ to: data.id, msg: data.content, type: "chat", ext: { time: time } });
                xxim.showmsg({
                    id: data.id,
                    type: xxim.nowchat.type,
                    time: time,
                    name: config.user.name,
                    face: config.user.face,
                    content: data.content
                }, 'me');
                node.imwrite.val('').focus();
            }
        };
        node.sendbtn.on('click', log.send);
        node.imwrite.keyup(function (e) {
            if (e.keyCode === 13) {
                log.send();
            }
        });
    };

    //事件
    xxim.event = function () {
        var node = xxim.node;
        //主界面tab
        node.tabs.eq(0).addClass('xxim_tabnow');
        node.tabs.on('click', function () {
            var othis = $(this), index = othis.index();
            xxim.tabs(index);
        });
        //列表展收
        node.list.on('click', 'h5', function () {
            var othis = $(this), chat = othis.siblings('.xxim_chatlist'), parentss = othis.find("i");
            if (parentss.hasClass('fa-caret-down')) {
                chat.hide();
                parentss.attr('class', 'fa fa-caret-right');
            } else {
                chat.show();
                parentss.attr('class', 'fa fa-caret-down');
            }
        });
        node.online.on('click', function (e) {
            if (node.layimMin.parent().hasClass('xxim_bottom_offline')) return;
            xxim.tabs(2);
            if (xxim.layimNode.attr('state') == '1') xxim.expend();
        });
        node.xximon.on('click', xxim.expend);
        node.xximHide.on('click', xxim.expend);
        node.rconnect.on('click', function () {
            xxim.rconnect();
        });
        //搜索
        node.xximSearch.keyup(function () {
            var val = $(this).val().replace(/\s/g, '');
            if (val !== '') {
                node.searchMian.show();
                node.closeSearch.show();
                //此处的搜索ajax参考xxim.getDates
                node.list.eq(3).html('<li class="xxim_errormsg">没有符合条件的结果</li>');
            } else {
                node.searchMian.hide();
                node.closeSearch.hide();
            }
        });
        node.closeSearch.on('click', function () {
            $(this).hide();
            node.searchMian.hide();
            node.xximSearch.val('').focus();
        });
        //弹出聊天窗
        config.chatings = 0;
        node.list.on('click', '.xxim_childnode', function () {
            var othis = $(this);
            xxim.popchatbox(othis);
        });
        //弹出新的联系人
        node.list.on('click', '.xxim_addnode', function () {
            xxim.poppresencebox();
        });
        //点击最小化栏
        node.layimMin.on('click', function () {
            //$(this).hide();
            $(this).parent().addClass('xxim_bottom_3');
            $('#layim_chatbox').parents('.layui-layerim').show();
        });
        //document事件
        dom[1].on('click', function () {
            node.setonline.hide();
            $('#layim_sendtype').hide();
        });
    };
    xxim.gettime = function () {
        //var date = new Date();
        //var time = date.getHours() + ":" + date.getMinutes();
        //return time;
        return new Date().ToFormat('yyyy/MM/dd hh:mm:ss');
        //return new Date().toString();
    };
    xxim.gochat = function () {
        var message = xxim.forchat;
        if (!message) return;
        $.extend(message, { time: xxim.gettime() });
        var msg = config.chatmsg[message.from];
        if (!msg) {
            msg = config.chatmsg[message.from] = [];
            var h = '<li data-id="' + message.from + '" class="xxim_childnode xxim_childnode_' + message.from + '" type="one"><img src="' + message.face + '" class="xxim_oneface layim_chatface_' + message.from + '"><span class="xxim_onename layim_chatname_' + message.from + '">' + message.name + '</span><em class="xxim_time">' + (message.time ? message.time.substring(5, 10) : '') + '</em><i class="xxim_chatcount xxim_chatcount_' + message.from + '">1</i></li>';
            xxim.node.list.eq(2).find('.xxim_chatlist').prepend(h);
        }
        var childnodes = xxim.node.list.find('.xxim_childnode_' + message.from);
        if (childnodes.length) xxim.popchatbox(childnodes.eq(0));
        xxim.forchat = null;
    }
    xxim.inchat = function (message) {
        xxim.forchat = message;
        if (layim.easemob.conn.isOpened()) xxim.gochat();
        else xxim.rconnect();
    };
    xxim.showuser = function (list) {
        xxim.userlist = list;
        var h = '';
        h += '<li class="xxim_addnode" id="xxim_addnode"><span class="xxim_addnode_face"><i class="fa fa-user"></i><i class="fa fa-plus-circle"></i></span><span class="">新的联系人</span><i class="xxim_chatcount" style="' + (config.presences.length ? 'display:block;' : '') + '">' + config.presences.length + '</i></li>';
        $(list).each(function (i, item) {
            if (item.subscription == 'both' || item.subscription == 'to') {
                var message = $.extend({ from: item.name }, xxim.getinfo(item.name));
                h += '<li data-id="' + message.from + '" class="xxim_childnode xxim_childnode_' + message.from + '" type="one"><img src="' + message.face + '" class="xxim_oneface layim_chatface_' + message.from + '"><span class="xxim_onename layim_chatname_' + message.from + '">' + message.name + '</span><i class="xxim_chatcount xxim_chatcount_' + message.from + '"></i></li>';
            }
        });
        xxim.node.list.eq(0).find('.xxim_chatlist').html(h);
    };
    xxim.searchuser = function () {
        if (!xxim.presencebox) return;
        var keyword = xxim.presencebox.find('.layim_presencebox_search_keyword').val();
        if (!keyword) return;
        common.post('/Api/Shop/ShopMbrBLL/GetMbrChatInfo', { KeyWord: keyword }, function (data) {
            if (!data.ResponseContent) return layer.msg('用户不存在！', { zIndex: layer.zIndex });;
            xxim.setinfo(data.ResponseContent);
            xxim.showuserinfo(data.ResponseContent.MbrID);
        });
    };
    xxim.showpresence = function (e) {
        if (e.type === 'subscribe') {
            //若e.status中含有[resp:true],则表示为对方同意好友后反向添加自己为好友的消息，demo中发现此类消息，默认同意操作，完成双方互为好友；如果不含有[resp:true]，则表示为正常的对方请求添加自己为好友的申请消息。
            if (e.status) {
                if (e.status.indexOf('resp:true') > -1) {
                    layim.easemob.conn.subscribed({
                        to: e.from,
                        message: "[resp:true]"
                    });
                    return;
                }
            }
            if (!xxim.presencebox) {
                config.presences.push(e);
                xxim.showcount();
            }
            else xxim.setpresence(e);
        }

        //(发送者允许接收者接收他们的出席信息)，即别人同意你加他为好友
        if (e.type === 'subscribed') {

        }

        //unsubscribe（发送者取消订阅另一个实体的出席信息）,即删除现有好友
        //unsubscribed（订阅者的请求被拒绝或以前的订阅被取消），即对方单向的删除了好友
        if (e.type === 'unsubscribe' || e.type === 'unsubscribed') {
            layim.easemob.conn.removeRoster({
                to: e.from,
                groups: ['default'],
                success: function () {
                    layim.easemob.conn.unsubscribed({
                        to: e.from
                    });
                }
            });
        }
    };
    xxim.showhistory = function (message) {
        $.extend(message, xxim.getinfo(message.from));
        var msg = config.chatmsg[message.from];
        if (!msg) {
            msg = config.chatmsg[message.from] = [message];
            var h = '<li data-id="' + message.from + '" class="xxim_childnode xxim_childnode_' + message.from + '" type="one"><img src="' + message.face + '" class="xxim_oneface layim_chatface_' + message.from + '"><span class="xxim_onename layim_chatname_' + message.from + '">' + message.name + '</span><em class="xxim_time">' + (message.time ? message.time.substring(5, 10) : '') + '</em><i class="xxim_chatcount xxim_chatcount_' + message.from + '"></i></li>';
            xxim.node.list.eq(2).find('.xxim_chatlist').prepend(h);
        }
        else {
            msg.push(message);
        }
        if (xxim.ischating && xxim.nowchat && xxim.nowchat.id == message.from) xxim.showusermsg(message.from, 'one');
        xxim.showcount(message.from);
    };
    xxim.showcount = function (id) {
        if (id) {
            var msg = config.chatmsg[id];
            if (!msg) return;
            var $chatcount = xxim.node.list.find('.xxim_chatcount_' + id);
            if (msg.length) $chatcount.html(msg.length).show();
            else $chatcount.hide().html(msg.length);
        }
        var pcount = config.presences ? config.presences.length : 0;
        if (pcount) xxim.node.list.find('#xxim_addnode .xxim_chatcount').html(pcount).show();
        else xxim.node.list.find('#xxim_addnode .xxim_chatcount').html(pcount).hide();
        var count = pcount;
        for (var i in config.chatmsg) {
            count += config.chatmsg[i].length;
        }
        var $count = xxim.node.online.children('.xxim_chatcount');
        if (layim.easemob.showtip) layim.easemob.showtip(count);
        else {
            if (count) $count.html(count);
            else $count.html('');
        }
    };
    //渲染骨架
    xxim.view = (function () {
        var xximNode = xxim.layimNode = $('<div id="xximmm" class="xxim_main">'
                + '<div class="xxim_top" id="xxim_top">'
                + '  <div class="xxim_search"><i class="fa fa-search"></i><input id="xxim_searchkey" /><span id="xxim_closesearch">×</span></div>'
                + '  <div class="xxim_tabs" id="xxim_tabs"><span class="xxim_tabfriend" title="好友"><i class="fa fa-user"></i></span><span class="xxim_tabgroup" title="群组"><i class="fa fa-users"></i></span><span class="xxim_latechat"  title="最近聊天"><i class="fa fa-clock-o"></i></span></div>'
                + '  <ul class="xxim_list loading"><li class="xxim_liston"><ul class="xxim_chatlist"></ul></li></ul>'
                + '  <ul class="xxim_list loading"></ul>'
                + '  <ul class="xxim_list loading"><li class="xxim_liston"><ul class="xxim_chatlist"></ul></li></ul>'
                + '  <ul class="xxim_list xxim_searchmain" id="xxim_searchmain"></ul>'
                + '</div>'
                + '<ul class="xxim_bottom xxim_bottom_3 xxim_bottom_offline" id="xxim_bottom">'
                + '<li class="xxim_online xxim_offline" id="xxim_online" title="状态">'
                    + '<i class="xxim_chatcount"></i><span id="xxim_onlinetex">离线</span>'
                + '</li>'
                + '<li class="xxim_mymsg" id="xxim_mymsg" title="对话窗口"><i class="fa fa-comments"></i></li>'
                + '<li class="xxim_seter" id="xxim_seter" title="设置">'
                    + '<i class="fa fa-gear"></i>'
                    + '<div>'

                    + '</div>'
                + '</li>'
                + '<li class="xxim_rconnect loading" id="xxim_rconnect"></li>'
                + '<li class="xxim_hide" id="xxim_hide" title="显示/隐藏面板"><i class="fa fa-exchange"></i></li>'
            + '</ul>'
        + '</div>');
        dom[3].append(xximNode);

        xxim.renode();
        xxim.event();
        xxim.layinit();
    }());
}