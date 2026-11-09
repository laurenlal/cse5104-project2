import pandas as pd
import duckdb

con = duckdb.connect()

flights = con.read_csv('data/flights.csv')
airports = con.read_csv('data/airports.csv')
airlines = con.read_csv('data/airlines.csv')
cancellations = con.read_csv('data/cancellation_codes.csv')

combo_data = con.sql("""

with filter as (
    SELECT * FROM flights
    WHERE Cancelled = 0 
), 

SELECT f.* exclude (cancelled, cancellation_reason, air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay),
           a.Airport as origin_airport,
           a.city as origin_city,
           a.state as origin_state,
           a.country as origin_country,
           a.latitude as origin_latitude,
           a.longitude as origin_longitude,
           l.Airline as airline,


    FROM filter f
    JOIN airports a ON f.ORIGIN_AIRPORT = a.IATA_CODE
    JOIN airlines l ON f.CARRIER = l.IATA_CODE

""")

cancellation_merge = con.sql(""" 
"""
)

print (combo_data)
