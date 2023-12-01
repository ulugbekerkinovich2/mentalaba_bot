# from aiogram import types
# from aiogram.dispatcher.filters.builtin import CommandStart
# import requests
# from loader import dp
#
import json


# def get_data():
#     url = "https://awards.gov.uz/api/api/v1/votation/result-by-average-score-home"
#     response = requests.get(url)
#     data = []
#
#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         raw_data = response.json()['data']
#
#         for team_data in raw_data:
#             team = {}
#             for i in range(1, 6):
#                 team[f'team_name_{i}'] = team_data[f'd{i}_team_name']
#                 team[f'score_{i}'] = team_data[f'd{i}_score']
#                 team[f'application_id_{i}'] = team_data[f'd{i}_application_id']
#                 team[f'votes_count_{i}'] = team_data[f'd{i}_votes_count']
#
#             data.append(team)
#
#     return data
#
# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     data = get_data()
#
#     # Selected teams filter
#     selected_teams = ['MenTalaba', 'Coozin', 'Lalu', 'Stepogram', 'Uztrip']
#     filtered_data = [team for team in data if any(team[f'team_name_{i}'] in selected_teams for i in range(1, 6))]
#
#     response_message = ""
#
#     for team in filtered_data:
#         team_info = (
#             f"\u2B50 Team: {team['team_name_1']} \n"
#             f"\U0001F3C6 Score: {team['score_1']} \n"
#             f"\U0001F4CA Votes count: {team['votes_count_1']} \n\n"
#         )
#         response_message += team_info
#
#     await message.answer(f"Salom, {message.from_user.full_name}!\n\n{response_message}")
import asyncio
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
from loader import dp

def get_data():
    url = "https://awards.gov.uz/api/api/v1/votation/result-by-average-score-home"
    response = requests.get(url)
    data = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        raw_data = response.json()['data']

        for team_data in raw_data:
            team = {}
            for i in range(1, 6):
                team[f'team_name_{i}'] = team_data[f'd{i}_team_name']
                team[f'score_{i}'] = team_data[f'd{i}_score']
                team[f'application_id_{i}'] = team_data[f'd{i}_application_id']
                team[f'votes_count_{i}'] = team_data[f'd{i}_votes_count']
            data.append(team)

    return data

async def send_data_to_channel(filtered_data, selected_teams):
    response_message = ""

    # Limit to send only 5 teams
    for team in filtered_data[:5]:
        for i in range(1, 6):
            # Check if the team is in the selected teams
            if team[f'team_name_{i}'] in selected_teams:
                team_info = (
                    f"\u2B50 Team: {team[f'team_name_{i}']} \n"
                    f"\U0001F3C6 Score: {team[f'score_{i}']} \n"
                    f"\U0001F4CA Votes count: {team[f'votes_count_{i}']} \n\n"
                )
                response_message += team_info

    # Send the message to the channel (replace CHANNEL_ID with your channel ID)
    message = await dp.bot.send_message(chat_id='-1002127522320', text=response_message)

    # Pin the last message
    await dp.bot.pin_chat_message(chat_id='-1002127522320', message_id=message.message_id)
async def periodic_task():
    while True:
        data = get_data()

        # Selected teams filter
        selected_teams = ['MenTalaba', 'Coozin', 'Lalu', 'Stepogram', 'Uztrip']
        filtered_data = [team for team in data if any(team[f'team_name_{i}'] in selected_teams for i in range(1, 6))]

        # Send the filtered data to the channel with selected teams
        await send_data_to_channel(filtered_data, selected_teams)

        # Sleep for two seconds (adjust as needed)
        await asyncio.sleep(60)

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # Start the periodic task
    asyncio.create_task(periodic_task())

    await message.answer(f"Salom, {message.from_user.full_name}! I will send you the data every two seconds.")

