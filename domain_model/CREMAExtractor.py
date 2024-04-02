from .featureExtractor import FeatureExtractor

class CREMAExtractor(FeatureExtractor):
    
    def extract_features(self):
        # Aquí iría la lógica para extraer características HPCP del contenido proporcionado
        print("Extrayendo características HPCP...")
        # Suponiendo que "content" contiene el audio en formato array, aquí simplemente devolvemos el array original
        return self.content