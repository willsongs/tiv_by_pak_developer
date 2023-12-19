from functools import lru_cache

import telebot
import requests
import json
import math

from google.protobuf import message
from telebot import types
import multiprocessing

from urllib3.util import url

from save_user_data import initialize_database, save_user_info
from telebot import custom_filters

# testing:
# API_TOKEN = '5505287179:AAFu9iQ7jTeY8JM_KTN7hPe6oUawkYI195A'

# local testing:
API_TOKEN = '5252289753:AAEk5edcuo1ZTmvhWETeJa1qbEYA8kCeoi8'

bot = telebot.TeleBot(API_TOKEN)

initialize_database()


def send_msg(msg_id, msg):
    """send a message from this bot"""
    bot.send_message(msg_id, msg)


def done_common(call):
    """common logic for done functions"""
    closer_id = call.message.chat.id
    raw_text = call.message.text
    txtsplt = raw_text.split(',')
    u_id = txtsplt[1]
    mv_name = txtsplt[0]
    res = [u_id.strip(), mv_name.strip(), closer_id]
    print(u_id)
    return res


class SomethingWentWrongException(Exception):
    """Raises a something went wrong exception"""

    def __init__(self, id):
        """Initialize this class"""
        super().__init__("something went wrong")
        print("something went wrong")
        send_msg(id, "kuch glt ho gaya :(")


user_dict = {}

session = requests.session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko)'
                  'Chrome?58.0.3029.110 Safari/537.3'})


class User:
    def __init__(self, u_id):
        self.u_id = u_id
        self.c_id = self.c_id


import logging

# Configure logging to save outputs in a separate log file
logging.basicConfig(filename='bot.log', level=logging.INFO)
# Implement client-side caching using a deque with a maximum length of 3
client_cache = {}


def process_message_with_client_cache(message):
    term = message.text.split(' ', 1)[1]

    # Check if the term is in the client cache
    if term in client_cache:
        # Use cached result
        result = client_cache[term]
    else:
        # Perform the search and store the result in the cache
        result = search_videos(term)
        data = url.text
        parse_json = json.loads(data)

        n = len(parse_json['result'])
        if n == 0:
            result = 'The movie is not in the database right now. It will be added to the database soon.'
        else:
            # Process the result as before
            result = process_result(parse_json)

        # Store the result in the client cache
        client_cache[term] = result

    bot.reply_to(message, result)


# Implement server-side caching using LRU (Least Recently Used) caching
def process_result(parse_json):
    pass


@lru_cache(maxsize=8)
def search_videos(term):
    result = search_videos(term)
    data = url.text
    parse_json = json.loads(data)

    n = len(parse_json['result'])
    if n == 0:
        return 'The movie is not in the database right now. It will be added to the database soon.'
    else:
        # Process the result as before
        return process_result(parse_json)


@bot.message_handler(commands=["start"])
def start(message):
    try:
        user = message.from_user
        save_user_info(user.id, user.username, user.first_name, user.last_name, message.chat.id)
        print("user information saved")
        markup = types.ReplyKeyboardMarkup(row_width=2)
        bot.reply_to(message, 'okey! now enter any name of the movie or web series you want to watch today',
                     reply_markup=markup)
    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Handle the exception gracefully (e.g., send a user-friendly error message)
        bot.reply_to(message, 'An error occurred while processing your request. Please try again later.')


@bot.message_handler(commands=['broadcast'])
def inptmsg(message):
    try:
        msg = bot.send_message(message.chat.id, "ok. forward the message")
        bot.register_next_step_handler(msg, brdcst)
    except:
        send_msg(message.chat.id, "something went wrong")


