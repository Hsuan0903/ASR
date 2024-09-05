import string
import re

# 示例 ATC 熱詞列表
action_hotwords = [
    "Scramble", "Holding Hands", "Flow Four", "Engaged", 
    "Mission Complete", "Initial Five", "Gear Check, Full Stop",
    "Go Cover", "IN", "OFF", "Cleared to Land",
    "Angle", "Heading",
]

ai_machine_hotwords = ['Alpha', 'Bravo', 'Delta', 'Gamma']

# 去除標點符號並將文本轉換為小寫
def remove_punctuation_and_lowercase(transcription):
    text = transcription.translate(str.maketrans("", "", string.punctuation))
    text = text.lower()
    return text

# 比對熱詞並返回匹配的關鍵詞
def find_matched_hotwords(text, hotwords):
    matched_words = []
    for word in hotwords:
        if word.lower() in text:
            matched_words.append(word)
    return matched_words

# 將數字字符串轉換為口語形式
def mixed_to_spoken(input_string):
    digit_to_word = {
        '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
    }

    def number_to_spoken(number_string):
        number_patterns = {
            '000': 'thousand',
        }
        for pattern, word in number_patterns.items():
            if number_string.endswith(pattern):
                num_len = len(number_string)
                if num_len > len(pattern):
                    prefix = number_string[:-len(pattern)]
                    prefix_spoken = ' '.join(digit_to_word[digit] for digit in prefix)
                    return f"{prefix_spoken} {word}"
                else:
                    return word
        return ' '.join(digit_to_word[digit] for digit in number_string)

    def process_alphanumeric_segment(segment):
        if segment.isdigit():
            return number_to_spoken(segment)
        else:
            return segment

    parts = re.split(r'(\d+)', input_string)
    spoken_parts = [process_alphanumeric_segment(part) for part in parts if part]
    
    # 用空格分隔部件並去除多餘的空格
    spoken_form = ' '.join(spoken_parts).strip()
    return re.sub(r'\s+', ' ', spoken_form)

# 將字母和數字分開
def separate_alphanumeric(text):
    pattern = re.compile(r'([a-zA-Z]+)(\d+)|(\d+)([a-zA-Z]+)')
    separated_text = pattern.sub(r'\1 \2\3 \4', text)
    return separated_text

# 處理轉錄文本，找到熱詞並轉換數字為口語形式
def process_transcription(transcription):
    cleaned_text = remove_punctuation_and_lowercase(transcription)
    separated_text = separate_alphanumeric(cleaned_text)
    
    matched_machine_hotwords = find_matched_hotwords(separated_text, ai_machine_hotwords)
    matched_action_hotwords = find_matched_hotwords(separated_text, action_hotwords)
    
    spoken_text = mixed_to_spoken(separated_text)
    
    return (matched_machine_hotwords, matched_action_hotwords), spoken_text


# 定義 AI 機器與動作的編碼
ai_machines = {
    "Tiger One": 1, "Tiger Two": 2, "Tiger Tree": 3, "Tiger Four": 4,
    "Viper One": 5, "Viper Two": 6, "Viper Tree": 7, "Viper Four": 8
}

actions = {
    "Scramble": 1, "Holding Hands": 2, "Engage": 3, "Mission Complete": 4,
    "Initial Five": 5, "Go Cover": 6, "In": 7, "Off": 8, "Cleared for Takeoff": 9,
    "Cleared to Land": 10, "Go Around": 11, "Heading": 12, "Angel": 13
}

# 編碼函數
def encode_command(ai_machine, action, number=None):
    ai_code = ai_machines.get(ai_machine, -1)
    action_code = actions.get(action, -1)
    
    if number is None:
        number = -1  # 表示無數字部分
    
    return (ai_code, action_code, number)

if __name__ == "__main__":
    # 示例使用
    transcription = "Data file of 3000"
    matched_hotwords, spoken_text = process_transcription(transcription)
    print("Matched hotwords:", matched_hotwords)
    print("Spoken form:", spoken_text)
