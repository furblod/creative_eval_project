from transformers import AutoModelForCausalLM, AutoTokenizer

# Model ve tokenizer seçimi
model_name = "EleutherAI/gpt-neo-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Prompt
prompt = """
Write a Verilog module for a 2-bit adder with carry-in and carry-out.

Inputs:
- a (1 bit)
- b (1 bit)
- cin (1 bit, carry-in)

Outputs:
- sum (1 bit)
- cout (1 bit, carry-out)

The module should be written in Verilog syntax:
"""

# Modeli kullanarak yanıt üretme
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=300)
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
with open("models/generated_code_gpt_neo_1.3B.v", "w") as f:
    f.write(filtered_code)