def brdcst(message):
    li = [5017637541, 1884680252, 2086643719, 1132088975, 6001354337, 650526737, 5412171798, 2038568986, 1420959149,
          771104798, 1401487394, 2115387437, 5321390130, 2073854077, 490944563, 847065157, 1247244376, 1267757157,
          1101027437, 1655144559, 1915029649, 697915541, 1475965084, 1120870562, 2125181093, 641706152, 1437122138,
          1343926441, 5201195176, 1118116085, 1435912450, 1981280551, 5576388904, 5713416505, 1726406986, 5581549913,
          5238417770, 424702316, 5771962740, 973101443, 977457540, 343603589, 5674131852, 1255102869, 1967663517,
          1462913441, 1061046696, 359068078, 1918792133, 574640583, 510634455, 1246693853, 722846193, 5527331323,
          1256354327, 630141507, 5473604165, 1056201309, 1285773924, 1628340858, 471159435, 5528023700, 5274542741,
          1934545564, 5736026781, 5282304671, 5736680105, 5396751043, 1460234962, 1821434609, 2139099915, 5238782735,
          1297124119, 731956003, 1943296815, 1390644043, 430545756, 1468584801, 1164385133, 5391719303, 5790190484,
          5311226797, 2084510643, 2135346108, 1857729473, 641926083, 5192344517, 5379683287, 5003559897, 1228141528,
          1679915995, 5689000937, 5312674815, 782687241, 1802443787, 681776143, 1820167186, 1267741731, 1838896166,
          5736381493, 929901638, 1609858119, 933784663, 1161462874, 5525517403, 890649706, 1676205165, 694568077,
          5030063249, 5733762210, 1281346725, 759370926, 855203002, 1701541060, 987720913, 1317604562, 5466305749,
          778702037, 5341908195, 1301048550, 1731560683, 829990126, 987346159, 5209816313, 5446995254, 5373613372,
          1352537408, 5821943120, 903064914, 5193973136, 1705196959, 1638450592, 834321831, 638487981, 582935998,
          1411417547, 5430531562, 972666367, 576722445, 1325671955, 902090266, 2136598054, 702619189, 2017951293,
          5771642460, 1415976541, 1361747557, 774510189, 1954027121, 1674153587, 5310910092, 5517354647, 855084704,
          775003809, 5007693478, 1346647726, 555386549, 5500839609, 1086658235, 5794422483, 5358556886, 2017431256,
          523431652, 1966794472, 870708970, 1078718189, 5329135343, 5383866115, 5007888132, 5050343178, 1143265036,
          633917199, 5354372910, 5110597457, 1232121686, 599810758, 863108978, 1053366138, 2023399292, 1248608128,
          1468585856, 785244035, 1482579830, 982530027, 5196748789, 1311896473, 858382357, 5599076407, 1819887674,
          982564930, 5600493635, 1475541061, 5245173831, 5727662197, 5114824838, 5788340366, 1974755478, 5156436158,
          2127016131, 5508776161, 932174072, 599341304, 232884475, 1976264997, 1761634616, 1111243106, 52343165,
          5745451401, 5576438159, 5385320854, 5536405927, 5788068265, 5500484017, 1218834875, 1895602620, 1882149321,
          5606271442, 5722939869, 5657084406, 5482584625, 5585766963, 5579237941, 5775032898, 293638731, 1081848422,
          1498129034, 1888264847, 254292635, 5515326127, 1025727152, 948681400, 5632486075, 1537694413, 801907408,
          5177877203, 5426485973, 5782713047, 2086953730, 5845588743, 2129816329, 1492149002, 5730425612, 1336605464,
          5693135641, 1726970652, 1350871840, 5556693801, 5402071861, 856986424, 956037951, 1807160156, 501338986,
          5218947949, 1177430907, 999951228, 1908925338, 5297976220, 1157735340, 2061153196, 631899053, 835425210,
          1482718139, 1828205500, 1340154814, 1399419839, 5631200215, 5556800473, 986739677, 2105676772, 5668686835,
          1497990133, 1662213111, 5602886654, 5201179655, 5772559372, 2091217943, 1993047076, 1279063093, 5457527878,
          5775905882, 5525621858, 756679781, 5453036716, 2087378101, 1398838455, 5403174074, 862772235, 1224382979,
          5374676172, 617030862, 1807080667, 1767537884, 5357186272, 648164583, 2129667309, 5353661678, 2030214419,
          5253225769, 901596459, 5379470645, 5220007236, 344173903, 2134289757, 5799449973, 1927159177, 5060771212,
          5494316456, 1004488145, 759436754, 651730385, 1339037173, 1773293050, 843945508, 965049895, 1568214581,
          1283372600, 5113093711, 5766872660, 2034429531, 5568548482, 5694058137, 644968090, 1417162407, 9780904,
          1705565866, 1497442027, 924653314, 5603069707, 5776504592, 1717335825, 699318045, 5279596318, 2068815653,
          5951728434, 5539051302, 5414944558, 5429059391, 5094254405, 61253, 5841080141, 5072731983, 5586747218,
          5410754396, 5434101611, 5119131533, 5704742800, 1742606234, 5050224541, 5125296059, 5778200508, 671383508,
          1717022695, 5406912558, 5628694607, 1054425172, 1248465004, 1087365534, 1444676211, 1840503457, 933323488,
          5331522339, 1299591995, 5569969079, 1322806235, 1768203298, 5354091675, 5745229013, 1362953170, 5709092351,
          1551302223, 653854437, 5077598105, 5104535482, 660922340]
    # li = [2086643719, 650526737, 5412171798, 2038568986, 771104798, 1401487394, 2115387437, 5406912558, 5321390130, 490944563, 847065157, 5628694607, 1054425172, 1247244376, 1267757157, 1248465004, 1101027437, 1655144559, 1915029649, 697915541, 1475965084, 1120870562, 2125181093, 641706152, 1437122138, 1343926441, 5201195176, 640782547, 1118116085, 1435912450, 1981280551, 5576388904, 5713416505, 1726406986, 5581549913, 5238417770, 424702316, 5771962740, 973101443, 977457540, 343603589, 5674131852, 1255102869, 1967663517, 1087365534, 1462913441, 1061046696, 359068078, 1918792133, 574640583, 510634455, 1820774871, 1246693853, 722846193, 5527331323, 1256354327, 630141507, 5473604165, 1056201309, 1285773924, 1444676211, 1628340858, 982373001, 471159435, 5528023700, 5274542741, 1934545564, 5736026781, 5282304671, 1840503457, 5736680105, 5396751043, 1460234962, 933323488, 1895756519, 1821434609, 2139099915, 5238782735, 1297124119, 5331522339, 731956003, 1943296815, 1299591995, 1390644043, 430545756, 1468584801, 1164385133, 5391719303, 5790190484, 5311226797, 2084510643, 5569969079, 2135346108, 1857729473, 641926083, 5192344517, 5379683287, 5003559897, 1228141528, 1679915995, 1322806235, 5689000937, 5312674815, 782687241, 1802443787, 681776143, 1820167186, 1768203298, 1267741731, 1838896166, 5736381493, 929901638, 1609858119, 933784663, 1161462874, 5525517403, 890649706, 1676205165, 694568077, 5030063249, 5354091675, 5733762210, 780700835, 1281346725, 759370926, 855203002, 1701541060, 987720913, 1317604562, 5466305749, 5745229013, 778702037, 5341908195, 1301048550, 1731560683, 829990126, 987346159, 5209816313, 5446995254, 1362953170, 5373613372, 1352537408, 5821943120, 903064914, 5193973136, 1705196959, 1638450592, 834321831, 638487981, 582935998, 1411417547, 5430531562, 972666367, 5709092351, 576722445, 1325671955, 902090266, 2136598054, 702619189, 2017951293, 1551302223, 5771642460, 1415976541, 1361747557, 774510189, 1954027121, 1674153587, 5310910092, 5517354647, 855084704, 775003809, 5007693478, 1346647726, 555386549, 5500839609, 1086658235, 5794422483, 5358556886, 2017431256, 523431652, 653854437, 1966794472, 870708970, 1078718189, 5329135343, 5383866115, 5007888132, 5050343178, 1143265036, 633917199, 5354372910, 5110597457, 1232121686, 599810758, 863108978, 1482579830, 1053366138, 2023399292, 1248608128, 1468585856, 785244035, 5077598105, 5104535482, 660922340, 982530027, 5196748789]
    # li = [1915029649, 2073000480]
    from_chat_id = 1915029649
    ids = len(li)
    for i in range(ids):
        try:
            chat_id = li[i]
            bot.forward_message(chat_id, from_chat_id, message.message_id)
            send_msg(message.chat.id, f"send successfully to {chat_id}")
        except:
            send_msg(message.chat.id, 'something went wrong')
            send_msg(message.chat.id, f"{chat_id} left bot")


