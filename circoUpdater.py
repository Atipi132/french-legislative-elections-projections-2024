import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def getDesistements():
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(driver_options)
    URL = "https://www.lemonde.fr/les-decodeurs/article/2024/07/01/la-carte-des-resultats-des-legislatives-au-premier-tour-et-le-tableau-des-candidats-qualifies_6245574_4355771.html"
    driver.get(URL)

    res = []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    for candidate_list in soup.find_all("div", class_=["candidat bordure"]):
        candidate = candidate_list.find("span", class_=["barre"])
        if candidate is not None:
            res.append(BeautifulSoup(str(candidate).replace("\xa0", " "), "html.parser").text)

    print(res)
    print(len(res))

    driver.quit()

    return res

def addDesistements(excel_file: pd.DataFrame, candidate_desistement_list: list):
    writer = pd.ExcelWriter("lg2024-resultats-circonscriptions-une-ligne-par-candidat2.xlsx", mode = 'a', if_sheet_exists="overlay")

    desistements = ["NON"]*4009
    nb_desis = 0
    candidate_desistement_list_copy = candidate_desistement_list.copy()


    for candidate in candidate_desistement_list:
        candidate_name = candidate.split(" ", 1)
        for i in range(4009):
            if excel_file["NomPsn"][i].lower() == candidate_name[1].lower() and excel_file["PrenomPsn"][i].lower() == candidate_name[0].lower():
                desistements[i] = "OUI"
                nb_desis += 1
                candidate_desistement_list_copy.remove(candidate)
    

    df = pd.DataFrame(list(zip(desistements)), columns=["desistement"])
    print(df, nb_desis, candidate_desistement_list_copy)

    df.to_excel(writer, sheet_name="Sheet1")
    writer.close()


