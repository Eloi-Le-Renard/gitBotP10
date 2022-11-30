#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "6dbe05b0-3b5c-428f-a7f2-9f6a2014207f")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Pzx8Q~waiMQi3pxBy612g5DvrWT9GTNzSRAnQbs7")
    LUIS_APP_ID = os.environ.get("LuisAppId", "992aa391-8f2e-4d23-ad82-be89361b9092")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "61a8d29177404906829359111ef928ea")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "luise-api-p10.cognitiveservices.azure.com")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "fc2c70d5-709a-45c8-b818-2fffba7463f3"
    )