@bot.callback_query_handler(func=lambda c: c.data == 'not_found')
def not_found(call: types.CallbackQuery):
    try:
        # Provide options for custom reply
        bot.answer_callback_query(call.id, text="No movies found. Select an option:")

        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        btn_custom_reply = telebot.types.InlineKeyboardButton('Send Custom Reply', callback_data='custom_reply')
        btn_cancel = telebot.types.InlineKeyboardButton('Cancel', callback_data='cancel')
        markup.add(btn_custom_reply, btn_cancel)

        bot.send_message(call.message.chat.id, "Choose an option:", reply_markup=markup)
    except Exception:
        print("Something went wrong.")


@bot.callback_query_handler(func=lambda c: c.data == 'custom_reply')
def custom_reply(call: types.CallbackQuery):
    try:
        bot.answer_callback_query(call.id, text="Send your custom reply.")
        # Add logic to handle custom reply from the user
    except Exception:
        print("Something went wrong.")


@bot.callback_query_handler(func=lambda c: c.data == 'edit_message')
def edit_message(call: types.CallbackQuery):
    try:
        # Add logic to allow editing of the message
        bot.answer_callback_query(call.id, text="Editing message. Send the corrected information.")
    except Exception:
        print("Something went wrong.")


# Define a list of team members or a specific chat ID for forwarding requests
team_members = [123456789, 987654321]


