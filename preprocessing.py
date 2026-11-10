import duckdb
import numpy
import pandas as pd

con = duckdb.connect()

flights = con.read_csv("data/flights.csv")
airports = con.read_csv("data/airports.csv")
airlines = con.read_csv("data/airlines.csv")
cancellations = con.read_csv("data/cancellation_codes.csv")

combo_data = con.sql("""
    WITH filtered_flights AS (
        SELECT *
        FROM flights
        WHERE CANCELLED = 0
    )
    SELECT
        f.* EXCLUDE (
            CANCELLED,
            CANCELLATION_REASON,
            AIR_SYSTEM_DELAY,
            SECURITY_DELAY,
            AIRLINE_DELAY,
            LATE_AIRCRAFT_DELAY,
            WEATHER_DELAY
        ),
        a.AIRPORT AS origin_airport_name,
        a.CITY AS origin_city,
        a.STATE AS origin_state,
        a.COUNTRY AS origin_country,
        a.LATITUDE AS origin_latitude,
        a.LONGITUDE AS origin_longitude,
        l.AIRLINE AS airline_name
    FROM filtered_flights AS f
    LEFT JOIN airports AS a
        ON f.ORIGIN_AIRPORT = a.IATA_CODE
    LEFT JOIN airlines AS l
        ON f.AIRLINE = l.IATA_CODE
""").df()

print(combo_data.head())