from app import app

def main():
    app.run(debug=True, host="0.0.0.0", port=5050)

if __name__ == "__main__":
    main()