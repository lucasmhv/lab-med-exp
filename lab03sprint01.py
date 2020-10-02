from dotenv import load_dotenv, find_dotenv
import requests
import os
import json
import pandas

load_dotenv(find_dotenv())

def __query(primaryLanguage, num_repositories):
  query = f"""
  {{
    search(query: "stars:>0 primarylanguage:{primaryLanguage} sort:stars", type: REPOSITORY, first: {num_repositories}) {{
      pageInfo {{
        startCursor
        endCursor
        hasPreviousPage
        hasNextPage
      }}
      edges {{
        node {{
          ... on Repository {{
            nameWithOwner
            createdAt
            forkCount
            primaryLanguage {{
              name
            }}
            stargazers {{
              totalCount
            }}
            releases(first: 10) {{
              totalCount
              nodes {{
                publishedAt
              }}
            }}
          }}
        }}
      }}
    }}
  }}
  """
  return query

def get_repositories(primaryLanguage, num_repositories):
  token = os.getenv("TOKEN")
  headers = headers = {'Authorization': f'Bearer {token}'}
  repositories = list()
  query = __query(primaryLanguage, num_repositories)
  result = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)
  if result.status_code == 200:
      data = result.json()['data']['search']
      repositories = list(map(lambda x: x['node'], data['edges']))
      print(f"\rRetrieved {len(repositories)} repositories", end = '')
      return repositories 

print("Laboratory 3 - Sprint 01")
print("Get Java Repositories")
repositoriesJava = get_repositories("java", 100)
print("\nGet Python Repositories")
repositoriesPython = get_repositories("python", 100)
repositories = repositoriesJava + repositoriesPython
df = pandas.json_normalize(repositories)
csvText = df.to_csv().replace("\r", "")
filename = "lab03sprint01.csv"
print(f"\nRepositories saved on file {filename}")
file = open(filename, "w")
file.write(csvText)
file.close()
print("End")            
