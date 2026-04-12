def system():
    import sys
    p = sys.platform
    if p == "darwin": return "mac"
    if p.startswith("win"): return "win"
    return "linux"