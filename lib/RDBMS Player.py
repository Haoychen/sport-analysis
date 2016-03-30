__author__ = 'voelunteer'
import xml.dom.minidom
import sqlite3 as lite
DomTree = xml.dom.minidom.parse('srml-98-2012-squads.xml')
DomData = DomTree.documentElement
timestamp = DomData.getAttribute('timestamp')
SoccerDocument = DomData.getElementsByTagName('SoccerDocument')
con = lite.connect('soccer.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Player_Data_Information(timestamp TEXT)")
    try:
        cur.execute("INSERT INTO Player_Data_Information VALUES(?);", (timestamp,))
    except:
        pass
    con.commit()

season_id = SoccerDocument[0].getAttribute('season_id')
Teams = SoccerDocument[0].getElementsByTagName('Team')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Country_Information(country_id INT PRIMARY KEY UNIQUE, country TEXT, country_iso TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Region_Information(region_id INT PRIMARY KEY UNIQUE, region_name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Team_Information_Detail(team_id INT PRIMARY KEY UNIQUE, season_id INT, country_id INT, region_id INT, found_time INT)")
    con.commit()

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Player_vs_Team(player_id INT, team_id INT, season_id INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Player_Stat(player_id INT, season_id INT, name TEXT, position TEXT, first_name TEXT, last_name TEXT, birth_date TEXT, birth_place TEXT, first_nationality TEXT, weight INT, height INT, jersey_num INT, real_position TEXT, real_position_side TEXT, join_date TEXT, leave_date TEXT, new_team TEXT, country TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Official_Information(official_id INT, season_id INT, team_id INT, first_name TEXT, last_name TEXT, position TEXT, country TEXT, birthday TEXT, birthplace TEXT, join_date TEXT, leave_date TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Stadium_Infomation(Statium_id INT PRIMARY KEY UNIQUE, team_id INT, season_id INT, stadium_name TEXT, capacity INT)")
    con.commit()

for team in Teams:
    country = team.getAttribute('country')
    country_id = team.getAttribute('country_id')
    country_iso = team.getAttribute('country_iso')
    region_id = team.getAttribute('region_id')
    region_name = team.getAttribute('region_name')
    team_id = team.getAttribute('uID')[1:]
    found_time = team.getElementsByTagName('Founded')
    try:
        found_time = found_time[0].firstChild.data
    except:
        found_time = ''
    with con:
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO TEAM_Information_Detail VALUES(?, ?, ?, ?, ?);", (team_id, season_id, country_id, region_id, found_time))
        except:
            pass
        con.commit()
    with con:
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO Country_Information VALUES(?, ?, ?);",(country_id, country, country_iso))
        except:
            pass
        con.commit()
    with con:
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO Region_Information VALUES(?, ?);",(region_id, region_name))
        except:
            pass
        con.commit()
    Players = team.getElementsByTagName('Player')
    for player in Players:
        player_id = player.getAttribute('uID')[1:]
        name = player.getElementsByTagName('Name')
        try:
            name = name[0].firstChild.data
        except:
            name = ''
        position = player.getElementsByTagName('Position')
        try:
            position = position[0].firstChild.data
        except:
            position = ''
        stats = player.getElementsByTagName('Stat')
        types = {}
        for stat in stats:
            type = stat.getAttribute('Type')
            try:
                type_value = stat.firstChild.data
            except:
                type_value = ''
            types[type] = type_value
        try:
            first_name = types['first_name']
        except:
            firt_name = ''
        try:
            last_name = types['last_name']
        except:
            last_name = ''
        try:
            birth_date = types['birth_date']
        except:
            birth_date = ''
        try:
            birth_place = types['birth_place']
        except:
            birth_place = ''
        try:
            first_nationality = types['first_nationality']
        except:
            first_nationality = ''
        try:
            weight = types['weight']
        except:
            weight = ''
        try:
            height = types['height']
        except:
            height = ''
        try:
            jersey_num = types['jersey_num']
        except:
            jersey_num = ''
        try:
            real_position = types['real_position']
        except:
            real_position = ''
        try:
            real_position_side = types['real_position_side']
        except:
            real_position_side = ''
        try:
            join_date = types['join_date']
        except:
            join_date = ''
        try:
            leave_date = types['leave_date']
        except:
            leave_date = ''
        try:
            new_team = types['new_team']
        except:
            new_team = ''
        country = types['country']

        with con:
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO Player_vs_Team VALUES(?, ?, ?);",(player_id, team_id, season_id))
            except:
                pass
            con.commit()

        with con:
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO Player_Stat VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",(player_id, season_id, name, position, first_name, last_name, birth_date, birth_place, first_nationality, weight, height, jersey_num, real_position, real_position_side, join_date, leave_date, new_team, country))
            except:
                pass
            con.commit()

    team_officials = team.getElementsByTagName('TeamOfficial')
    for team_official in team_officials:
        official_position = team_official.getAttribute('Type')
        official_country = team_official.getAttribute('country')
        official_id = team_official.getAttribute('uID')
        official_name = team_official.getElementsByTagName('PersonName')[0]
        try:
            official_birthday = official_name.getElementsByTagName('BirthDate')[0].firstChild.data
        except:
            official_birthday = ''
        try:
            official_birthplace = official_name.getElementsByTagName('BirthPlace')[0].firstChild.data
        except:
            official_birthplace = ''
        official_first_name = official_name.getElementsByTagName('First')[0].firstChild.data
        official_last_name = official_name.getElementsByTagName('Last')[0].firstChild.data
        official_join_date = official_name.getElementsByTagName('join_date')[0].firstChild.data
        try:
            official_leave_date = official_name.getElementsByTagName('leave_date')[0].firstChild.data
        except:
            pass
        with con:
            cur = con.cursor()
            try:
                print(official_birthplace)
                cur.execute("INSERT INTO Official_Information VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",(official_id, season_id, team_id, official_first_name, official_last_name, official_position, official_country, official_birthday, official_birthplace, official_join_date, official_leave_date))
            except:
                print('error')
                pass
            con.commit()

    stadium = team.getElementsByTagName('Stadium')
    try:
        stadium_id = stadium[0].getAttribute('uID')
    except:
        stadium_id = ''
    try:
        stadium_name = stadium[0].getElementsByTagName('Name')[0].firstChild.data
    except:
        stadium_name =  ''
    try:
        stadium_capacity = stadium[0].getElementsByTagName('Capacity')
    except:
        stadium_capacity = ''
    try:
        stadium_capacity = stadium_capacity[0].firstChild.data
    except:
        stadium_capacity = ''


    with con:
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO Stadium_Infomation VALUES(?, ?, ?, ?, ?);",(stadium_id, season_id, team_id, stadium_name, stadium_capacity))
        except:
            pass
        con.commit()