import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st


# ---------- Task 1 ----------
def scrape_pokemon_stats():
    url = "https://pokemondb.net/pokedex/stats/height-weight"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.select_one("table")
    rows = table.select("tbody tr")

    pokemons_clean = []
    for row in rows:
        image = row.select_one("img")["src"]
        cells = [td.get_text().strip() for td in row.select("td")]
        pokemons_clean.append([image] + cells)

    columns = [
        "Image", "Number", "Name", "Type",
        "Height (ft)", "Height (m)",
        "Weight (lbs)", "Weight (kg)", "BMI"
    ]

    df = pd.DataFrame(pokemons_clean, columns=columns)
    df["Height (m)"] = df["Height (m)"].astype(float)
    df["Weight (kg)"] = df["Weight (kg)"].astype(float)
    df[["Type 1", "Type 2"]] = df["Type"].str.split(" ", n=1, expand=True)

    return df[[
        "Image", "Number", "Name", "Type",
        "Height (m)", "Weight (kg)", "BMI",
        "Type 1", "Type 2"
    ]]


# ---------- Streamlit Page ----------
def main():
    st.title("Pokemon Stats")

    df = scrape_pokemon_stats()

    st.write(f"Loaded {len(df)} Pokémon statistics.")
    st.dataframe(df.head())


if __name__ == "__main__":
    main()
