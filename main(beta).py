from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters
from transformers import MarianMTModel, MarianTokenizer
from googletrans import Translator  # 언어 감지 및 번역용

# 번역기 초기화
translator = Translator()

# MarianMT 모델 로드 (영어 번역용)
tokenizer_en = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-ru-en')
model_en = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-ru-en')

# MarianMT 모델 로드 (한국어 번역용)
tokenizer_ko = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-ru-ko')
model_ko = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-ru-ko')

# 러시아어를 영어로 번역하는 함수
def translate_to_english(text):
    inputs = tokenizer_en(text, return_tensors="pt", padding=True)
    translated = model_en.generate(**inputs)
    return tokenizer_en.decode(translated[0], skip_special_tokens=True)

# 러시아어를 한국어로 번역하는 함수
def translate_to_korean(text):
    inputs = tokenizer_ko(text, return_tensors="pt", padding=True)
    translated = model_ko.generate(**inputs)
    return tokenizer_ko.decode(translated[0], skip_special_tokens=True)

# 채널 메시지 핸들러
def handle_channel_message(update: Update, context):
    message = update.channel_post.text
    detected_language = translator.detect(message).lang

    if detected_language == 'ru':  # 메시지가 러시아어일 경우
        english_translation = translate_to_english(message)
        korean_translation = translate_to_korean(message)

        # 출력할 메시지 포맷
        output_message = f"🇷🇺 원본 (러시아어):\n{message}\n\n🇬🇧 영어 번역:\n{english_translation}\n\n🇰🇷 한국어 번역:\n{korean_translation}"

        # 번역된 메시지를 다시 채널에 전송
        context.bot.send_message(chat_id=update.effective_chat.id, text=output_message)

# 봇 초기화 및 핸들러 추가
def main():
    # 봇 생성 (여기에 봇 토큰을 넣으세요)
    updater = Updater("7281341409:AAGrf83Mk4jUqNnHgpdY4VRfP68RI3a8Y4U", use_context=True)
    dispatcher = updater.dispatcher

    # 특정 채널('publicyes123')의 메시지 처리 핸들러 추가
    dispatcher.add_handler(MessageHandler(Filters.chat('publicyes123'), handle_channel_message))

    # 봇 실행
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
