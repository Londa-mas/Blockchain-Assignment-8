EXPLORER_HTML = """
<!DOCTYPE html>
<html>
<head><title>BLCH9X2 Minimal Explorer</title></head>
<body style="font-family: Arial; margin: 40px;">
    <h1>Blockchain Node Explorer</h1>
    <hr>
    <h2>Mempool (Pending Transactions)</h2>
    <pre>{{ mempool | tojson(indent=2) }}</pre>
    <h2>Chain Tip / Blocks</h2>
    <pre>{{ chain | tojson(indent=2) }}</pre>
</body>
</html>
"""