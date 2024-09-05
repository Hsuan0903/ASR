import os
import whisper
import torch
from glob import glob
import torchaudio
import json
from lib.text_postprocess import process_transcription
from lib.metric import compute_wer, compute_cer, compute_real_time_factor
import csv
import time
import evaluate

# 設定模型權重檔案

model_name = '/mnt/whisper_main/weight/large-v2.pt'  # 可以選擇 'tiny', 'base', 'small', 'medium', ''medium.en, 'large-v2', 'large-v3'

start_time = time.time()
model = whisper.load_model(model_name)
load_model_time = time.time() - start_time
print(load_model_time)
is_prompt = True
# 設定資料夾路徑
audio_folder = 'finetune_code/wav/Li/'  # 替換成你的資料夾路徑
json_file_path = 'finetune_code/wav/Li.json'

if is_prompt:
    csv_file_path = 'openai_results_with_prompt_Li_v2.csv'
else:
    csv_file_path = 'openai_results_Li_v2.csv'

gt_dict = {}
# Open and read the JSON file line by line
with open(json_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Parse the JSON line into a Python dictionary
        data = json.loads(line.strip())

        # Extract the 'sentence' field which contains the reference text
        reference_text = data.get('sentence', '').strip()

        # Extract the file name from the 'path' field
        file_name = data['audio']['path'].split('/')[-1]
        file_name = file_name[:-4]

        # Print the file name and its corresponding reference text
        gt_dict[file_name] = reference_text.lower()

# 獲取資料夾內所有 .wav 文件
audio_files = glob(os.path.join(audio_folder, '*.wav'))

# 檢查是否有可用的 GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

wer_metric = evaluate.load(f'finetune_code/metrics/wer.py')


# 打開 CSV 文件進行寫入
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # 寫入標頭行
    csv_writer.writerow(
        ['Filename', 'Ground Truth', 'Prediction', 'Postprocessed', 'Inference Time', 'WER', 'CER', 'RTF'])

    # 初始化總計和計數
    total_infer_time = 0
    total_wer = 0
    total_cer = 0
    total_rtf = 0
    file_count = 0

    # 進行語音識別
    for audio_file in audio_files:
        print(f'Processing file: {audio_file}')

        # # 使用 torchaudio 讀取音頻文件
        # waveform, sample_rate = torchaudio.load(audio_file)

        # # 如果需要將音頻轉換為模型所需的格式
        # if sample_rate != 16000:
        #     transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        #     waveform = transform(waveform)

        # # Whisper 模型期望音頻數據為 numpy array 格式
        # audio = waveform.squeeze().numpy()

        # 進行推論，限制語言為英文
        options = {
            "fp16": torch.cuda.is_available(),
            "language": "en",
            "task": "transcribe",  # 確保進行轉錄而不是翻譯
            # "initial_prompt": """
            #                   two ,off, Alpha, Bravo, Beta, Delta, Gamma, Scramble, Holding Hands, Flow Four, Engaged, Mission Complete, Initial Five, Gear Check, Full Stop, Go Cover, IN, OFF, Cleared to Land, Angle and Heading.
            #                   """ if is_prompt else None,
            "initial_prompt": """
                              two , off, tiger, viper, Scramble, Holding Hands, fluid four, Engaged, Mission Complete, Initial Five, wedge, Go Cover, IN, OFF, Cleared to Land, Angle and Heading, Cleared for Takeoff, Go Around.
                              """ if is_prompt else None, # 李博新版 240905
        }

        start_time = time.time()
        result = model.transcribe(audio_file, **options)
        infer_time = time.time() - start_time

        gt = gt_dict[audio_file.split('/')[-1][:-4]]
        ori_pred = result['text']

        hotword, pred = process_transcription(ori_pred)

        # 計算 WER、CER 和 RTF
        print(gt)
        print(pred)
        print(hotword)
        wer_metric.add_batch(predictions=[gt], references=[pred])
        wer_value = compute_wer(gt, pred)
        cer_value = compute_cer(gt, pred)
        rtf_value = compute_real_time_factor(audio_file, infer_time)

        # 更新總計和計數
        total_infer_time += infer_time
        total_wer += wer_value
        total_cer += cer_value
        total_rtf += rtf_value
        file_count += 1

        # 打印結果
        print(
            f"inference time: {infer_time:.4f} | gt: {gt} | ori_pred: {ori_pred} | text: {pred} | wer: {wer_value:.2%} | cer: {cer_value:.2%} | rtf: {rtf_value:.4F}")

        # 寫入結果到 CSV 文件
        csv_writer.writerow([os.path.basename(audio_file), gt, ori_pred, pred, f"{infer_time:.4f}", f"{wer_value:.2%}",
                             f"{cer_value:.2%}", f"{rtf_value:.4F}"])

        # 計算平均值
    avg_infer_time = total_infer_time / file_count
    avg_wer = total_wer / file_count
    avg_cer = total_cer / file_count
    avg_rtf = total_rtf / file_count
    m = wer_metric.compute()

    # 打印和寫入平均值到 CSV 文件
    print(
        f"Average Inference Time: {avg_infer_time:.4f} | Average WER: {avg_wer:.2%} | Average CER: {avg_cer:.2%} | Average RTF: {avg_rtf:.4F}")
    csv_writer.writerow(
        ['Averages', '', '', '', f"{avg_infer_time:.4f}", f"{avg_wer:.2%}", f"{avg_cer:.2%}", f"{avg_rtf:.4F}"])
    print(f"评估结果： wer={round(m, 5)}")
