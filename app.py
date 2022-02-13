from flask import Flask, render_template, request
import pokepy
import requests


app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('homepage.html')

@app.route('/pokemon', methods=['GET'])
def poke_name():
    client_disk_cache = pokepy.V2Client(cache='in_disk', cache_location='./temp')

    global_pokedex_id = request.values.get('pokemon')
    err = ''

    poke = None
    char = None
    poke_species = None

    # check if the global_pokedex_id exists
    #if not global_pokedex_id:
    #    err = err + "The global pokedex id wasn't defined. \n"

    # check if the global_pokedex_id is an integer
    try:
        global_pokedex_id = int(global_pokedex_id)

        if global_pokedex_id not in range(1,898):
            err = err + "Global pokedex id is not in range, the maximum is 898. \n"
            return render_template('erro.html', err=err)

    except ValueError:
        if global_pokedex_id:
            global_pokedex_id 
    except TypeError:
        err = "Try a Pokemon name or a pokemon id between 1-898"

    if err:
        err = err.replace("\n", "<br>")

    else:
        poke = client_disk_cache.get_pokemon(global_pokedex_id)
        poke_species = client_disk_cache.get_pokemon_species(global_pokedex_id)

    return render_template('index.html', err=err, poke=poke, char=char, poke_species=poke_species)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')