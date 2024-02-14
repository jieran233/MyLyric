import re
import hanzidentifier as hanzi

languages = {'en': 'en',
             'sc': 'zh_hans',
             'tc': 'zh_hant',
             'ja': 'ja',
             'ko': 'ko'}

japanese_regex = r'([ぁ-んァ-ンｧ-ﾝﾞﾟ])'
korean_regex = r'([\u3131-\u314e\u314f-\u3163\uac00-\ud7a3])'


def identify_language(text: str):
    # Japanese
    if re.search(japanese_regex, text):
        return languages['ja']

    # Korean
    elif re.search(korean_regex, text):
        return languages['ko']

    # Chinese
    elif hanzi.has_chinese(text):

        print(hanzi.identify(text))

        if hanzi.is_simplified(text):
            return languages['sc']  # Simplified Chinese
        else:
            return languages['tc']  # Traditional Chinese

    # English
    else:
        return languages['en']
