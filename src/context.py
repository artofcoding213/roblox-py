"""Class to store the python code context"""

from tokenend import *
from symbols import SymbolsStack


class Context:
    """Class to store the python code context"""

    def __init__(self, values=None):
        values = (
            values
            if values is not None
            else {
                "token_end_mode": TokenEndMode.LINE_FEED,
                "class_name": "",
                "locals": SymbolsStack(),
                "globals": SymbolsStack(),  # Not working yet
                "loop_label_name": "",
                "docstring": False,
                'direct_class': False,
            }
        )

        self.ctx_stack = [values]
        self.scope_depth = 0

    def last(self):
        """Return actual context state"""
        return self.ctx_stack[-1]

    def push(self, values):
        """Push new context state with new values"""
        value = self.ctx_stack[-1].copy()
        value.update(values)
        self.ctx_stack.append(value)

    def pop(self):
        """Pop last context state"""
        assert (
            len(self.ctx_stack) > 1
        ), "Pop context failed. This is a last context in the stack."
        return self.ctx_stack.pop()
    
    def exists_in_any_scope(self, var: str):
        if self.ctx_stack == None:
            return False

        for ctx in reversed(self.ctx_stack):
            if ctx['locals'] and ctx['locals'].exists(var):
                return True
            
        return False

    def push_scope(self):
        self.scope_depth += 1
        self.ctx_stack[-1].update(direct_class=False)

    def pop_scope(self):
        self.scope_depth -= 1
    
    def is_top_level(self):
        return self.scope_depth == 0
