import click, getpass, os, datetime, requests as re

main_api = "api/v1"
login_api = "auth/login"
secrets_api = ["secrets/create", "secrets/", "secrets/"]
users_api = ["users/register", "users/"]
TOKEN_FILE = ".env"
URL_MAIN = "http://voa.local"


def show_banner():
    username = os.getlogin()
    if username: usnm = " ".join([char for char in username.upper()])
    else: usnm = ""
    click.clear()
    click.echo(click.style(f"""
W E L C O M E   {usnm}   T O   V O A
    """, fg="cyan", bold=True))
    click.echo(click.style(f"Developer : SENANI DERRADJI", fg="red", bold=True, blink=True))
    click.echo(click.style("Version  : 1.0.0\n\n", fg="green", bold=True, blink=True))


@click.group()
def cli(): show_banner(); pass


@cli.command()
@click.option('-u', type=str , help='Your username')
@click.option('-p', type=str ,hide_input=True, help='Your password')
def login(u, p):
    username, password = u, p
    URL = f"{URL_MAIN}/{main_api}/{login_api}"
    if not username: username = input("Username: ")
    if not password: password = getpass.getpass("Password: ")
    
    payload = {"username": username, "password": password}
    response = re.post(URL, data=payload)

    if response.status_code == 200:
        click.echo(click.style("Login successful!", fg='green'))
        data = response.json()
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        if access_token and refresh_token:
            with open(TOKEN_FILE, 'w') as f: f.write(f"ACCESS_TOKEN={access_token}\n")

    else: click.echo(response.text)


def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f: content = f.read().strip(); return content[13:]
    else: click.echo(click.style("Please login first." ,fg="red")); return None


@cli.group()
def secrets(): pass


@secrets.command()
def list():
    URL = f"{URL_MAIN}/{main_api}/{secrets_api[1]}"
    access_token, headers = str(get_token()), {'Authorization': f'Bearer {access_token}'}

    response = re.get(URL, headers=headers)
    if response.status_code == 200:
        secrets = response.json()
        for secret in secrets:
            click.echo(click.style(f"Secret {secret['id']}\nName : {secret['name']}\nOwner ID : {secret['owner_id']}",fg="green"))
    else: click.echo(response.text)


@secrets.command()
@click.option("-n", prompt=True, help="Name of the secret")
@click.option("-v", prompt=True, help="Value of the secret")
def create(n, v):

    if not (n and v): click.echo(click.style("Please provide both name and value for the secret.",fg="red")); return

    if not n: n = click.prompt("Name of the secret", type=str)
    if not v: v = click.prompt("Value of the secret", type=str)

    URL = f"{URL_MAIN}/{main_api}/{secrets_api[0]}"
    access_token, headers = str(get_token()), {'Authorization': f'Bearer {access_token}'}
    payload = {"name": n, "value": v}

    try: response = re.post(URL, headers=headers, json=payload)
    except Exception as e: click.echo(click.style(f"An error occurred: {e}",fg="red")); return

    if response.status_code == 200: click.echo(click.style("Secret created successfully!",fg="green"))
    else: click.echo(response.text)


