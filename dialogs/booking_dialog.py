# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
# TODO: replace the all-zero GUID with your instrumentation key.
# 858507df-0f27-48e8-b598-4741bd6836e4
logger.addHandler(AzureLogHandler(
    #connection_string='InstrumentationKey='+CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY)
    connection_string='InstrumentationKey=f0163947-d8c0-436b-8636-36cee15e8872')
)


"""Flight booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.travel_date_step,
                self.return_date_step,
                self.budget_step,
                self.confirmation_step,
                self.conclusion_step,                
                self.final_step,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        self.add_dialog(
            DateResolverDialog(DateResolverDialog.__name__, self.telemetry_client)
        )
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for destination."""
        booking_details = step_context.options
        if booking_details.destination is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("To what city would you like to travel?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        

        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result
        if booking_details.origin is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("From what city will you be travelling?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.origin)

    async def travel_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.origin = step_context.result
        if not booking_details.travel_date or self.is_ambiguous(
            booking_details.travel_date
        ):
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, booking_details.travel_date
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.travel_date)

    async def return_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for return date.
        This will use the DATE_RESOLVER_DIALOG."""
        # marche pas
        #step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=MessageFactory.text("test ?")))
        
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.travel_date = step_context.result
        if booking_details.return_date is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("return date ?")
                    #prompt=MessageFactory.text(f"return date ? {booking_details}")
                ),
            )
        
        if not booking_details.return_date or self.is_ambiguous(
            booking_details.return_date
        ):
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, booking_details.return_date
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.return_date)

    async def budget_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.return_date = step_context.result
        
        if booking_details.budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("budget ?")
                ),
            )
        return await step_context.next(booking_details.budget)
    
    
    async def confirmation_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        booking_details = step_context.options
        booking_details.budget = step_context.result
        
        msg = (
            f"Please confirm, I have you traveling to: { booking_details.destination }"
            f" from: { booking_details.origin } on: { booking_details.travel_date}."
            f" return: { booking_details.return_date } for max: { booking_details.budget}."
         #   f" OBJECT: { booking_details } "
        )
        return await step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=MessageFactory.text(
            msg)))

   # TODO
    async def conclusion_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        booking_details = step_context.options
        booking_details.validate = step_context.result
        
        if booking_details.validate == "yes":
            msg = "you say YES, i confirmed your flight"
        else:
            msg = "you say NO, let's restart"
            #logger.warning("user say no", properties={'test': {'key_1': 'value_1', 'key_2': 'value_2'}})#step_context.dialogs)
            logger.warning("user say no")
        # voir journal log severity == 0 and message == "notConfirmed"
            self.telemetry_client.track_trace(name='notConfirmed', properties={"destination":str(booking_details.destination),
                                                                            "origin":str(booking_details.origin),
                                                                            "travel_date":str(booking_details.travel_date),
                                                                            "return_date":str(booking_details.return_date),
                                                                            "budget":str(booking_details.budget)})
        
        return await step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=MessageFactory.text(
            msg)))


    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
