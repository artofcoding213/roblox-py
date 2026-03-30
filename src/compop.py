"""Compare operation description"""

import ast


class CompareOperationDesc:
    """Compare operation description"""

    OPERATION = {
        ast.Eq: ["__eq__"],
        ast.NotEq: "~=",
        ast.Lt: "<",
        ast.LtE: "<=",
        ast.Gt: ">",
        ast.GtE: ">=",
        ast.Is: "==",
        ast.IsNot: "~=",
    }