# Function to forward movie requests to team members
def forward_request_to_team(movie_info, team_member):
    try:
        # Implement the forwarding logic here
        forward_chat_id = team_member  # Replace with the appropriate logic to determine the destination chat ID
        forward_message = f"New movie request:\n\n{movie_info}"

        # Forward the message to the team member
        bot.forward_message(forward_chat_id, movie_info.chat.id, movie_info.message_id)

        # Notify the team member about the forwarded request
        bot.send_message(forward_chat_id, "You have received a new movie request.")
    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Handle the exception gracefully (e.g., send a user-friendly error message)
        bot.reply_to(message, 'An error occurred while processing your request. Please try again later.')


# Update the function for handling "Not Found" button to include forwarding
@bot.callback_query_handler(func=lambda c: c.data == 'not_found')
def not_found(call: types.CallbackQuery):
    try:
        # Provide options for custom reply
        bot.answer_callback_query(call.id, text="No movies found. Select an option:")

        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        btn_custom_reply = telebot.types.InlineKeyboardButton('Send Custom Reply', callback_data='custom_reply')
        btn_forward_request = telebot.types.InlineKeyboardButton('Forward to Team', callback_data='forward_request')
        btn_cancel = telebot.types.InlineKeyboardButton('Cancel', callback_data='cancel')
        markup.add(btn_custom_reply, btn_forward_request, btn_cancel)

        bot.send_message(call.message.chat.id, "Choose an option:", reply_markup=markup)
    except Exception:
        print("Something went wrong.")


# Add a callback to handle forwarding movie requests
def get_movie_info(message):
    pass


@bot.callback_query_handler(func=lambda c: c.data == 'forward_request')
def forward_request(call: types.CallbackQuery):
    try:
        # Replace with the appropriate logic to extract movie information
        movie_info = get_movie_info(call.message)

        # Forward the request to each team member
        for team_member in team_members:
            forward_request_to_team(movie_info, team_member)

        bot.answer_callback_query(call.id, text="Request forwarded to the team.")
    except Exception:
        print("Something went wrong.")


@bot.message_handler(commands=["done"])
def done(message):
    name = message.text
    spltarray = name.split(" ", 2)
    mv_name = spltarray[2]
    c_id = spltarray[1]
    try:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        send_msg(c_id,
                 f'The movie has been added to the database 😊\n You can retry now\n try saying```{mv_name.strip()}```',
                 parse_mode='MarkdownV2', reply_markup=markup)
    except Exception:
        bot.reply_to(message, 'oooops')


@bot.message_handler(func=lambda message: message.text.lower() in ['ok'])
def ok(message):
    try:
        bot.reply_to(message, "😊")
    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Handle the exception gracefully (e.g., send a user-friendly error message)
        bot.reply_to(message, 'An error occurred while processing your request. Please try again later.')


