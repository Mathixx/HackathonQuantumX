############################################
# 
# Here we create all necessary modules and methods that will help evaluating our model

RAPPEL : 
Nous exigeons que notre modèle nous réponde sous la forme d'un dictionnaire JSON.
Nous avons donc besoin de comparer les résultats de notre modèle avec les résultats attendus.
Pour cela, nous avons besoin de créer une fonction qui compare deux objets JSON et qui nous retourne un pourcentage de similarité entre les deux objets.

Chaque réponse de notre modèle doit avoir la forme suivante :
{
    "inquiry ": {
        "result": "..."
    }
}

############################################
from jsonschema import validate, ValidationError
import json 

# Define the schema
schema2 = {
    "type": "object",
    "properties": {
        "inquiry": {
            "type": "string",
            "enum": ["new_product", "feed_back", "details"]
        },
        "message": {
            "type": "string"
        },
        "list_of_proposals": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 5,
            "maxItems": 5
        }
    },
    "required": ["inquiry", "message", "list_of_proposals"]
}

schema1 = {
  "type": "object",
  "properties": {
    "category_abstract": {
      "type": "string",
      "description": "General category, e.g., 'electronics'"
    },
    "category_precise": {
      "type": "string",
      "description": "Specific category, e.g., 'smartphones'"
    },
    "max_price": {
      "type": "number",
      "minimum": 0,
      "description": "Maximum price (float or integer)"
    },
    "min_price": {
      "type": "number",
      "minimum": 0,
      "description": "Minimum price (float or integer)"
    },
    "min_rating": {
      "type": "number",
      "minimum": 0,
      "maximum": 5,
      "description": "Minimum acceptable rating (e.g., 4.5)"
    },
    "rating_count": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of ratings for the product or category"
    },
    "preference": {
      "type": "string",
      "enum": ["best_seller", "highest_rating", "cheapest", "most_popular"],
      "description": "User preference, e.g., 'best_seller', 'highest_rating'"
    }
  },
  "required": ["category_abstract", "category_precise", "max_price", "min_price", "min_rating", "rating_count", "preference"],
  "additionalProperties": false
}




def compare_json_objects(obj1, obj2):
    total_fields = 0
    identical_fields = 0
    common_keys = set(obj1.keys()) & set(obj2.keys())
    for key in common_keys:
        identical_fields += obj1[key] == obj2[key]
    percentage_identical = (identical_fields / max(len(obj1.keys()), 1)) * 100
    return percentage_identical