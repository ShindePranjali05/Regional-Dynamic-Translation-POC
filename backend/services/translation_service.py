from sarvamai import SarvamAI


class TranslationService:
    def __init__(self, api_key):
        self.client = SarvamAI(api_subscription_key=api_key)

    def translate_text(self, text, source_lang="en-IN", target_lang="hi-IN"):
        response = self.client.text.translate(
            input=text,
            source_language_code=source_lang,
            target_language_code=target_lang,
            model="sarvam-translate:v1"
        )

        if hasattr(response, "translated_text"):
            return response.translated_text

        if isinstance(response, dict) and "translated_text" in response:
            return response["translated_text"]

        return str(response)

    def translate_fields(self, fields_data, source_lang="en-IN", target_lang="hi-IN"):
        translated_data = {}

        for field_name, field_value in fields_data.items():
            if field_value and isinstance(field_value, str):
                translated_data[field_name] = self.translate_text(
                    field_value,
                    source_lang,
                    target_lang
                )
            else:
                translated_data[field_name] = field_value

        return translated_data