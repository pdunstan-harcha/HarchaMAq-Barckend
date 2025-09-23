from app import create_app

app = create_app()

if __name__ == '__main__':
    # El host 0.0.0.0 permite acceder desde la red local (útil para probar desde el móvil)
    app.run(host='0.0.0.0', port=5000, debug=True)
