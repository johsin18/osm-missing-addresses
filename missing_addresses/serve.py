import waitress
import missing_addresses

if __name__ == '__main__':
    print("Visit http://localhost/Leonberg/summary or http://localhost/PaperTown/summary")
    waitress.serve(missing_addresses.wsgi.application, port=80, url_scheme='http')