def fetch_final_data(code, num_variants=3):
    s_url = requests.get(f"https://doodapi.com/api/file/info?key=13527p8pcv54of4yjeryk&file_code={code}")
    sdata = s_url.text
    s_parse = json.loads(sdata)

    variants = s_parse['result'][0]['variants'][:num_variants]  # Get a limited number of variants

    img = s_parse['result'][0]['single_img']
    name = s_parse['result'][0]['title']

    file_info = ""
    for variant in variants:
        size = variant['size']
        file_info += f"\nSize: {size}"

    watch_link = f"https://dood.wf/d/{code}"
    watch_link1 = f"https://dood.re/d/{code}"

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton('Watch', url=watch_link, callback_data="click")
    btn2 = telebot.types.InlineKeyboardButton('Alternate link', url=watch_link1)
    markup.add(btn1, btn2)

    return img, name, file_info, markup


@bot.message_handler(func=lambda message: message.text.lower().startswith('@tiviafilmsbot'))
def tagged_message(message):
    try:
        # Extract the movie name from the tagged message
        term = message.text.split(' ', 1)[1]

        # Ensure that the message has a valid movie name after the tag
        if term:
            # Process the message as before
            result = search_videos(term)
            data = url.text
            parse_json = json.loads(data)

            n = len(parse_json['result'])
            if n == 0:
                bot.reply_to(message,
                             'The movie is not in the database right now. It will be added to the database soon.')
                send_msg(message.chat.id,
                         'Please try again after some time. Wait for the next 15 minutes and try again.')
            else:
                try:
                    if __name__ == "__main__":
                        with multiprocessing.Pool(processes=4) as pool:
                            main_data = pool.map(fetch_final_data, [d['file_code'] for d in parse_json['result']])
                            for img, name, file_info, markup in main_data:
                                bot.send_photo(message.chat.id, img, f"<b>TITLE:</b> <i>{name}</i>{file_info}",
                                               parse_mode='html', reply_markup=markup)
                                # Send a "Show More" button
                                markup_more = types.InlineKeyboardMarkup(row_width=1)
                                btn_more = types.InlineKeyboardButton('Show More', callback_data='show_more')
                                markup_more.add(btn_more)
                                bot.send_message(message.chat.id, "Click 'Show More' for additional variants.",
                                                 reply_markup=markup_more)

                except Exception:
                    pass

        else:
            # Reply to the user that the message is missing a movie name
            bot.reply_to(message, 'Please include the movie name after tagging the bot.')

    except Exception:
        bot.reply_to(message, 'oooops')


@bot.callback_query_handler(func=lambda c: c.data == 'show_more')
def show_more(call: types.CallbackQuery):
    try:
        # Add logic to show more variants or handle user interaction
        # You might want to keep track of the user's search term and show additional variants accordingly
        bot.answer_callback_query(call.id, text="Showing more variants...")
        # Add your logic to display more variants or take appropriate action
    except Exception:
        print("Something went wrong.")


@bot.callback_query_handler(func=lambda c: c.data == 'click')
def click(call: types.CallbackQuery):
    try:
        print(call.message.chat.id)
    except Exception:
        print("something went wrong")


@bot.callback_query_handler(func=lambda c: c.data == 'done_default')
def done_default(call: types.CallbackQuery):
    done = done_common(call)
    u_id = done[0]
    mv_name = done[1]
    try:
        # print(f"{mv_name} & {u_id}")
        send_msg(u_id.strip(),
                 f"The movie has been added to the database 😊\nYou can retry now\nTry saying```waste {mv_name.strip()}```",
                 parse_mode="Markdownv2")
        send_msg(1915029649, "message sent successfully ")
    except Exception:
        print("something went wrong")
        send_msg(1915029649, "kuch glt ho gaya :(")


@bot.callback_query_handler(func=lambda c: c.data == 'nothing_found')
def done_default(call: types.CallbackQuery):
    done = done_common(call)
    u_id = done[0]
    mv_name = done[1]
    closer = done[2]
    try:
        # print(f"{mv_name} & {u_id}")
        send_msg(u_id.strip(),
                 f"Sorry 😢😓 no results found for ```waste {mv_name.strip()}```",
                 parse_mode="Markdownv2")
        send_msg(closer, "message sent successfully ")
    except Exception:
        print("something went wrong")
        send_msg(closer, "kuch glt ho gaya :(")


