from __future__ import annotations
from typing import List, Dict, Any
from pydantic import BaseModel
from lxml import etree
import requests
from rich.console import Console

console = Console()

class ValidationError(BaseModel):
    codigo: str
    mensagem: str
    campo: str
    sugestao_ia: str | None = None

class NFeValidator:
    def __init__(self, llm: str = "grok"):
        self.llm = llm
        self.schema_url = "https://www.nfe.fazenda.gov.br/portal/exibirArquivo.aspx?conteudo=9Qz5p9Y9Qz5p9Y="  # Schema v4

    def validate_xml_structure(self, xml_content: str) -> List[ValidationError]:
        errors = []
        try:
            schema_doc = etree.fromstring(requests.get(self.schema_url).content)
            schema = etree.XMLSchema(schema_doc)
            doc = etree.fromstring(xml_content.encode())
            schema.assertValid(doc)
        except etree.DocumentInvalid as e:
            for error in e.error_log:
                errors.append(ValidationError(
                    codigo="XML-001",
                    mensagem=str(error.message),
                    campo=error.path or "desconhecido",
                    sugestao_ia=None
                ))
        except Exception as e:
            errors.append(ValidationError(codigo="XML-000", mensagem=str(e), campo="root"))
        return errors

    def analyze(self, xml_content: str) -> Dict[str, Any]:
        structure_errors = self.validate_xml_structure(xml_content)
        ai_suggestions = self._ask_ai(xml_content) if not structure_errors else []

        return {
            "valida": len(structure_errors) == 0,
            "erros_estrutura": [e.dict() for e in structure_errors],
            "sugestoes_ia": ai_suggestions,
            "summary": self._generate_summary(structure_errors, ai_suggestions)
        }

    def _ask_ai(self, xml_content: str) -> List[str]:
        # Simulação realista (vamos integrar Grok API no Sprint 2)
        return [
            "Alíquota ICMS suspeita no item 2 (SP → 12% em vez de 18%)",
            "Considere substituição tributária para economizar R$ 800"
        ]

    def _generate_summary(self, errors, suggestions) -> str:
        if not errors and not suggestions:
            return "NF-e válida e otimizada!"
        elif errors:
            return f"{len(errors)} erro(s) de estrutura encontrado(s)."
        else:
            return f"{len(suggestions)} sugestão(ões) de otimização."
