import re

from bs4 import BeautifulSoup
import requests
import shutil
import os



def manage_player(youthplayer_id):
    '''
    prende in input url di un giocatore e ne estrae le stelline ruolo per ruolo che verranno poi utilizzate per assemblare il csv

    :param youthplayer_id: youthplayerID del giocatore da analizzare
    :return: stelline ruolo per ruolo
    '''

    url = "https://stage.hattrick.org/Club/Players/YouthPlayer.aspx?YouthPlayerID="+str(youthplayer_id)
    print(url)
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")

    #print(soup)


    for line in str(soup).split("\n"):
        if "years".lower() in str(line) and "day".lower() in str(line):

            age = (re.findall("[1-2][0-9] years and [0-9]?[0-9]?[0-9]", line)[0])
            age_processed = str(age).replace(" years and ", "y")
            age_processed = str(age_processed.split("y")[0]) + "y" + str(age_processed.split("y")[1]).zfill(3)

            print(age_processed)
            #print(re.findall("[1-2][0-9] anni e [0-9]?[0-9][0-9] giorni", line))
        if "can be promoted".lower() in str(line).lower():
            #print(str(line))
            days_to_promo = 0
            try:

                #to_promo = (re.findall("Can be promoted in [0-9]?[0-9]?[0-9] days", line))
                #print("..."+to_promo+"...")
                to_promo = "".join(_ for _ in str((re.findall("Can be promoted in [0-9]?[0-9]?[0-9] days", line))[0]) if _ in "1234567890")
                print(to_promo)
                days_to_promo = str(to_promo)
            except:
                print("già promuovibile")

    #estraggo la tabelle
    for link in soup.find_all("table"):
        print("\n===\n")
        #print(link)
        #print("\n===\n")
        #ci son più tabelle. Prendo solo quella con i ruoli elencati, nella quale so per
        #certo che son presenti le stelline
        if "Central defender".lower() in link.text.lower()\
                and "date nowrap".lower() not in str(link):

            #dentro la tabella coi dati del giocatore cerco il tag td
            #che è quello dove sono "salvati" i dati delle prestazioni
            #ruolo per ruolo
            td_position_by_position = link.find_all("td")

            #parto da -.5 perchè nel td_position_by_position (sotto)
            #son presenti righe da saltare
            #il -.5 compensa l'offset.
            position_counter = -.5

            stars_gk = 0
            stars_cd = 0
            stars_wb = 0
            stars_im = 0
            stars_wg = 0
            stars_fw = 0

            for td in td_position_by_position:


                #se contiene la stringa "player-rating" significa che quel field contiene le stelline.
                #(offset citato prima causato dai td che nn contengono player-rating)
                if "player-rating" in str(td):


                    for el in td.find_all("div"):

                        #sono presenti due.
                        #seleziono quello senza "player-rating" per semplicita
                        #di elaborazione
                        if "stars-full" in str(el) and "player-rating" not in str(el):
                            #print("\n ### \n")
                            a=0
                            #prendo la stringa e seleziono solo numeri e separatore decimale (punto)
                            #print("".join(_ for _ in str(el) if _ in ".1234567890"))

                    #associo posizione a stelline in base al position_counter
                    if position_counter == 0:
                        #print("keeper")
                        stars_gk = "".join(_ for _ in str(el) if _ in ".1234567890")
                    if position_counter == 1:
                        #print("CD")
                        stars_cd = "".join(_ for _ in str(el) if _ in ".1234567890")
                    if position_counter == 2:
                        #print("WB")
                        stars_wb = "".join(_ for _ in str(el) if _ in ".1234567890")
                    if position_counter == 3:
                        #print("IM")
                        stars_im = "".join(_ for _ in str(el) if _ in ".1234567890")
                    if position_counter == 4:
                        #print("winger")
                        stars_wg = "".join(_ for _ in str(el) if _ in ".1234567890")
                    if position_counter == 5:
                        #print("forward")
                        stars_fw = "".join(_ for _ in str(el) if _ in ".1234567890")
                    #print("\n *** \n")
                position_counter += .5

    '''
    print("FINALE===")
    print("gk="+str(stars_gk))
    print("cd="+str(stars_cd))
    print("wb="+str(stars_wb))
    print("im="+str(stars_im))
    print("wg="+str(stars_wg))
    print("fw="+str(stars_fw))
    '''
    return str(stars_gk), str(stars_cd), str(stars_wb), str(stars_im), str(stars_wg), str(stars_fw), str(age_processed), str(days_to_promo)
