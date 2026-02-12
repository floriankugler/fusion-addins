import adsk.core

def nurbs_length(nurbs: adsk.core.NurbsCurve3D) -> float:
    _, start, end = nurbs.evaluator.getParameterExtents()
    _, length = nurbs.evaluator.getLengthAtParameter(start, end)
    return length