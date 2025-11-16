from ..client import LLMClient
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class DeepSeekClient(LLMClient):
    def analyze_nfe(self, xml: str) -> List[str]:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return ["[IA] Configure DEEPSEEK_API_KEY"]

        prompt = f"Analise esta NF-e e dê 3 sugestões fiscais em PT-BR:\n\n{xml[:3000]}"
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        try:
            resp = httpx.post(
                "https://api.deepseek.com/v1/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=30
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"]
            return [line.strip() for line in text.split("\n") if "•" in line or line.strip()]
        except:
            return ["[IA] Erro na API"]
