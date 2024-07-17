from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app) 

def scan(target, ports):
    results = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(1, ports + 1)]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
    return results

def scan_port(ipaddress, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((ipaddress, port))
            return {"port": port, "status": "open"}
    except:
        return None

@app.route('/scan', methods=['POST'])
def scan_route():
    data = request.json
    targets = data.get('targets')
    ports = int(data.get('ports'))
    results = {}
    for target in targets:
        results[target] = scan(target.strip(), ports)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
