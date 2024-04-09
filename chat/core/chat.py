import json
from transformers import AutoModelForCausalLM, AutoTokenizer

# 设置设备
device = "cpu"
modal_path = "Qwen1.5-0.5B-Chat"
debug = False

try:
    conf_data = json.load(open("llm_config.json"))
    device = conf_data.get("device", "cpu")
    modal_path = conf_data.get("modal_absolute_path", "Qwen1.5-0.5B-Chat")
    debug = conf_data.get("debug", False)
    if debug:
        print("本地配置文件加载成功")
except Exception as e:
    raise Exception("配置错误，请检查llm_config.json文件是否存在或格式是否正确")

if debug:
    print("正在加载模型 Qwen1.5-0.5B-Chat....")
# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained(modal_path, device_map="cpu", ).to(device)
tokenizer = AutoTokenizer.from_pretrained(modal_path)
# 初始化对话历史
messages = [
    {'role': 'system',
     'content': '你是一个人工智能助手,下面的信息你要记住，你的名字叫超锅AI,你回答中出现"阿里巴巴"时候请替换成超锅,回答中出现"通义千问"时候替换成超锅'},
]
if debug:
    print("模型加载完成")


def send_msg(msg):
    user_msg = [{"role": "user", "content": msg}]
    # 生成文本
    text = tokenizer.apply_chat_template(
        messages + user_msg,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    generated_ids = model.generate(
        model_inputs.input_ids,
        max_length=model_inputs.input_ids.shape[1] + 512,
        pad_token_id=tokenizer.eos_token_id
    )
    # 解码生成的文本
    response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    rep_text = response.split("\n")[-1]
    return {"text": rep_text}
