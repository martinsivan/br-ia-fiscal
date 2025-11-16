from lxml import etree
from ..ai.client import LLMClient
from ..utils.xml import extract_field
from typing import List, Dict

class NFeValidator:
    def __init__(self):
        self.llm = LLMClient()
        self.schema = etree.XMLSchema(etree.parse("br_ia_fiscal/schemas/nfe_v4.00.xsd"))

    def validate(self, xml_path: str) -> Dict:
        with open(xml_path, "rb") as f:
            doc = etree.parse(f)
        
        try:
            self.schema.assertValid(doc)
            structure_ok = True
            errors = []
        except etree.DocumentInvalid as e:
            structure_ok = False
            errors = [str(err) for err in e.error_log]

        ai_suggestions = self.llm.analyze_nfe(open(xml_path).read()) if structure_ok else []

        return {
            "valida": structure_ok,
            "erros": errors,
            "sugestoes_ia": ai_suggestions
        }
