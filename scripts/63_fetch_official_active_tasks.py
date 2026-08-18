import requests
import json

query = """
{
  tasks {
    id
    name
    normalizedName
    trader {
      name
      normalizedName
    }
    map {
      name
      normalizedName
    }
    experience
    wikiLink
    taskRequirements {
      task {
        name
      }
    }
    objectives {
      id
      type
      description
      maps {
        name
        normalizedName
      }
      zones {
        id
        position {
          x
          y
          z
        }
        map {
          normalizedName
        }
      }
    }
  }
}
"""

headers = {"Content-Type": "application/json"}
try:
    r = requests.post("https://api.tarkov.dev/graphql", json={"query": query}, headers=headers, timeout=15)
    print("tarkov.dev API status:", r.status_code)
    if r.status_code == 200:
        data = r.json()
        tasks = data.get("data", {}).get("tasks", [])
        print(f"Successfully fetched {len(tasks)} ACTIVE OFFICIAL TASKS from tarkov.dev API!")
        with open("primary_data/tarkov_dev_api_tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
            
        # Check if 'BP depot' exists vs 'The Blood of War'
        bp_found = [t for t in tasks if "bp depot" in t["name"].lower()]
        bow_found = [t for t in tasks if "blood of war" in t["name"].lower()]
        print(f"BP Depot in official tasks: {len(bp_found)} -> {[t['name'] for t in bp_found]}")
        print(f"Blood of War in official tasks: {len(bow_found)} -> {[t['name'] for t in bow_found]}")
    else:
        print("API Response error:", r.text[:300])
except Exception as e:
    print("Error querying tarkov.dev GraphQL API:", e)
