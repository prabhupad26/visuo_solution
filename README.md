huggingface-cli download MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF --local-dir . --include '*Q2_K*gguf'



docker run -p 8080:8080 -v C://Users//mini-KRONOS//OneDrive//Documents//visuo_solution//models:/models ghcr.io/ggerganov/llama.cpp:server -m models/Llama-2-7B-instruct-text2sql.q4_k_m.gguf -c 512 --host 0.0.0.0 --port 8080


curl --request POST --url http://localhost:8080/completion --header "Content-Type: application/json" --data '{"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}'