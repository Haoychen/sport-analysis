__author__ = 'voelunteer'

import xml.dom.minidom
import sqlite3 as lite
import glob

for doc_name in glob.glob('*.xml'):
    DomTree = xml.dom.minidom.parse(doc_name)
    DomData = DomTree.documentElement
    Game = DomData.getElementsByTagName('Game')
    game_id = Game[0].getAttribute('id')
    timestamp = DomData.getAttribute('timestamp')
    con = lite.connect('soccer.db')

    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Data_Information(id INT PRIMARY KEY UNIQUE, timestamp TEXT)")
        try:
            cur.execute("INSERT INTO Data_Information VALUES(?,?);", (game_id, timestamp))
        except:
            pass
        con.commit()

    season_id = Game[0].getAttribute('season_id')
    season_name = Game[0].getAttribute('season_name')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Season_Information(season_ID INT PRIMARY KEY UNIQUE, season_name TEXT)")
        try:
            cur.execute("INSERT INTO Season_Information VALUES(?, ?);",(season_id, season_name))
        except:
            pass
        con.commit()

    away_team_id = Game[0].getAttribute('away_team_id')
    away_team_name = Game[0].getAttribute('away_team_name')
    home_team_id = Game[0].getAttribute('home_team_id')
    home_team_name = Game[0].getAttribute('home_team_name')

    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Team_Information(team_id INT PRIMARY KEY UNIQUE, team_name TEXT)")
        try:
            cur.execute("INSERT INTO Team_Information VALUES(?, ?);",(away_team_id, away_team_name))
        except:
            pass
        try:
            cur.execute("INSERT INTO Team_Information VALUES(?, ?);",(home_team_id, home_team_name))
        except:
            pass
        con.commit()


    game_date = Game[0].getAttribute('game_date')
    game_date = game_date.split('T')[0]
    period_1_start = Game[0].getAttribute('period_1_start')
    period_1_start = period_1_start.split('T')[1]
    period_2_start = Game[0].getAttribute('period_2_start')
    period_2_start = period_2_start.split('T')[1]

    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Competition_Information(id INT PRIMARY KEY UNIQUE, away_team_id INT, home_team_id INT, season_id INT, game_date TEXT, period_1_start TEXT, perior_2_start TEXT)")
        try:
            cur.execute("INSERT INTO Competition_Information VALUES(?, ?, ?, ?, ?, ?, ?);",(game_id, away_team_id, home_team_id, season_id, game_date, period_1_start, period_2_start))
        except:
            pass
        con.commit()


    Events = Game[0].getElementsByTagName('Event')

    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Event_Information(id INT PRIMARY KEY UNIQUE, game_id INT, event_id INT, type_id INT, period_id INT, min INT, sec INT, player_id INT, team_id INT, outcome INT, x REAL, y REAL, keypass INT, timestamp TEXT, last_modified TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS Q_Information(Q_id INT PRIMARY KEY UNIQUE, event_id INT, qualified_id INT, value TEXT)")
        con.commit()


    for event in Events:
        a_event_id = event.getAttribute('id')
        event_id = event.getAttribute('event_id')
        type_id = event.getAttribute('type_id')
        period_id = event.getAttribute('period_id')
        min = event.getAttribute('min')
        sec = event.getAttribute('sec')
        team_id = event.getAttribute('team_id')
        player_id = event.getAttribute('player_id')
        outcome = event.getAttribute('outcome')
        x = event.getAttribute('x')
        y = event.getAttribute('y')
        keypass = event.getAttribute('keypass')
        timestamp = event.getAttribute('timestamp')
        last_modified = event.getAttribute('last_modified')
        with con:
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO Event_Information VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",(a_event_id,  game_id, event_id, type_id, period_id, min, sec, player_id, team_id, outcome, x, y, keypass, timestamp, last_modified))
            except:
                pass
            con.commit()
        Qs = event.getElementsByTagName('Q')
        for Q in Qs:
            Q_id = Q.getAttribute('id')
            qualifier_id = Q.getAttribute('qualifier_id')
            value = Q.getAttribute('value')
            with con:
                cur = con.cursor()
                try:
                    cur.execute("INSERT INTO Q_Information VALUES(?, ?, ?, ?);",(Q_id, a_event_id, qualifier_id, value))
                except:
                    pass