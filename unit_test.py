##########################################
############## email_prompt.py ##############
##########################################
from botbuilder.dialogs.prompts import Prompt, PromptOptions,PromptRecognizerResult
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import ActivityTypes
from recognizers_text import Culture, ModelResult,StringUtility
from recognizers_sequence import SequenceRecognizer
# modif lib
#from recognizers_text.model import Model, ModelResult



class Constants:
    IP_REGEX_IPV4: str = "ipv4"
    IP_REGEX_IPV6: str = "ipv6"
    IPV6_ELLIPSIS: str = "::"
    PHONE_NUMBER_REGEX_GENERAL: str = "GeneralPhoneNumber"
    PHONE_NUMBER_REGEX_BR: str = "BRPhoneNumber"
    PHONE_NUMBER_REGEX_UK: str = "UKPhoneNumber"
    PHONE_NUMBER_REGEX_DE: str = "DEPhoneNumber"
    PHONE_NUMBER_REGEX_US: str = "USPhoneNumber"
    PHONE_NUMBER_REGEX_CN: str = "CNPhoneNumber"
    PHONE_NUMBER_REGEX_DK: str = "DKPhoneNumber"
    PHONE_NUMBER_REGEX_IT: str = "ITPhoneNumber"
    PHONE_NUMBER_REGEX_NL: str = "NLPhoneNumber"
    PHONE_NUMBER_REGEX_SPECIAL: str = "SpecialPhoneNumber"
    MENTION_REGEX = "Mention"
    HASHTAG_REGEX = "Hashtag"
    EMAIL_REGEX = "Email"
    URL_REGEX = "Url"
    GUID_REGEX = "Guid"
    SYS_PHONE_NUMBER = "builtin.phonenumber"
    SYS_IP = "builtin.ip"
    SYS_MENTION = "builtin.mention"
    SYS_HASHTAG = "builtin.hashtag"
    SYS_EMAIL = "builtin.email"
    #SYS_AIRPORT = "builtin.airport"
    SYS_URL = "builtin.url"
    SYS_GUID = "builtin.guid"
    MODEL_PHONE_NUMBER = "phonenumber"
    MODEL_IP = "ip"
    MODEL_MENTION = "mention"
    MODEL_HASHTAG = "hashtag"
    MODEL_EMAIL = "email"
    #MODEL_EMAIL = "airport"
    MODEL_URL = "url"
    MODEL_GUID = "guid"
    
class AirportModel(AbstractSequenceModel):
    @property
    def model_type_name(self) -> str:
        return "email"
        #return Constants.MODEL_AIRPORT
        

class SequenceRecognizer(Recognizer[SequenceOptions]):
    def __init__(self, target_culture: str = None, options: SequenceOptions = SequenceOptions.NONE,
                 lazy_initialization: bool = True):
        if options < SequenceOptions.NONE or options > SequenceOptions.NONE:
            raise ValueError()
        super().__init__(target_culture, options, lazy_initialization)

    def initialize_configuration(self):
        self.register_model('PhoneNumberModel', Culture.English,
                            lambda options: PhoneNumberModel(PhoneNumberParser(),
                                                             BasePhoneNumberExtractor(EnglishPhoneNumberExtractorConfiguration())))

        self.register_model('PhoneNumberModel', Culture.Chinese,
                            lambda options: PhoneNumberModel(PhoneNumberParser(),
                                                             BasePhoneNumberExtractor(ChinesePhoneNumberExtractorConfiguration())))

        self.register_model('PhoneNumberModel', Culture.Portuguese,
                            lambda options: PhoneNumberModel(PhoneNumberParser(),
                                                             BasePhoneNumberExtractor(PortuguesePhoneNumberExtractorConfiguration())))

        self.register_model('EmailModel', Culture.English,
                            lambda options: EmailModel(EmailParser(), EnglishEmailExtractor()))

        self.register_model('IpAddressModel', Culture.English,
                            lambda options: IpAddressModel(IpParser(),
                                                           BaseIpExtractor(EnglishIpExtractorConfiguration(options))))

        self.register_model('IpAddressModel', Culture.Chinese,
                            lambda options: IpAddressModel(IpParser(),
                                                           BaseIpExtractor(ChineseIpExtractorConfiguration(options))))

        self.register_model('MentionModel', Culture.English,
                            lambda options: MentionModel(MentionParser(), EnglishMentionExtractor()))

        self.register_model('HashtagModel', Culture.English,
                            lambda options: HashtagModel(HashtagParser(), EnglishHashtagExtractor()))

        self.register_model('URLModel', Culture.English,
                            lambda options: URLModel(
                                URLParser(), BaseURLExtractor(EnglishURLExtractorConfiguration(options)))
                            )

        self.register_model('URLModel', Culture.Chinese,
                            lambda options: URLModel(
                                URLParser(), BaseURLExtractor(ChineseURLExtractorConfiguration(options)))
                            )

        self.register_model('GUIDModel', Culture.English,
                            lambda options: GUIDModel(GUIDParser(), EnglishGUIDExtractor()))

    def get_phone_number_model(self, culture: str = None, fallback_to_default_culture: bool = True) -> Model:
        if culture and (culture.lower().startswith("zh-") or culture.lower().startswith("ja-")):
            return self.get_model('PhoneNumberModel', Culture.Chinese, fallback_to_default_culture)
        return self.get_model('PhoneNumberModel', culture, fallback_to_default_culture)

    def get_ip_address_model(self, culture: str = None, fallback_to_default_culture: bool = True) -> Model:
        if culture and (culture.lower().startswith("zh-") or culture.lower().startswith("ja-")):
            return self.get_model('IpAddressModel', Culture.Chinese, fallback_to_default_culture)
        return self.get_model('IpAddressModel', culture, fallback_to_default_culture)

    def get_mention_model(self, culture: str = None, fallback_to_default_culture: bool = True) -> Model:
        return self.get_model('MentionModel', culture, fallback_to_default_culture)

    def get_hashtag_model(self, culture: str = None, fallback_to_default_culture: bool = True) -> Model:
        return self.get_model('HashtagModel', culture, fallback_to_default_culture)

    def get_url_model(self, culture: str = None, fallback_to_default_culture: bool = True) -> Model:
        if culture and (culture.lower().startswith("zh-") or culture.lower().startswith("ja-")):
            return self.get_model('URLModel', Culture.Chinese, fallback_to_default_culture)
        return self.get_model('URLModel', culture, fallback_to_default_culture)

    def get_guid_model(self, culture: str = None, fallback_to_default_culture: bool = True) -> Model:
        return self.get_model('GUIDModel', culture, fallback_to_default_culture)

    def get_email_model(self, culture: str = None, fallback_to_default_culture: bool = True) -> Model:
        return self.get_model('EmailModel', culture, fallback_to_default_culture)
    
    def get_airport_model(self, culture: str = None, fallback_to_default_culture: bool = True) -> Model:
        return self.get_model('AirportModel', culture, fallback_to_default_culture)


