import pandas as pd
from circoCalculator import calculate_all_winners
from circoUpdater import getDesistements, addDesistements

def main():
    excel_file = pd.read_excel("lg2024-resultats-circonscriptions-une-ligne-par-candidat2.xlsx", "Sheet1")

    candidate_desistements = getDesistements()
    addDesistements(excel_file, candidate_desistements)

    winners = calculate_all_winners(excel_file)

    print("")

    total = 0
    for party_winner in winners["party_winners"].keys():
        print(f"{party_winner} : {winners['party_winners'][party_winner]}")
        total += winners['party_winners'][party_winner]

    print("")

    for coalition_winner in winners["coalition_winners"].keys():
        print(f"{coalition_winner} : {winners['coalition_winners'][coalition_winner]}")

    print("")

    print(f"Total : {total}")


if __name__ == "__main__":
    main()