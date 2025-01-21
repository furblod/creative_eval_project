from transformers import AutoModelForCausalLM, AutoTokenizer 

# Model ve tokenizer seçimi
model_name = "EleutherAI/gpt-neo-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Prompt (2-to-1 Multiplexer modülü için)
prompt = """
Create a Verilog module that implements a 2-to-1 multiplexer.

Module requirements:
1. Inputs: a (1 bit), b (1 bit), sel (1 bit selector)
2. Output: y (1 bit output)

Use standard Verilog syntax and include 'assign' statement for logic.
Ensure the module starts with 'module' and ends with 'endmodule'.
"""

# Modeli kullanarak yanıt üretme
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_new_tokens=300,
    do_sample=True,  # Çeşitliliği artırmak için örnekleme
    temperature=0.7,  # Daha çeşitli yanıtlar almak için sıcaklık
    top_k=50,  # En iyi 50 sonucu dikkate al
    top_p=0.9  # En olası sonuçların %90'ını seç
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Filtreleme: "module" ile başlayıp "endmodule" ile biten kısmı alalım
if "module" in response and "endmodule" in response:
    start_index = response.find("module")
    end_index = response.find("endmodule") + len("endmodule")
    filtered_code = response[start_index:end_index]
else:
    filtered_code = "No valid Verilog code found."

# Yanıtı yazdırma ve dosyaya kaydetme
print("Filtered Verilog Code:\n", filtered_code)
with open("models/generated_mux_code_filtered.v", "w") as f:
    f.write(filtered_code)
