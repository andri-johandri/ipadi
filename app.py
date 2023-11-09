from cms import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True,port=3232,host='0.0.0.0')
