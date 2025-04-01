from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    career = request.args.get('career', '')
    if not career:
        return jsonify({"error": "Career not provided"}), 400

    try:
        url = f"https://en.wikipedia.org/wiki/{career.replace(' ', '_')}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.select('p')
        intro = ""

        for p in paragraphs:
            text = p.get_text().strip()
            if text:
                intro = text
                break

        return jsonify({"intro": intro})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
