/* BotUI */
(function () {
    var botui = new BotUI('hello-world');

    sendMessage('head');

	//メッセージを送信する
	function sendMessage(callMsg) {
		//画像初期化
		$(".botui-message .botui-message-content:not(.human)").css({ backgroundImage: 'none' });
		botui.message.bot({
			loading: true
		}).then(function (index) {
		//同期ajaxにより返答取得
		var res = sendSync(callMsg);
		botui.message.remove(index, {
			loading: false
		});
		var jsonres = JSON.parse(res);
		var msgs = jsonres['responses'];
		parseReponses(msgs).then(function() {
			//JQueryで最後のメッセージに候補のリストを追加する。
			var content = $('#hello-world .botui-message-content.text').last();
			var candidacys = jsonres['intents'];
			if(candidacys && candidacys.length > 0) {
				//画像切替
				$(".botui-message:last-child .botui-message-content:not(.human)").css({ backgroundImage: 'url("/static/images/piyopiyo.gif")' });
				content.html(content.html() + '<ul class="candidacy"></ul>');
				var ul = content.children('.candidacy');
				$.each(candidacys, function(index,value) {
						ul.append('<li>' + value + '</li>');
					});
				//イベント設定
				$('.candidacy li').off('.candidacy');
				$('.candidacy li').on('click.candidacy',function(){
					var text = $(this).text();
					botui.action.hide();
					botui.message.human(text);
					sendMessage(text);
				});
			} else {
				//候補がゼロ：解釈できなかった。
				//画像切替
				$(".botui-message:last-child .botui-message-content:not(.human)").css({ backgroundImage: 'url("/static/images/wakewakaran.png")' });
			}
			});
		});
	}

    //再帰的にメッセージを組み立てる
    function parseReponses(obj) {
        if (obj.length == 1) {
            return parseUi(obj[0]);
        } else if (obj.length > 1) {
            return parseUi(obj[0]).then(parseReponses(obj.slice(1)));
        }
    }

    //JSONからBotUiへ命令する
    //基本的に最後はユーザーのレスポンスが必要なもの
    function parseUi(response) {
        switch (response['ui']) {
            case 'message' :
                return botui.message.add(response['params']);
            case 'button' :
                return botui.action.button(response['params'])
                        .then(function (res) {
                          sendMessage(res.label);
                        });
            case 'text' :
                return botui.action.text(response['params'])
                        .then(function (res) {
                          sendMessage(res.value);
                        });
        }
    }
}
)();
