import discord
import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup

url = 'https://www.fischerschule-hgw.de/vertretungsplan.html'
data = {
    'FORM_SUBMIT': 'tl_login_7',
    'username': os.getenv('username'),
    'password': os.getenv('password')
}
 

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print("Found username: " + os.getenv('username'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!Vertretungsplan'):
        response = requests.post(url, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')

        if response.status_code == 200:
            now = datetime.now()
            timestamp = now.strftime('%d.%m.%Y %H:%M').replace(':', '_')
            filename = f'Vertretungsplan {timestamp}.html'

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
                print(f'HTML file saved as "{filename}" successfully')

        # find all the sections with class "ce_accordion"
        sections = soup.find_all("section", class_="ce_accordion")

        # iterate over the sections and extract the relevant information
        output = ""
        for section in sections:
            # get the day of the week from the section header
            day = section.find("div", class_="toggler").text.strip()

            # get the table rows from the section content
            rows = section.find_all("tr")

            # check if there are rows for the current day
            if len(rows) > 1:  # header row is always present
                output += f"\n{day}:\n"
                output += "Klasse    |St. |Fach  |Lehrer                |Raum| Info \n"

                # iterate over the rows and extract the relevant information
                for row in rows[1:]:  # skip the header row
                    # check if the row has at least two columns
                    cells = row.find_all("td")
                    if len(cells) == 6:
                        # get the class, hour, subject, teacher, and info from the table cells
                        klass = cells[0].text.strip()
                        hour = cells[1].text.strip()
                        subject = cells[2].text.strip()
                        teacher = cells[3].text.strip()
                        classroom = cells[4].text.strip()
                        info = cells[5].text.strip()

                        # check if the row contains "10A" or "10B" in the klass variable
                        if "10A" in klass or "10A" in klass:
                            # format the information according to the desired output
                            output += f"{klass:<10}|{hour:<4}|{subject:<6}|{teacher:<22}|{classroom:<4}|{info}\n"


        # write the output to a file
        output_filename = f'Vertretungsplan {timestamp}.txt'
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(output)
            print(f'Text file saved as "{output_filename}" successfully')

        print(output)

        # send the output as a message
        await message.channel.send(f'```{output}```')


client.run(os.getenv('dc_token'))