bot.callback_query_handler(func=lambda c: c.data == 'done_custom')


# Define the "/help" command handler
@bot.message_handler(commands=['help'])
def help_command(message):
    # Create a helpful user manual guide
    help_message = """
    Welcome to Tivia Films Bot! Here are some commands you can use:

    /start - Start the bot.
    /clear - Clear all messages in the chat (admin only).
    /help - Display this help message.

    To recommend a movie, tag the bot in your message like this: @tiviafilmsbot movie recommendation.

    Enjoy using the bot!
    """

    # Send the help message to the user
    bot.reply_to(message, help_message, parse_mode='Markdown')


# Define the "/clear" command handler
@bot.message_handler(commands=['clear'])
def clear_command(message, chat_admin_id=None):
    # Check if the user has administrative privileges
    if message.from_user.id == chat_admin_id:  # Replace chat_admin_id with the actual admin user ID
        # Get the chat ID
        chat_id = message.chat.id

        # Get the list of all messages in the chat
        messages = bot.get_chat_history(chat_id, limit=100)  # Adjust the limit as needed

        # Iterate through messages and delete each one
        for msg in messages:
            bot.delete_message(chat_id, msg.message_id)

        # Notify the user that the chat has been cleared
        bot.reply_to(message, "Chat has been cleared.")
    else:
        # Notify the user that they don't have permission to use the command
        bot.reply_to(message, "You don't have permission to use this command.")


# Define the "/safesearch" command handler
@bot.message_handler(commands=['safesearch'])
def safesearch_command(message, chat_admin_id=None):
    # Check if the command has the correct format
    if len(message.text.split()) == 2:
        command, status = message.text.split()

        # Check if the user is an admin (customize this check based on your requirements)
        if message.from_user.id == chat_admin_id:
            if status.lower() == 'on':
                # Activate safe search
                bot.reply_to(message, "Safe search is now ON.")
                # Set a flag or variable to indicate that safe search is ON
                safe_search_enabled = True
            elif status.lower() == 'off':
                # Deactivate safe search
                bot.reply_to(message, "Safe search is now OFF.")
                # Set a flag or variable to indicate that safe search is OFF
                safe_search_enabled = False
            else:
                # Invalid command format
                bot.reply_to(message, "Invalid command format. Use '/safesearch on' or '/safesearch off'.")
        else:
            # User is not authorized to change safe search settings
            bot.reply_to(message, "You don't have permission to change safe search settings.")
    else:
        # Invalid command format
        bot.reply_to(message, "Invalid command format. Use '/safesearch on' or '/safesearch off'.")


# Function to check safe search status
def is_safe_search_enabled(safe_search_enabled=None):
    # Implement logic to check if safe search is enabled
    return safe_search_enabled


def done_custom(call: types.CallbackQuery):
    closer_id = call.message.chat.id
    raw_text = call.message.text
    txtsplt = raw_text.split(',')
    u_id = txtsplt[1]
    print(u_id)
    user = User(u_id)
    # user_dict[c_id] = user
    # mv_name = txtsplt[0]
    try:
        # print(f"{mv_name} & {u_id}")
        msg = bot.send_message(closer_id, "Enter correct name")
        bot.register_next_step_handler(msg, crct_name)
    except Exception:
        print("something went wrong")
        bot.send_message(closer_id, "kuch glt ho gaya :(")


def crct_name(message):
    closer_id = message.chat.id
    mv_name = message.text
    user = user_dict[closer_id]

    try:
        bot.send_message(
            user.u_id.strip(),
            f"The movie has been added to the database 😊\nYou can retry now\nPlease enter correct spelling\n Try "
            f"saying```waste {mv_name.strip()}```",
            parse_mode="Markdownv2")
        bot.send_message(closer_id, "message sent successfully ")
    except Exception:
        print("something went wrong")
        bot.send_message(closer_id, "kuch glt ho gaya :(")


if __name__ == "__main__":
    try:
        bot.enable_save_next_step_handlers(delay=2)
        bot.infinity_polling()
    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Handle the exception gracefully (e.g., send a user-friendly error message)
        bot.reply_to(message, 'An error occurred while processing your request. Please try again later.')
