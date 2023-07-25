import utils.casascrap as scrap
import utils.casalimpia as limpia

def main():
    #Scrapeo
    scrap.main() # --> scrapeo con selenium de la web de la casa encendida
    #Limpieza de datos 
    limpia.save_casa_limpia() # --> guarda en "data/casa-encendida" los datasets que se manipularán en los notebooks
main()