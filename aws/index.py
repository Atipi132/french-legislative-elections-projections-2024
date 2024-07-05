import json
import base64
from circoCalculator import calculate_all_winners
import pandas as pd

def get_winners_as_json_res(options: str) -> dict:
    excel_file = pd.read_excel("lg2024-resultats-circonscriptions-une-ligne-par-candidat2.xlsx", "Sheet1")
    print("excel_file opened")

    # candidate_desistements = getDesistements()
    # addDesistements(excel_file, candidate_desistements)

    winners = calculate_all_winners(excel_file)

    # print("")

    # total = 0
    # for party_winner in winners["party_winners"].keys():
    #     print(f"{party_winner} : {winners['party_winners'][party_winner]}")
    #     total += winners['party_winners'][party_winner]

    # print("")

    # for coalition_winner in winners["coalition_winners"].keys():
    #     print(f"{coalition_winner} : {winners['coalition_winners'][coalition_winner]}")

    # print("")

    # print(f"Total : {total}")

    return winners

def handler(event, context):
    body = ""
    if event["isBase64Encoded"] == True:
        body = base64.b64decode(event["body"])
        print("body scraped")
    else:
        body = event["body"]
        # print(body)
    try:
        res = get_winners_as_json_res(json.loads(body))
        print("winners gotten")
    except Exception as e:
        # print(e)
        return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": f"An unexpected error occured : {str(e)}"
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(res)
    }