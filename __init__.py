import os
import json
from . import yaml3 as yaml
from cudatext import *

class Command:

    def check(self):

        carets = ed.get_carets()
        if len(carets)!=1:
            msg_status('JSON-YAML: Cannot handle multi-carets')
            return False
        return True

    def conv_json(self, s):
        s = json.loads(s)
        s = yaml.safe_dump(
          s,
          indent=2,
          default_flow_style=False,
        )
        return s

    def conv_yaml(self, s):

        s = yaml.load(s)
        s = json.dumps(
          s,
          indent=2,
          ensure_ascii=False,
          sort_keys=False,
        )
        return s

    def work(self, conv, lexer, tooltip):

        if not self.check(): return

        s = ed.get_text_sel()
        is_sel = bool(s)
        if not is_sel:
            s = ed.get_text_all()

        try:
            s = conv(s)
        except Exception as e:
            return msg_status(tooltip+': '+str(e))

        if not s:
            return msg_status(tooltip+': Cannot convert')

        file_open('')
        ed.set_text_all(s)
        ed.set_prop(PROP_LEXER_FILE, lexer)
        msg_status(tooltip+': '+('Converted selection' if is_sel else 'Converted entire document'))

    def json_to_yaml(self):

        self.work(self.conv_json, 'YAML', 'JSON->YAML')

    def yaml_to_json(self):

        self.work(self.conv_yaml, 'JSON', 'YAML->JSON')