def manage_team(id):
    '''
    dall'ID della squadra senior estrae ID squadra giovanile

    :param id: ID della squadra "senior"
    :return: ID della giovanile se esiste, altrimenti 0
    '''
    url = "https://stage.hattrick.org/Club/?TeamID="+str(id)
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    youth_club_id = 0
    for all in soup.find_all("a"):
        if "YouthTeamID".lower() in str(all).lower() and "?TeamID".lower() not in str(all).lower():
            #print(all)
            youth_club_id = "".join(_ for _ in str(all) if _ in "1234567890")

    #print(youth_club_id)
    return youth_club_id
def from_youth_team_get_youthplayerid_list(youthclubid):
    '''

    :param youthclubid: ID di una singola giovanile
    :return: lista degli ID dei giocatori di quella specifica squadra giovanile
    '''
    #entro direttamente alla pagina della lista dei giocatori

    list_of_youth_players = []

    url = "https://stage.hattrick.org/Club/Players/YouthPlayers.aspx?YouthTeamID=" + str(youthclubid)
    print(url)
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    for td in soup.find_all("td"):
        #print("\n===\n")
        #print(str(td))
        #print("\n===\n")
        if "hidden".lower() in str(td).lower() and "left".lower() not in str(td).lower():
            #print(str(td))
            youth_player_id = "".join(_ for _ in str(td) if _ in "1234567890")
            #print("---"+str(youth_player_id)+"---")
            list_of_youth_players.append(youth_player_id)
    return list_of_youth_players

def create_csv_string(youthplayer_id, stars_gk, stars_cd, stars_wb, stars_im, stars_wg, stars_fw, age, to_promo ):
    str_out = ""
    str_out += "http://www.hattrick.org/goto.ashx?path=/Club/Players/YouthPlayer.aspx?YouthPlayerID=" + str(youthplayer_id) + ";"
    str_out += str(age) + ";"
    str_out += str(to_promo) + ";"
    str_out += stars_gk + ";"
    str_out += stars_cd + ";"
    str_out += stars_wb + ";"
    str_out += stars_im + ";"
    str_out += stars_wg + ";"
    str_out += stars_fw

    return str_out

#manage_player("https://stage.hattrick.org/Club/Players/YouthPlayer.aspx?YouthPlayerID=299062182")


try:
    os.remove(".\lucatest.csv")
    shutil.copyfile(".\luca.csv", ".\lucatest.csv")
except:
    print("nada")

#shutil.copyfile(".\luca.csv", ".\lucatest.csv")
with open(".\luca.csv", "w") as file_out:
    with open(".\luca_top.csv", "w") as file_top_out:
        file_out.write("playerID;age;to_promo;GK;CD;WB;IM;WG;FW"+"\n")
        file_top_out.write("playerID;age;to_promo;GK;CD;WB;IM;WG;FW" + "\n")
        #file_out.write("ciao")

        with open(".\\team_list.txt", "r") as team_list:
            for line in team_list:
                print("..."+line.strip("\n")+"...")

                youthclub_id = manage_team(line.strip("\n"))
                youth_player_id_list = from_youth_team_get_youthplayerid_list(youthclub_id)

                for single_player in youth_player_id_list:
                    gk, cd, wb, im, wg, fw, age, to_promo = manage_player(single_player)
                    str_out = create_csv_string(single_player, gk, cd, wb, im, wg, fw, age, to_promo)


                    file_out.write(str_out+"\n")
                    if (
                        float(gk) >= 7 or
                            float(cd) >= 7 or
                            float(wb) >= 7 or
                            float(im) >= 7 or
                            float(wg) >= 7 or
                            float(fw) >= 7

                    ):
                        file_top_out.write(str_out+"\n")