import requests

from utils import AnimeUtil

# Define the GraphQL endpoint
url = 'https://graphql.anilist.co'

# Base query for fetching anime details by ID
query_by_id = '''
query ($id: Int) {
  Media(id: $id, type: ANIME) {
    id
    title {
      romaji
      english
      native
    }
  }
}
'''

# Base query for fetching anime details by name
query_by_name = '''
query ($search: String) {
  Page {
    media(search: $search, type: ANIME) {
      id
      title {
        romaji
        english
        native
      }
    }
  }
}
'''


def get_anime_details_by_id(id):
    """Fetches anime details by ID from AniList API."""
    variables = {'id': id}
    response = requests.post(url, json={'query': query_by_id, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        return data['data']['Media']
    else:
        raise Exception(f"Query failed with status code {response.status_code}. {response.text}")


def get_anime_details_by_name(name):
    """Fetches anime details by name from AniList API."""
    variables = {'search': name}
    response = requests.post(url, json={'query': query_by_name, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        # Assuming the first result is the best match
        if data['data']['Page']['media']:
            return data['data']['Page']['media'][0]
        else:
            return None
    else:
        raise Exception(f"Query failed with status code {response.status_code}. {response.text}")


# Query to fetch detailed anime information by ID, including characters
query_detailed_info = '''
query ($id: Int) {
  Media(id: $id, type: ANIME) {
    id
    title {
      romaji
      english
      native
    }
    genres
    episodes
    averageScore
    startDate {
      year
      month
      day
    }
    endDate {
      year
      month
      day
    }
    description
    status
    coverImage {
      large
    }
    characters {
      edges {
        node {
          name {
            full
          }
        }
      }
    }
  }
}
'''


def get_anime_detailed_info_by_id(id):
    """Fetches detailed information about an anime by ID from AniList API."""
    variables = {'id': id}
    response = requests.post(url, json={'query': query_detailed_info, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        anime_data = data['data']['Media']

        # Format release dates
        start_date = anime_data['startDate']
        end_date = anime_data['endDate']
        start_date_formatted = f"{start_date['year']}-{start_date['month']}-{start_date['day']}" if start_date else "N/A"
        end_date_formatted = f"{end_date['year']}-{end_date['month']}-{end_date['day']}" if end_date else "N/A"

        # Extract character names
        characters = [edge['node']['name']['full'] for edge in anime_data['characters']['edges']]

        # Return a dictionary with the detailed information
        return {
            'id': anime_data['id'],
            'title': anime_data['title'],
            'genres': anime_data['genres'],
            'episodes': anime_data['episodes'],
            'averageScore': anime_data['averageScore'],
            'startDate': start_date_formatted,
            'endDate': end_date_formatted,
            'description': anime_data['description'],
            'status': anime_data['status'],
            'coverImage': anime_data['coverImage']['large'],
            'characters': characters
        }
    else:
        raise Exception(f"Query failed with status code {response.status_code}. {response.text}")


# Query to fetch character details by ID
query_character_by_id = '''
query ($id: Int) {
  Character(id: $id) {
    id
    name {
      full
    }
    dateOfBirth {
      year
      month
      day
    }
    gender
    description
    image {
      large
    }
  }
}
'''

# Query to fetch character details by Name
query_character_by_name = '''
query ($name: String) {
  Character(search: $name) {
    id
    name {
      full
    }
    dateOfBirth {
      year
      month
      day
    }
    gender
    description
    image {
      large
    }
  }
}
'''


def get_character_details_by_id(id):
    """Fetches detailed information about a character by ID from AniList API."""
    variables = {'id': id}
    response = requests.post(url, json={'query': query_character_by_id, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        character_data = data['data']['Character']

        # Format birthdate
        birth_date = character_data['dateOfBirth']
        birth_date_formatted = f"{birth_date['year']}-{birth_date['month']}-{birth_date['day']}" if birth_date else "N/A"

        # Return a dictionary with the character details
        return {
            'name': character_data['name']['full'],
            'birthday': birth_date_formatted,
            'gender': character_data['gender'],
            'description': character_data['description'],
            'profileImage': character_data['image']['large']
        }
    else:
        raise Exception(f"Query failed with status code {response.status_code}. {response.text}")


def get_character_details_by_name(name):
    """Fetches detailed information about a character by Name from AniList API."""
    variables = {'name': name}
    response = requests.post(url, json={'query': query_character_by_name, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        character_data = data['data']['Character']

        # Format birthdate
        birth_date = character_data['dateOfBirth']
        birth_date_formatted = f"{birth_date['year']}-{birth_date['month']}-{birth_date['day']}" if birth_date else "N/A"

        # Return a dictionary with the character details
        return {
            'name': character_data['name']['full'],
            'birthday': birth_date_formatted,
            'gender': character_data['gender'],
            'description': character_data['description'],
            'profileImage': character_data['image']['large']
        }
    else:
        raise Exception(f"Query failed with status code {response.status_code}. {response.text}")


# Example usage:
if __name__ == "__main__":
    try:
        # anime_by_id = get_anime_details_by_id(15125)
        # print("Anime Details by ID:", anime_by_id)
        # 113813

        # file_path = "data/anime_history.json"

        # anime_util = AnimeUtil(file_path)

        # loaded_anime = anime_util.load_animes()
        #
        # anime_by_name = get_anime_details_by_name("Rent a girlfriend")
        # print("Anime Details by Name:", anime_by_name)

        # anime_details = get_anime_detailed_info_by_id(anime_by_name['id'])

        # print(anime_details)

        character = get_character_details_by_name("Chizuru Ichinose")

        print(character)

    except Exception as e:
        print(e)
