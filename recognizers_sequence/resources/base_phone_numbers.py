# ------------------------------------------------------------------------------
# <auto-generated>
#     This code was generated by a tool.
#     Changes to this file may cause incorrect behavior and will be lost if
#     the code is regenerated.
# </auto-generated>
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# ------------------------------------------------------------------------------

# pylint: disable=line-too-long


class BasePhoneNumbers:
    NumberReplaceToken = '@builtin.phonenumber'
    WordBoundariesRegex = f'\\b'
    NonWordBoundariesRegex = f'\\B'
    EndWordBoundariesRegex = f'\\b'
    PreCheckPhoneNumberRegex = f'(\\d{{1,4}}.){{2,4}}\\s?\\d{{2,3}}'

    def GeneralPhoneNumberRegex(WordBoundariesRegex, EndWordBoundariesRegex):
        return f'({WordBoundariesRegex}(((\\d[\\s]?){{4,12}}))(-?[\\d\\s?]{{3}}\\d)(?!-){EndWordBoundariesRegex})|(\\(\\d{{5}}\\)\\s?\\d{{5,6}})|\\+\\d{{2}}\\(\\d\\)\\d{{10}}'

    def BRPhoneNumberRegex(WordBoundariesRegex, NonWordBoundariesRegex, EndWordBoundariesRegex):
        return f'((\\(\\s?(\\+\\s?|00)55\\s?\\)\\s?)|(((?<!\\d)\\+\\s?|{WordBoundariesRegex}00)55\\s?)|{WordBoundariesRegex})?((({NonWordBoundariesRegex}\\(\\s?))\\d{{2,3}}(\\s?\\))|({WordBoundariesRegex}\\d{{2,3}}))\\s?\\d{{4,5}}-?\\d{{3,5}}(?!-){EndWordBoundariesRegex}'

    def UKPhoneNumberRegex(WordBoundariesRegex, NonWordBoundariesRegex, EndWordBoundariesRegex):
        return f'((({WordBoundariesRegex}(00)|{NonWordBoundariesRegex}\\+)\\s?)?({WordBoundariesRegex}\\d{{2}}\\s?)?((\\s?\\(0\\)[-\\s]?|{WordBoundariesRegex}|(?<=(\\b^#)\\d{{2}}))\\d{{2,5}}|\\(0\\d{{3,4}}\\))[/-]?\\s?(\\d{{5,8}}|\\d{{3,4}}[-\\s]?\\d{{3,4}})(?!-){EndWordBoundariesRegex})'

    def DEPhoneNumberRegex(WordBoundariesRegex, EndWordBoundariesRegex):
        return f'((\\+\\d{{2}}\\s?((\\(0\\))?\\d\\s?)?|{WordBoundariesRegex})(\\d{{2,4}}\\s?[-/]?[\\s\\d]{{7,10}}\\d)(?!-){EndWordBoundariesRegex})'

    def USPhoneNumberRegex(WordBoundariesRegex, NonWordBoundariesRegex, EndWordBoundariesRegex):
        return f'((((({NonWordBoundariesRegex}\\+)|{WordBoundariesRegex})1(\\s|-)?)|{WordBoundariesRegex})?(\\d{{3}}\\)[-\\s]?|\\(\\d{{3}}\\)[-\\.\\s]?|{WordBoundariesRegex}\\d{{3}}\\s?[-\\.]?\\s?)|{WordBoundariesRegex})[2-9]\\d{{2}}\\s?[-\\.]?\\s?\\d{{4}}(\\s?(x|X|ext)\\s?\\d{{3,5}})?(?!(-\\s?\\d)){EndWordBoundariesRegex}'

    def CNPhoneNumberRegex(WordBoundariesRegex, EndWordBoundariesRegex):
        return f'(({WordBoundariesRegex}00\\s?)?\\+?(86|82|81)\\s?-?\\s?)?((({WordBoundariesRegex}|(?<=(86|82|81)))\\d{{2,5}}\\s?-?\\s?|\\(\\d{{2,5}}\\)\\s?)\\d{{4}}\\s?-?\\s?\\d{{4}}(\\s?-?\\s?\\d{{4}})?|(\\b|(?<=(86|82|81)))\\d{{3}}\\s?-?\\s?\\d{{4}}\\s?-?\\s?\\d{{4}})(?!-){EndWordBoundariesRegex}'

    def DKPhoneNumberRegex(WordBoundariesRegex, EndWordBoundariesRegex):
        return f'((\\(\\s?(\\+\\s?|00)45\\s?\\)\\s?)|(((?<!\\d)\\+\\s?|\\b00)45\\s?)|{WordBoundariesRegex})(\\s?\\(0\\)\\s?)?((\\d{{8}})|(\\d{{4}}\\s?-?\\s?\\d{{4,6}})|((\\d{{2}}[\\s-]){{3}}\\d{{2}})|(\\d{{2}}\\s?-?\\s?\\d{{3}}\\s?-?\\s?\\d{{3}}))(?!-){EndWordBoundariesRegex}'

    def ITPhoneNumberRegex(WordBoundariesRegex, EndWordBoundariesRegex):
        return f'((\\(\\s?(\\+\\s?|00)39\\s?\\)\\s?)|(((?<!\\d)\\+\\s?|\\b00)39\\s?)|{WordBoundariesRegex})((0[\\d-]{{4,12}}\\d)|(3[\\d-]{{7,12}}\\d)|(0[\\d\\s]{{4,12}}\\d)|(3[\\d\\s]{{7,12}}\\d))(?!-){EndWordBoundariesRegex}'

    def NLPhoneNumberRegex(WordBoundariesRegex, EndWordBoundariesRegex):
        return f'((((\\(\\s?(\\+\\s?|00)31\\s?\\)\\s?)|(((?<!\\d)\\+\\s?|{WordBoundariesRegex}00)31\\s?))?((({WordBoundariesRegex}|(?<=31))0?\\d{{1,3}}|\\(\\s?0?\\d{{1,3}}\\s?\\)|\\(0\\)[-\\s]?\\d{{1,3}})((-?[\\d]{{5,11}})|(\\s[\\d\\s]{{5,11}}))\\d))|\\b\\d{{10,12}})(?!-){EndWordBoundariesRegex}'

    def SpecialPhoneNumberRegex(WordBoundariesRegex, EndWordBoundariesRegex):
        return f'({WordBoundariesRegex}(\\d{{3,4}}[/-]\\d{{1,4}}[/-]\\d{{3,4}}){EndWordBoundariesRegex})'
    NoAreaCodeUSPhoneNumberRegex = f'(?<!(-|-\\s|\\d|\\)|\\)\\s|\\.))[2-9]\\d{{2}}\\s?[-\\.]\\s?\\d{{4}}(?!(-\\s?\\d))\\b'
    InternationDialingPrefixRegex = f'0(0|11)$'
    TypicalDeductionRegexList = [r'^\d{5}-\d{4}$', r'\)\.', r'^0(0|11)(-)']
    PhoneNumberMaskRegex = f'([0-9a-e]{{2}}(\\s[0-9a-e]{{2}}){{7}})'
    CountryCodeRegex = f'^(\\(\\s?(\\+\\s?|00)\\d{{1,3}}\\s?\\)|(\\+\\s?|00)\\d{{1,3}})'
    AreaCodeIndicatorRegex = f'\\('
    FormatIndicatorRegex = f'(\\s|-|/|\\.)+'
    ColonMarkers = [r':']
    ColonPrefixCheckRegex = f'(([a-z])\\s*$)'
    AmbiguityFiltersDict = dict([("^\\d{4}-\\d{4}$", "omb(\\s*(no(\\.)?|number|#))?:?\\s+\\d{4}-?\\d{4}")])
    SpecialBoundaryMarkers = [r'-', r' ']
    BoundaryMarkers = [r'-', r'.', r'/', r'+', r'#', r'*']
    ForbiddenPrefixMarkers = [r',', r':', r'%']
    ForbiddenSuffixMarkers = [r'/', r'+', r'#', r'*', r':', r'%']
    SSNFilterRegex = f'^\\d{{3}}-\\d{{2}}-\\d{{4}}$'
# pylint: enable=line-too-long
