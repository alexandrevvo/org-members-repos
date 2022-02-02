import requests
import json
import argparse as ap
from dotenv import load_dotenv
import os

load_dotenv()

# proxies = {
#   "http": "http://127.0.0.1:8080",
#   "https": "https://127.0.0.1:8080",
# }

def get_org_repo_names(token, org):
	dados = []
	repo_names = []

	headers = {'content-type': 'application/json','Authorization': f"token {token}"}
	#TODO: Automatizar o tamanho do range (n. de páginas)
	for page in range (1,16):
		url= f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}"
		# r = requests.get(url, headers=headers, proxies=proxies, verify=False)
		r = requests.get(url, headers=headers)
		dados.append(r.json())


	for page in dados:
		for repo in page:
			# print(repo["name"])
			repo_names.append(repo["name"])

	return(repo_names)

def get_members_repos(token,org):

	headers = {'content-type': 'application/json','Authorization': f"token {token}"}
	dados = []
	members_repos = []
	#TODO: Automatizar o tamanho do range (n. de páginas)
	for page in range (1,5):
		url= f"https://api.github.com/orgs/{org}/members?per_page=100&page={page}"
		# r = requests.get(url, headers=headers, proxies=proxies, verify=False)
		r = requests.get(url, headers=headers)
		dados.append(r.json())

	#salvando a url de repositórios de cada membro da org.
	for page in dados:
		for member in page:
			# print(member["repos_url"])
			members_repos.append(member["repos_url"])

	clone_urls = []
	repo_names = []
	repos_dict = {}
	#Acessando a url de repos de cada membro, e salvando a clone_url de cada repo;
	for repos in members_repos:
		url = f"{repos}?per_page=100"
		# r = requests.get(url, headers=headers, proxies=proxies, verify=False)
		r = requests.get(url, headers=headers)
		repos_data = r.json()
		for repo in repos_data:
			# clone_urls.append(repo["clone_url"])
			# repo_names.append(repo["name"])
			repos_dict[repo["name"]] = repo["clone_url"]

	return(repos_dict)


if __name__=='__main__':



	parser = ap.ArgumentParser()
	parser.add_argument('-t','--token', help="Token de acesso à API do github, com permissões de acesso à ORG pesquisada.", required=True)
	parser.add_argument('-o','--org',help="Nome de organização no github",required=True)
	args = parser.parse_args()

	token = args.token
	
	#for local tests
	token = os.getenv("GITHUB_TOKEN")

	members_repos_dict = get_members_repos(token,args.org)
	org_repos = get_org_repo_names(token,args.org)

	# A intersecção tem o problema de ignorar quando mais de um user tem o repo da org. 
	# print(set(org_repos).intersection(members_repos))

	f = open("org_repos.txt", "w")
	f.write(json.dumps(org_repos))
	f.close()

	f = open("members_repos_dict.txt", "w")
	f.write(json.dumps(members_repos_dict))
	f.close()

	user_has_org_repo=[]
	for repo in org_repos:
		for key, val in members_repos_dict.items():
			if repo == key:
				user_has_org_repo.append(val)

	print(user_has_org_repo)
