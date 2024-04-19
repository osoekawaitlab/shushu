import json
from io import StringIO
from logging import Logger
from subprocess import run

from ..models import BaseDataModel, Element, ElementSequence, json_schema_to_data_model
from ..types import CodeString
from .base import BaseDataProcessor
from .exceptions import PythonCodeError


class PythonCodeDataProcessor(BaseDataProcessor):
    def __init__(self, code: CodeString, payload: BaseDataModel, logger: Logger):
        super(PythonCodeDataProcessor, self).__init__(payload=payload, logger=logger)
        self._code = code

    @classmethod
    def _export_element(cls, element: Element) -> str:
        return element.model_dump_json(by_alias=False).replace("\\", "\\\\").replace('"', '\\"')

    @classmethod
    def _export_element_sequence(cls, element_sequence: ElementSequence) -> str:
        return element_sequence.model_dump_json(by_alias=False).replace("\\", "\\\\").replace('"', '\\"')

    @classmethod
    def _export_payload(cls, payload: BaseDataModel) -> str:
        if isinstance(payload, Element):
            return cls._export_element(payload)
        if isinstance(payload, ElementSequence):
            return cls._export_element_sequence(payload)
        raise TypeError(f"Unsupported payload type: {type(payload)}")

    def perform(self) -> BaseDataModel:
        model_exporting_string = self._export_payload(self.payload)
        result = run(
            [
                "python",
                "-c",
                self._code
                + f"""
import json
import sys

res = convert({self.payload.__class__.__name__}(**json.loads('{model_exporting_string}')))
json.dump(res.model_json_schema(), sys.stdout, ensure_ascii=False)
sys.stdout.write('\\n')
sys.stdout.write(res.model_dump_json())
""",
            ],
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            self.log_error(result.stderr)
            raise PythonCodeError(result.stderr)
        (json_schema, serizlied_data) = [json.loads(ln) for ln in StringIO(result.stdout).readlines()]
        dynamic_model = json_schema_to_data_model(json_schema)
        return dynamic_model.model_validate(serizlied_data)
