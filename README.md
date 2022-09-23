# GPT Graph Search

This repository generates random graphs and generates prompts that ask GPT-3 to find paths through the graph. GPT-3's
response is parsed and we try to automatically determine if the response is correct, or if not, why.

You should expose an environment variable `OPENAI_API_KEY=sk-<key>` before you run this code.

```bash
python3 -m pip install -r requirements.txt
python3 src/main.py
```
