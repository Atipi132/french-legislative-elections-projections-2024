import pandas as pd

def calculate_circo_winner(candidates: list[dict[str, str | int]], beaten_candidates: list[dict]) -> dict:
    """Calculates the potential winner for a specific district

    Parameters
    ----------
    candidates : list[dict[str, str | int]]
        The list of each canditate represented by a dictionary
    beaten_candidates : list[dict[str, str | int]]
        The list of each candidate beaten in the first round, represented by a dictionary

    Returns
    -------
    dict[str, str | int]
        the potential winner of the district in the 2nd round, represented by a dictionary
    """

    NFP_COALITION = {"Extrême gauche", "Union de la gauche", "Ecologistes", "Divers gauche", "Parti communiste français", "Parti socialiste", "La France insoumise", "Les Ecologistes", "Parti radical de gauche"}
    REN_COALITION = {"Ensemble ! (Majorité présidentielle)", "Divers", "Horizons", "Divers centre"}
    LR_COALITION = {"Les Républicains", "Union des Démocrates et Indépendants", "Divers droite", "Régionaliste"}
    RN_LR_COALITION = {"Rassemblement National", "Droite souverainiste", "Extrême droite", "Reconquête !", "Union de l'extrême droite"}

    nb_candidates_left = 0
    nb_candidates_center = 0
    nb_candidates_right = 0
    nb_candidates_far_right = 0

    for candidate in candidates:
        match candidate["nuance"]:
            case "Extrême gauche" | "Union de la gauche" | "Ecologistes" | "Divers gauche" | "Parti communiste français" | "Parti socialiste" | "La France insoumise" | "Les Ecologistes" | "Parti radical de gauche":
                nb_candidates_left += 1
            case "Rassemblement National" | "Droite souverainiste" | "Extrême droite" | "Reconquête !" | "Union de l'extrême droite":
                nb_candidates_far_right += 1
            case "Les Républicains" | "Union des Démocrates et Indépendants" | "Divers droite" | "Régionaliste":
                nb_candidates_right += 1
            case "Ensemble ! (Majorité présidentielle)" | "Divers"  | "Horizons" | "Divers centre":
                nb_candidates_center += 1

    sorted_candidates = []
    sorted_votes = sorted((candidate["NbVoix"] for candidate in candidates), reverse=True)
    for vote in sorted_votes:
        for candidate in candidates:
            if candidate["NbVoix"] == vote:
                sorted_candidates.append(candidate)
                break

    for beaten_candidate in beaten_candidates:
        if len(sorted_candidates) == 2:
            # cas voix de gauche et au moins un candidat NFP
            if beaten_candidate["nuance"] in NFP_COALITION and sorted_candidates[0]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de gauche et au moins un candidat NFP
            elif beaten_candidate["nuance"] in NFP_COALITION and sorted_candidates[1]["nuance"] in NFP_COALITION:
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de gauche et candidats ENS/LR et RN
            elif beaten_candidate["nuance"] in NFP_COALITION and sorted_candidates[0]["nuance"] in REN_COALITION | LR_COALITION and sorted_candidates[1]["nuance"] in RN_LR_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.465
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.035
            # cas voix de gauche et candidats RN et ENS/LR
            elif beaten_candidate["nuance"] in NFP_COALITION and sorted_candidates[1]["nuance"] in REN_COALITION | LR_COALITION and sorted_candidates[0]["nuance"] in RN_LR_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.035
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.465

            # cas voix de centre et au moins un candidat ENS/LR
            elif beaten_candidate["nuance"] in REN_COALITION and sorted_candidates[0]["nuance"] in REN_COALITION | LR_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de centre et au moins un candidat ENS/LR
            elif beaten_candidate["nuance"] in REN_COALITION and sorted_candidates[1]["nuance"] in REN_COALITION | LR_COALITION:
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de centre et candidats RN et NFP
            elif beaten_candidate["nuance"] in REN_COALITION and sorted_candidates[0]["nuance"] in RN_LR_COALITION and sorted_candidates[1]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.12
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.30
            # cas voix de centre et candidats NFP et RN
            elif beaten_candidate["nuance"] in REN_COALITION and sorted_candidates[1]["nuance"] in RN_LR_COALITION and sorted_candidates[0]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.30
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.12

            # cas voix de droite et au moins un candidat LR
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[0]["nuance"] in LR_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de droite et au moins un candidat LR
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[1]["nuance"] in LR_COALITION:
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de droite et candidats RN et NFP
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[0]["nuance"] in RN_LR_COALITION and sorted_candidates[1]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.70
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.30
            # cas voix de droite et candidats NFP et RN
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[1]["nuance"] in RN_LR_COALITION and sorted_candidates[0]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.30
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.70
            # cas voix de droite et candidats RN et ENS
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[0]["nuance"] in RN_LR_COALITION and sorted_candidates[1]["nuance"] in REN_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.31
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.61
            # cas voix de droite et candidats ENS et RN
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[1]["nuance"] in RN_LR_COALITION and sorted_candidates[0]["nuance"] in REN_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.31
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.61
            # cas voix de droite et candidats ENS et NFP
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[0]["nuance"] in REN_COALITION and sorted_candidates[1]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.92
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.08
            # cas voix de droite et candidats NFP et ENS
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[1]["nuance"] in REN_COALITION and sorted_candidates[0]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.08
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.92

            # cas voix de extrême-droite et au moins un candidat RN/LR
            elif beaten_candidate["nuance"] in RN_LR_COALITION and sorted_candidates[0]["nuance"] in RN_LR_COALITION | LR_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de extrême-droite et au moins un candidat RN/LR
            elif beaten_candidate["nuance"] in RN_LR_COALITION and sorted_candidates[1]["nuance"] in RN_LR_COALITION | LR_COALITION:
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de extrême-droite et candidats ENS et NFP
            elif beaten_candidate["nuance"] in RN_LR_COALITION and sorted_candidates[0]["nuance"] in REN_COALITION and sorted_candidates[1]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.68
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.32
            # cas voix de extrême-droite et candidats NFP et ENS
            elif beaten_candidate["nuance"] in RN_LR_COALITION and sorted_candidates[1]["nuance"] in REN_COALITION and sorted_candidates[0]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.32
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.68

        elif len(sorted_candidates) == 3:
            # cas voix de gauche et au moins un candidat NFP
            if beaten_candidate["nuance"] in NFP_COALITION and sorted_candidates[0]["nuance"] in NFP_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
            # cas voix de gauche et au moins un candidat NFP
            elif beaten_candidate["nuance"] in NFP_COALITION and sorted_candidates[1]["nuance"] in NFP_COALITION:
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
            # cas voix de gauche et au moins un candidat NFP
            elif beaten_candidate["nuance"] in NFP_COALITION and sorted_candidates[2]["nuance"] in NFP_COALITION:
                sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
            # cas voix de gauche et candidat RN en tête sans candidat NFP
            elif beaten_candidate["nuance"] in NFP_COALITION and sorted_candidates[0]["nuance"] in RN_LR_COALITION:
                if sorted_candidates[1]["nuance"] in REN_COALITION:
                    sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.07*0.75
                    sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.93*0.75
                else:
                    sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.465*0.75
                    sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.465*0.75

            # cas voix de centre et au moins un candidat ENS/ LR en tête
            elif beaten_candidate["nuance"] in REN_COALITION and sorted_candidates[0]["nuance"] in REN_COALITION | LR_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
            # cas voix de centre et au moins un candidat ENS
            elif beaten_candidate["nuance"] in REN_COALITION and sorted_candidates[1]["nuance"] in REN_COALITION:
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
            # cas voix de centre et au moins un candidat ENS
            elif beaten_candidate["nuance"] in REN_COALITION and sorted_candidates[2]["nuance"] in REN_COALITION:
                sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
            # cas voix de centre et candidat NFP en tête sans candidat ENS
            elif beaten_candidate["nuance"] in REN_COALITION and sorted_candidates[0]["nuance"] in NFP_COALITION:
                if sorted_candidates[1]["nuance"] in LR_COALITION:
                    sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
                else:
                    sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.67*0.75
                    sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.33*0.75
            # cas voix de centre et candidat RN en tête sans candidat ENS
            elif beaten_candidate["nuance"] in REN_COALITION and sorted_candidates[0]["nuance"] in RN_LR_COALITION:
                if sorted_candidates[1]["nuance"] in LR_COALITION:
                    sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
                else:
                    sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.50*0.75
                    sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.50*0.75

            # cas voix de droite et au moins un candidat LR
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[0]["nuance"] in LR_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de droite et au moins un candidat LR
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[1]["nuance"] in LR_COALITION:
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de droite et au moins un candidat LR
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[2]["nuance"] in LR_COALITION:
                sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]
            # cas voix de droite et candidats NFP en tête
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[0]["nuance"] in NFP_COALITION:
                if sorted_candidates[1]["nuance"] in RN_LR_COALITION:
                    sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.70*0.75
                    sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.30*0.75
                else:
                    sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.70*0.75
                    sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.30*0.75
            # cas voix de droite et candidat NFP en deuxième position
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[1]["nuance"] in NFP_COALITION:
                if sorted_candidates[0]["nuance"] in RN_LR_COALITION:
                    sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.70*0.75
                    sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.30*0.75
                else:
                    sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.70*0.75
                    sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.30*0.75
            # cas voix de droite et candidat NFP en troisième position
            elif beaten_candidate["nuance"] in LR_COALITION and sorted_candidates[2]["nuance"] in NFP_COALITION:
                if sorted_candidates[0]["nuance"] in RN_LR_COALITION:
                    sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.70*0.75
                    sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.30*0.75
                else:
                    sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.70*0.75
                    sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.30*0.75

            # cas voix de extrême-droite et au moins un candidat RN_LR/LR
            if beaten_candidate["nuance"] in RN_LR_COALITION and sorted_candidates[0]["nuance"] in RN_LR_COALITION | LR_COALITION:
                sorted_candidates[0]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
            # cas voix de extrême-droite et au moins un candidat RN_LR/LR
            elif beaten_candidate["nuance"] in RN_LR_COALITION and sorted_candidates[1]["nuance"] in RN_LR_COALITION | LR_COALITION:
                sorted_candidates[1]["NbVoix"] += beaten_candidate["NbVoix"]*0.75
            # cas voix de extrême-droite et au moins un candidat RN_LR/LR
            elif beaten_candidate["nuance"] in RN_LR_COALITION and sorted_candidates[2]["nuance"] in RN_LR_COALITION | LR_COALITION:
                sorted_candidates[2]["NbVoix"] += beaten_candidate["NbVoix"]*0.75

    resorted_candidates = []
    sorted_votes = sorted((candidate["NbVoix"] for candidate in sorted_candidates), reverse=True)
    for vote in sorted_votes:
        for candidate in candidates:
            if candidate["NbVoix"] == vote:
                resorted_candidates.append(candidate)
                break    

    return resorted_candidates[0]


