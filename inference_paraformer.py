from funasr import AutoModel
import glob
import time
import re
from lib.metric import compute_wer, compute_cer, compute_real_time_factor
import json
import csv
from lib.text_postprocess import mixed_to_spoken, separate_alphanumeric


# Replace 'your_file.json' with the actual JSON file path  
json_file_path = 'real_data_V2/annotations.json'  
files = glob.glob("real_data_V2/wav/*.wav")


# json_file_path = 'fake_data/annotations.json'  
# files = glob.glob("fake_data/wav/*.wav")


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


start_time = time.time()
model = AutoModel(

    model="models/speech_paraformer_asr-en-16k-vocab4199-pytorch",
    
    ## disable check update of funasr
    disable_update=True,
    output_dir="outputs_paraformer",
    disable_pbar=True,
    device='cuda:0'
)
end_time = time.time()
print(f"loading time: {end_time - start_time}")

for i in range(5):
    res = model.generate(
                input=files[i],
                language="en",
                ban_emo_unk=True,
            )
            
# Initialize CSV writer  
csv_file_path = 'paraformer_fake_results.csv'  
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:  
    csv_writer = csv.writer(csv_file)  
    # Write the header row  
    csv_writer.writerow(['Filename', 'Ground Truth', 'Prediction', 'Inference Time', 'WER', 'CER', 'RTF'])  

    # Initialize totals and counts  
    total_infer_time = 0  
    total_wer = 0  
    total_cer = 0  
    file_count = 0
    total_rtf = 0

    for file in files:
        start_time = time.time()
        res = model.generate(
            input=file,
            # cache={},
            # pred_timestamp=True,
            # return_raw_text=True,
            # sentence_timestamp=True,
            # en_post_proc=True,
        )
        end_time = time.time()
        infer_time = end_time - start_time
        gt = gt_dict[res[0]['key']]
        pred = mixed_to_spoken(separate_alphanumeric( res[0]['text'].lower()))

        wer = compute_wer(gt, pred)
        cer = compute_cer(gt, pred)
        rtf = compute_real_time_factor(file, infer_time)

        # Update totals and counts  
        total_infer_time += infer_time  
        total_wer += wer  
        total_cer += cer
        total_rtf += rtf
        file_count += 1

        print(f"inference time: {infer_time:.4f}", "|",f"gt: {gt}","|", f"text: {pred}", "|", f"wer: {wer:.2%}", "|", f"cer: {cer:.2%}", "|", f"rtf: {rtf:.4F}")
        # Write the results to the CSV file  
        csv_writer.writerow([res[0]['key'], gt, pred, f"{infer_time:.4f}", f"{wer:.2%}", f"{cer:.2%}",  f"{rtf:.4F}"])
        
    # Calculate averages  
    avg_infer_time = total_infer_time / file_count  
    avg_wer = total_wer / file_count  
    avg_cer = total_cer / file_count
    avg_rtf = total_rtf / file_count
  
    # Print and write the averages to the CSV file  
    print(f"Average Inference Time: {avg_infer_time:.4f} | Average WER: {avg_wer:.2%} | Average CER: {avg_cer:.2%} | Average RTF: {rtf:.4F}")  
    csv_writer.writerow(['Averages', '', '', f"{avg_infer_time:.4f}", f"{avg_wer:.2%}", f"{avg_cer:.2%}", f"{avg_rtf:.4F}"])  
    