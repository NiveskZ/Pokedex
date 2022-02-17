#%%
from flask import Flask, render_template, request
import pokepy
import requests, json
#%%

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('homepage.html')

client_disk_cache = pokepy.V2Client(cache='in_disk', cache_location='./temp')
# gets all pokemon names and put in a list
poke_names = ['wormadam']
for global_pokedex_id in range(1,899):
    pokemon = client_disk_cache.get_pokemon(global_pokedex_id)
    poke_names.append(pokemon.name)

#%%
# get the name and url from all location areas in pokemon games
endpoint = 'https://pokeapi.co/api/v2/location-area/?offset=0&limit=702'

r = requests.get(endpoint)
locationData = json.loads(r.text)
locatData = locationData['results']

# get all location areas id and put the ids in a list
local_area_ids = []
for i in range(0,9):
    l_id = locatData[i]['url'][-2:-1]
    local_area_ids.append(l_id)
for i in range(9,67):
    l_id = locatData[i]['url'][-3:-1]
    local_area_ids.append(l_id)
for i in range(67,702):
    l_id = locatData[i]['url'][-4:-1]
    local_area_ids.append(l_id)

#%%
# get all location area names
local_area_names = []
for area in local_area_ids:
    local_area_names.append(client_disk_cache.get_location_area(area).name)
#%%

@app.route('/location-area', methods=['GET'])
def location_area():
    # receive a location area name
    global_location_area = request.values.get('location-area').lower().replace(' ', '-')

    # creating variables
    l_area = None

    # create a list that will have all pokemons in the requesting area
    pokemon_names = []
    pokemon_id_by_name = {}

    # sees if the location area exists and gets all infos from it
    if global_location_area in local_area_names:
        l_area = client_disk_cache.get_location_area(global_location_area)
        
        for i in range(len(l_area.pokemon_encounters)):
            pokemon_names.append(l_area.pokemon_encounters[i].pokemon.name)
        for pokemon_name in pokemon_names:
            pokemon_id_by_name[pokemon_name] = client_disk_cache.get_pokemon(pokemon_name).id


    # returns an error message
    else:
        err = " This area doesn't exist. \n  Location area name must be specific."
        err = err.replace("\n", "<br>")

        return render_template('erro.html', err=err)

    return render_template('location.html', l_area = l_area, pokemon_names=pokemon_names, pokemon_id_by_name = pokemon_id_by_name)


@app.route('/pokemon', methods=['GET'])
def poke_name():
    
    client_disk_cache = pokepy.V2Client(cache='in_disk', cache_location='./temp')

    global_pokedex_id = request.values.get('pokemon').lower().replace(' ','-')

    poke = None
    poke_species = None
    err = ''

    # check if the global_pokedex_id exists
    #if not global_pokedex_id:
    #    err = err + "The global pokedex id wasn't defined. \n"

    # check if the global_pokedex_id is an integer

    if global_pokedex_id not in poke_names:

        try:
            global_pokedex_id = int(global_pokedex_id)

            if global_pokedex_id not in range(1,899):
                err = err + "Global pokedex id is not in range, the maximum is 898. \n"
                return render_template('erro.html', err=err)

        except ValueError:
            err = "There is no pokemon with this name"


        except TypeError:
            err = "Try a Pokemon name or a pokemon id between 1-898"

    if err:
        err = err.replace("\n", "<br>")

    else:
        if global_pokedex_id == 'wormadam-plant' or global_pokedex_id == 'wormadam':
            global_pokedex_id = 'wormadam-plant'
            poke = client_disk_cache.get_pokemon(global_pokedex_id)
            poke.name = 'wormadam'
            poke_species = client_disk_cache.get_pokemon_species(poke.name)

        else:

            poke = client_disk_cache.get_pokemon(global_pokedex_id)
            poke_species = client_disk_cache.get_pokemon_species(global_pokedex_id)

    return render_template('index.html', err=err, poke=poke, poke_species=poke_species)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

