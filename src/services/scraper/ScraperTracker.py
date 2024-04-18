from selenium import webdriver
from bs4 import BeautifulSoup


class ScraperTracker:
    def __init__(self, username: str) -> None:
        self.username = self.replace_hashtag(username)

    def replace_hashtag(self, username):
        return username.replace("#", "%23") if "#" in username else username

    def get_options(self) -> webdriver.ChromeOptions:
        # Configuración de las opciones del navegador
        options = webdriver.ChromeOptions()
        options.add_argument("--enable-javascript")
        options.add_argument("--enable-cookies")
        options.add_argument("--enable-chrome-browser-cloud-management")
        return options

    def find_value_with_label(self, labels: list, target_label: str):
        for label in labels:
            label_text = label.text.strip()
            if label_text.lower() == target_label.lower():
                # Si coincide, encontrar el elemento "value" correspondiente que está al mismo nivel que el elemento "label"
                value = label.find_next_sibling('div', class_='value')
                if value:
                    return value.text.strip()
                else:
                    return ""


    def search_by_classname_and_attribute(self, tag, element_dom: str, class_name: str = None, attribute_value: str = None) -> bool:
        if tag.name != element_dom:
            return False
        
        if class_name is not None and class_name not in tag.get("class", []):
            return False
        
        if attribute_value is not None and tag.get(attribute_value) != "":
            return False
        
        return True



    def get_stats(self):
        # Inicializar el navegador con las opciones configuradas
        driver = webdriver.Chrome(options=self.get_options())
        driver.get(f"https://tracker.gg/valorant/profile/riot/{self.username}/overview")
        
        # Obtener el contenido de la página después de que JavaScript haya cargado los datos
        page_source = driver.page_source
        driver.quit()  # Cerrar el navegador después de obtener el contenido
        
        soup = BeautifulSoup(page_source, "html.parser")

        exists_user = soup.find(lambda tag: self.search_by_classname_and_attribute(tag, "span", "lead", "data-v-cdda8101"))
        if not(exists_user):
            is_private_profile = soup.find(lambda tag: self.search_by_classname_and_attribute(tag, "span", attribute_value="data-v-53edd0bf"))
            if not(is_private_profile):
                # Elementos a extraer
                basic_stats = soup.find_all(lambda tag: self.search_by_classname_and_attribute(tag, "span", "stat__value", "data-v-b9c27fa8"))
                range = basic_stats[0].text.strip()
                level = basic_stats[1].text.strip()

                labels = soup.find_all("div", class_="label")
                tracker_score = self.find_value_with_label(labels=labels, target_label="Tracker score")

                top_agents = ""
                count = 1
                agents_stats = soup.find_all(lambda tag:self.search_by_classname_and_attribute(tag, "div", "info", "data-v-626ba5f5"))
                for stat in agents_stats:
                    if stat.find("div", class_="label"):
                        top_agents += str(count) + ") " + stat.find("div", class_="value").text.strip() + " \n"
                        count += 1

                return {
                    "range": range,
                    "level": level,
                    "tracker_score": tracker_score,
                    "top_agents": top_agents
                }
            else:
                return {
                    "error": is_private_profile.text.strip()
                }
        else:
            return {
                "error": exists_user.text.strip()
            }


if __name__ == "__main__":
    # Ejemplo de uso
    scraper = ScraperTracker(username="Feduse#LAS")
    stats = scraper.get_stats()
    if stats:
        print(f"Estadísticas para {scraper.username}:")
        print(stats)
