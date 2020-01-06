from botadero import create_app

print()
print(' Ejecutando desde uwsgi.py ')
print()
app = create_app()

if __name__ == '__main__':
    app.run()
