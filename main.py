import os
from google import genai
from dotenv import load_dotenv
from src.connectors.ofx_connector import read_ofx_file
from src.extractors.gemini_extractor import GeminiExtractor
from pathlib import Path

load_dotenv()

def main():
    # 1. Define o caminho do arquivo OFX real
    file_path_ofx = Path(__file__).parent / "NU_FILE.ofx"

    # 2. Lê e converte o arquivo OFX em dicionário limpo
    raw_data = read_ofx_file(file_path_ofx)

    # 3. Extrai a lista de transações do dicionário
    transactions = raw_data["transactions"]

    # 4. Cria o client aqui (ponto de entrada da aplicação)
    #    e injeta na dependência — Dependency Inversion na prática
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    extractor = GeminiExtractor(client=client)

    # 5. Envia para o Gemini e recebe o objeto Pydantic validado
    analysis = extractor.analyze_expenses(transactions)

    # 6. Converte o objeto Pydantic em JSON formatado
    json_output = analysis.model_dump_json(indent=4)

    # 7. Salva o resultado em um arquivo
    output_path = Path(__file__).parent / "insight_financeiro.json"
    output_path.write_text(json_output, encoding="utf-8")

    print(f"Análise concluída! Resultado salvo em: {output_path}")
    print(json_output)

if __name__ == "__main__":
    main()