def calculate_all_winners(excel_file: pd.DataFrame) -> dict[str, dict[str, int]]:
    """Calculates the potential winner for every district

    Parameters
    ----------
    excel_file : pd.DataFrame
        The excel file taken from [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/resultats-du-1er-tour-des-elections-legislatives-2024-par-circonscription) with the added candidate withdrawals

    Returns
    -------
    dict[str, dict[str, int]]
        a dict representing :
            "party_winners" : a list representing the number of seats potentially won by every singular party
            "coalition_winners" : a list representing the number of seats potentially won by every coalition
    """

    NFP_COALITION = {"Extrême gauche", "Union de la gauche", "Ecologistes", "Divers gauche", "Parti communiste français", "Parti socialiste", "La France insoumise", "Les Ecologistes", "Parti radical de gauche"}
    REN_COALITION = {"Ensemble ! (Majorité présidentielle)", "Divers", "Horizons", "Divers centre"}
    LR_COALITION = {"Les Républicains", "Union des Démocrates et Indépendants", "Divers droite", "Régionaliste"}
    RN_LR_COALITION = {"Rassemblement National", "Droite souverainiste", "Extrême droite", "Reconquête !", "Union de l'extrême droite"}


    winners = {'Extrême gauche': 0, 'Rassemblement National': 0, 'Les Républicains': 0, 'Union de la gauche': 0, 'Droite souverainiste': 0, 'Ensemble ! (Majorité présidentielle)': 0, 'Extrême droite': 0, 'Divers': 0, 'Ecologistes': 0, 'Divers droite': 0, 'Reconquête !': 0, "Union de l'extrême droite": 0, 'Divers gauche': 0, 'Union des Démocrates et Indépendants': 0, 'Régionaliste': 0, 'Divers centre': 0, 'Horizons': 0, 'Parti communiste français': 0, 'Parti socialiste': 0, 'La France insoumise': 0, 'Les Ecologistes': 0, 'Parti radical de gauche': 0}
    coalition_winners = {"NFP": 0, "REN": 0, "LR": 0, "RN_LR": 0}
    current_candidates = []
    beaten_candidates = []
    
    n=0
    for i in range(4009):
        current_department = excel_file["Departement"][i]
        current_circo = excel_file["LibCirElec"][i]

        if excel_file["Elu"][i] in {"QUALIF T2", "OUI"} and excel_file["desistement"][i] == "NON":
            current_candidates.append({"nom": excel_file["NomPsn"][i] + excel_file["PrenomPsn"][i], "NbVoix": excel_file["NbVoix"][i], "nuance": excel_file["LibNuaCand"][i]})
        elif excel_file["Elu"][i] == "NON" or excel_file["desistement"][i] == "OUI":
            beaten_candidates.append({"nom": excel_file["NomPsn"][i] + excel_file["PrenomPsn"][i], "NbVoix": excel_file["NbVoix"][i], "nuance": excel_file["LibNuaCand"][i]})

        if excel_file["Departement"][(i+1)%4009] != current_department or excel_file["LibCirElec"][(i+1)%4009] != current_circo or i == 4008:
            winner = calculate_circo_winner(current_candidates, beaten_candidates)
            n += 1
            print(f"{n}/577 circonscription(s) terminée(s). Candidat gagant : {winner['nuance']}")
            winners[winner["nuance"]] += 1
            if winner["nuance"] in NFP_COALITION:
                coalition_winners["NFP"] += 1
            elif winner["nuance"] in REN_COALITION:
                coalition_winners["REN"] += 1
            elif winner["nuance"] in LR_COALITION:
                coalition_winners["LR"] += 1
            elif winner["nuance"] in RN_LR_COALITION:
                coalition_winners["RN_LR"] += 1
            current_candidates = []
            beaten_candidates = []

    return {"party_winners" : winners, "coalition_winners" : coalition_winners}