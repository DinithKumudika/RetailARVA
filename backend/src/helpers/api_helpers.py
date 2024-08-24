from flask import current_app as app

def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = f"{rule.endpoint:50s} {methods:20s} {str(rule)}"
        output.append(line)

    for line in sorted(output):
        print(f"route: {line}")