import requests
import time
from urllib.parse import urlparse

class SecondHandSongsAPI:
    def __init__(self):
        self.base_url = "https://secondhandsongs.com"
        
    def search_performance(self, title, performer):
        url = f"{self.base_url}/search/performance"
        parameters = {"title": title, "performer": performer, "format": "json"}
        
        wait_time = 10  # Tiempo de espera en segundos entre intentos
        
        while True:
            try:
                respuesta = requests.get(url, params=parameters)
                respuesta.raise_for_status()  # Throws an exception if there is an error in the HTTP request
                
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    return datos
                else:
                    print("Error when making the request:", respuesta.status_code)
            except requests.exceptions.RequestException as err:
                print("Error when making the request:", err)

            # Wait before trying again
            print(f"Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)

    def search_artist(performer):
        url = "https://secondhandsongs.com/search/artist"
        parameters = {"commonName": performer, "format": "json"}
        
        try:
            respuesta = requests.get(url, params=parameters)
            respuesta.raise_for_status()  # Throws an exception if there is an error in the HTTP request
            
            if respuesta.status_code == 200:
                datos = respuesta.json()
                return datos
            else:
                print("Error when making the request::", respuesta.status_code)
        except requests.exceptions.RequestException as err:
            print("Error when making the request::", err)
        return None

    def search_work(title):
        url = "https://secondhandsongs.com/search/work"
        parameters = {"title": title, "format": "json"}
        
        try:
            respuesta = requests.get(url, params=parameters)
            respuesta.raise_for_status()  # Throws an exception if there is an error in the HTTP request
            
            if respuesta.status_code == 200:
                datos = respuesta.json()
                return datos
            else:
                print("Error when making the request:", respuesta.status_code)
        except requests.exceptions.RequestException as err:
            print("Error when making the request:", err)
        return None
    
    def extract_id(self, url):
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        return path_parts[-1]

# Example

if __name__ == "__main__":
    api = SecondHandSongsAPI()
    results = api.search_performance("Blackbird", "Beatles")
    print(results)

    if results:
        total_results = results.get("totalResults", 0)
        print("Total performances found:", total_results)
        
        result_page = results.get("resultPage", [])
        for performance in result_page:
            print("Title:", performance.get("title"))
            print("Interprete:", performance.get("performer", {}).get("name"))
            print("URL:", performance.get("uri"))
            print("Is original:", performance.get("isOriginal"))
            print("ID:", api.extract_id(performance.get("uri")))
            print("-----")
    else:
        print("No se encontraron performancees para el título '{}' interpretado por '{}'".format("Blackbird", "Beatles"))
