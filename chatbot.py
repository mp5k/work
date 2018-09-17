# coding: utf-8

from watson_developer_cloud import AssistantV1

class Chatbot:
    def __init__(self, version, username, password, workspace_id, debug = False) :
        self.watson_assistant = AssistantV1(
            version=version,
            username=username,
            password=password)
        self.workspace_id = workspace_id
        self.context_val = {}
        self.debug = debug

    def send(self, message, confidence):
        '''
        send message

        Parameters
        ----------
        message : str
            message
        confidence : float
            intent confidence
        '''
        response = {}
        if message == 'head' :
            #headの場合最初のメッセージ
            self.context_val = {}
            response = self.watson_assistant.message(
                workspace_id=self.workspace_id,
                context=self.context_val,
                alternate_intents=True
                )
        else :
            response = self.watson_assistant.message(
                workspace_id= self.workspace_id,
                input={
                    'text': str(message)
                },
                context=self.context_val,
                alternate_intents=True
                )

        self.context_val = response['context']
        if self.debug :
            print('Assistant Response -----------')
            print(response)
            print('------------------------------')
        msg = response['output']['text'][0]
        dic = {'intents' : [],'responses' : []}
        #候補のIntentsを抽出
        dic['intents'].extend([x['intent'] for x in response['intents'] if x['confidence'] >= confidence])
        #テキストメッセージを表示
        for text in response['output']['text'] :
            if response['output']['nodes_visited'] != None :
                text = "<div class='intent'>" + response['output']['nodes_visited'][0] + "</div>" + text
            dic['responses'].append({'ui' : 'message', 'params' : {'content' : text}})
        hasinput = False #入力方法が指定されてるフラグ
        #他のresponseを判定
        for other in response['output']['generic'] :
            if other['response_type'] == 'option' :
                #ボタン
                if other['title'] == 'button' :
                    hasinput = True
                    buttons = []
                    #optionからボタン作成
                    for btn in other['options'] :
                        buttons.append({'text' : btn['value']['input']['text'], 'label' : btn['label']})
                    dic['responses'].append({'ui': 'button', 'params' : {'action' : buttons}})
        #入力方法が指定されていない場合は、通常のインプットを出力する
        if hasinput == False :
            dic['responses'].append({'ui': 'text', 'params' : {'action' : {'placeholder':'入力してください'}}})
        if self.debug :
            print('Server Response --------------')
            print(dic)
            print('------------------------------')
        return dic


