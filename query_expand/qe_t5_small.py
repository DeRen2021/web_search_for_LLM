from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 加载模型和分词器
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def expand_query(query):
    # 指令格式更自由（无需严格的前缀）
    input_text = f"Expand this search query to include related terms: {query}"
    
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding="max_length"
    )
    
    outputs = model.generate(
        inputs.input_ids,
        max_new_tokens=100,
        do_sample=True,       # 允许更长扩展
        temperature=0.7,           # 控制创造性（0~1，越大越随机）
        num_beams=3,               # 提升输出质量
        early_stopping=True
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 测试
if __name__ == "__main__":
    print(expand_query("china is"))
    # 可能输出：lunar settlements, official moon capital city, proposed lunar colony governments