@secrets.command()
@click.option("--usec", type=int, help="ID of the secret to update")
@click.option("--dsec", type=int, help="ID of the secret to delete")
@click.option("--gsec", type=int, help="ID of the secret to get")
def manage(usec, dsec, gsec):
    if usec: URL = f"{URL_MAIN}/{main_api}/{secrets_api[1]}{usec}"
    elif dsec: URL = f"{URL_MAIN}/{main_api}/{secrets_api[1]}{dsec}"
    elif gsec: URL = f"{URL_MAIN}/{main_api}/{secrets_api[1]}{gsec}"

    access_token = str(get_token())
    headers = {'Authorization': f'Bearer {access_token}'}
    if usec:
        payload = {
            "name": click.prompt("New name", type=str, default=None),
            "value": click.prompt("New value", type=str, default=None),
            "environment": click.prompt("New environment", type=str, default=None)
        }
        response = re.put(URL, headers=headers, json=payload)
        if response.status_code == 200: click.echo(click.style(f"{usec} : Updated Successfully",fg="green"))
        else: click.echo(response.content)

    elif dsec:
        try: response = re.delete(URL, headers=headers)
        except Exception as e: click.echo(click.style(f"An error occurred: {e}",fg="red")); return
        if response.status_code == 200: click.echo(click.style(f"{dsec} : Deleted Successfully",fg="green"))
        else: click.echo(response.content)

    elif gsec:

        try: response = re.get(URL, headers=headers)
        except Exception as e: click.echo(click.style(f"An error occurred: {e}",fg="red")); return

        if response.status_code == 200:
            secret = response.json()
            click.echo(click.style(f"{secret['id']} : {secret['name']} : {secret['value']} : {secret['env']}",fg="green"))
        else: click.echo(response.content)
    else: click.echo(click.style("Please provide a valid option --usec, --dsec, --gsec ",fg="red"))


@cli.group()
def users(): pass


@users.command()
def list():
    URL = f"{URL_MAIN}/{main_api}/{users_api[1]}"
    access_token, headers = str(get_token()), {'Authorization': f'Bearer {access_token}'}

    try: response = re.get(URL, headers=headers)
    except Exception as e: click.echo(click.style(f"An error occurred: {e}",fg="red")); return

    if response.status_code == 200: 
        for user in response.json(): 
            click.echo(click.style(f"{user['id']} : {user['username']} : {user['role']}",fg="green"))
    else: click.echo(response.text)


@users.command()
@click.option('-u', prompt=True, help='Username for the new user')
@click.option('-p', prompt=True, hide_input=True, help='Password for the new user')
@click.option('-r', prompt=True, help='Role for the new user')
def create(u: str = "user", p: str = "password", r: str = "developer"):

    URL = f"{URL_MAIN}/{main_api}/{users_api[0]}"
    access_token, headers = str(get_token()), {'Authorization': f'Bearer {access_token}'}
    payload = {"username": u, "password": p, "role": r}

    try: response = re.post(URL, headers=headers, json=payload)
    except Exception as e: click.echo(click.style(f"An error occurred: {e}",fg="red")); return

    if response.status_code == 200: click.echo(click.style("User created successfully!",fg="green"))
    else: click.echo(response.text)


@users.command()
@click.option("--upuser", type=int, help="ID of the user to update")
@click.option("--deluser", type=int, help="ID of the user to delete")
def manage(upuser, deluser):
    if not any([upuser, deluser]):
        click.echo(click.style("Please provide a valid option --upuser, --deluser, or --getuser", fg="red"))
        return

    access_token = str(get_token())
    headers = {'Authorization': f'Bearer {access_token}'}

    if upuser:
        URL = f"{URL_MAIN}/{main_api}/{users_api[1]}{upuser}"
        payload = {
            "id": upuser,
            "username": click.prompt("New username", type=str, default=None),
            "password": click.prompt("New password", type=str, default=None),
            "role": click.prompt("New role", type=str, default=None)
        }
        try: response = re.put(URL, headers=headers, json=payload)
        except Exception as e: click.echo(click.style(f"An error occurred: {e}",fg="red")); return
        if response.status_code == 200: click.echo(click.style(f"User {upuser} updated successfully.",fg="green"))
        else: click.echo(response.text)

    elif deluser:
        URL = f"{URL_MAIN}/{main_api}/{users_api[1]}{deluser}"
        try: response = re.delete(URL, headers=headers)
        except Exception as e: click.echo(click.style(f"An error occurred: {e}", fg="red")); return
        if response.status_code == 200: click.echo(click.style(f"User {deluser} deleted successfully.",fg="green"))
        else: click.echo(response.text)

if __name__ == "__main__":
    cli()