from os import getenv
from time import sleep

import requests
import os
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from projects.models import Project

load_dotenv()

class Command(BaseCommand):
    help = 'Fetches pinned repositories from github'

    def handle(self, *args, **kwargs):
        username = os.getenv('GITHUB_USERNAME')
        token = os.getenv('GITHUB_TOKEN')
        if not username and token:
            self.stdout.write(self.style.ERROR("Error: GITHUB_USERNAME and GITHUB_TOKEN missing"))
            return
        if not username:
            self.stdout.write(self.style.ERROR("Error: GITHUB_USERNAME missing"))
            return
        if not token:
            self.stdout.write(self.style.ERROR("Error: GITHUB_TOKEN missing"))
            return
        headers = {"Authorization": f"Token {token}"}
        # GraphQL Query to get Pinned Repos + README
        query = """
                {
                  user(login: "%s") {
                    pinnedItems(first: 6, types: REPOSITORY) {
                      nodes {
                        ... on Repository {
                          name
                          description
                          url
                          primaryLanguage {
                            name
                          }
                          object(expression: "HEAD:README.md") {
                            ... on Blob {
                              text
                            }
                          }
                        }
                      }
                    }
                  }
                }
                """ % username
        self.stdout.write(f"Fetching data for {username}...")
        response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Connection failed: {response.content}"))
            return

        data = response.json()

        if 'errors' in data:
            self.stdout.write(self.style.ERROR(f"GraphQL Error: {data['errors']}"))
            return

            # Wipe old data to keep it fresh
        Project.objects.all().delete()
        repos = data['data']['user']['pinnedItems']['nodes']

        if not repos:
            self.stdout.write(self.write.WARNING("No pinned repos founded"))
            return
        for repo in repos:
            lang = repo['primaryLanguage']['name'] if repo['primaryLanguage'] else "Code"

            #Get readme
            readme = repo['object']['text'] if repo['object'] else ""

            Project.objects.create(
                title=repo['name'],
                description=repo['description'] or "",
                technology=lang,
                github_url=repo['url'],
                readme_content=readme
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully imported: {repo['name']}"))