# modif lib

from typing import Callable, Dict
import enum

class EmailPrompt (Prompt):
    def __init__(self, 
        dialog_id,
        validator : object = None,
        defaultLocale = None):
     super().__init__(dialog_id, validator=validator)
     
     if defaultLocale is None:
        defaultLocale = Culture.English

     self._defaultLocale = defaultLocale

    async def on_prompt(
        self, 
        turn_context: TurnContext, 
        state: Dict[str, object], 
        options: PromptOptions, 
        is_retry: bool, 
    ):
        if not turn_context:
            raise TypeError("turn_context Can’t  be none")
        if not options:
            raise TypeError("options Can’t  be none")

        if is_retry and options.retry_prompt is not None:
            await turn_context.send_activity(options.retry_prompt)
        else:
            if options.prompt is not None:
                await turn_context.send_activity(options.prompt)    

    async def on_recognize(self,
        turn_context: TurnContext, 
        state: Dict[str, object], 
        options: PromptOptions, 
    ) -> PromptRecognizerResult:  
        if not turn_context:
            raise TypeError("turn_context cannt be none")

        if turn_context.activity.type == ActivityTypes.message:
            usertext = turn_context.activity.text
        
        turn_context.activity.locale = self._defaultLocale

        recong = SequenceRecognizer(turn_context.activity.locale)
        # TODO
        #mode = recong.get_email_model()
        mode = recong.get_airport_model()
        mode_result = mode.parse(usertext)

        prompt_result = PromptRecognizerResult()

        if len(mode_result) > 0 and len(mode_result[0].resolution) > 0:
            prompt_result.value = mode_result[0].resolution["value"]
            prompt_result.succeeded = True

        return prompt_result
    
    


##########################################
############## custom_test.py ##############
##########################################
import sys
import pathlib
import pytest
import aiounittest
import asyncio

from botbuilder.dialogs.prompts import (
    AttachmentPrompt, 
    PromptOptions, 
    PromptValidatorContext, 
)

from botbuilder.core import (
    TurnContext, 
    ConversationState, 
    MemoryStorage, 
    MessageFactory, 
)
from botbuilder.schema import Activity, ActivityTypes, Attachment
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.core.adapters import TestAdapter

#Q = "What is your email address?"
Q = "To what city would you like to travel?"#"niktamere2"#"BBBBBB What can I help you with today?"
#userInput = "My email id is r.vinoth@live.com"
#botAnswer = "r.vinoth@live.com"
userInput = "book a flight from paris to berlin for the 12/12/12 until 12/12/22 for $1200 max"
botAnswer = "AAAAAA To what city would you like to travel?"


class EmailPromptTest(aiounittest.AsyncTestCase):
    async def test_email_prompt(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = Q
                        )
                    )
                await dialog_context.prompt("cityprompt", options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(reply)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        dialogs.add(EmailPrompt("cityprompt"))

        step1 = await adapter.test('Hello', Q)
        #step2 = await step1.send('My email id is r.vinoth@live.com')
        step2 = await step1.send('Book a flight to Paris ')
        #assert step1 == step2
        await step2.assert_reply("Paris")
        
        #step1 = await adapter.test('Hello', 'What can I help you with today?')
        #step2 = await step1.test(userInput, Q)
        #step3 = await step2.send("I want to go to Paris")
        #assert 
        #await step3.assert_reply("Paris")
        
        #step1 = await adapter.test('Hello', Q)
        #step1 = await adapter.test('niktameree',Q)
        #step2 = await step1.send(userInput)
        #await step2.assert_reply(Q)

        # + dialog ?
        #step3 = await step2.send(userInput)
        #await step3.assert_reply(botAnswer)
        
        
def test1():
    assert 1 == 1