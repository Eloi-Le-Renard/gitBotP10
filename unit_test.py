##########################################
############## email_prompt.py ##############
##########################################
from botbuilder.dialogs.prompts import Prompt, PromptOptions,PromptRecognizerResult
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import ActivityTypes
from recognizers_text import Culture, ModelResult,StringUtility
from recognizers_sequence import SequenceRecognizer

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
        mode = recong.get_url_model()
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
        step2 = await step1.send('Book a flight to Paris.')
        await step2.assert_reply("Paris.")
        
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