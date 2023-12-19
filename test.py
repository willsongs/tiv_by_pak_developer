import telebot
import requests
import json
import multiprocessing
from telebot import types

# ...

# Use an environment variable or a configuration file for storing the API_TOKEN
API_TOKEN = '5505287179:AAFu9iQ7jTeY8JM_KTN7hPe6oUawkYI195A'

# Create the bot instance
bot = telebot.TeleBot(API_TOKEN)

# ...

# Define constants for repeated IDs or values
TEAM_MEMBERS = [123456789, 987654321]
DODAPI_KEY = '13527p8pcv54of4yjeryk'


# ...

# Use try-except blocks more selectively and handle specific exceptions
@bot.message_handler(commands=["start"])
def start(message):
    try:
        user = message.from_user
        save_user_info(user.id, user.username, user.first_name, user.last_name, message.chat.id)
        print("User information saved")
        markup = types.ReplyKeyboardMarkup(row_width=2)
        bot.reply_to(message, 'Okay! Now enter any name of a movie or web series you want to watch today',
                     reply_markup=markup)
    except Exception as e:
        print(f"Error in 'start' command: {e}")
        bot.reply_to(message, 'Oops! Something went wrong.')


# ...

# Use f-strings for string formatting for better readability
@bot.callback_query_handler(func=lambda c: c.data == 'show_more')
def show_more(call: types.CallbackQuery):
    try:
        # Implement logic to show more variants or handle user interaction
        bot.answer_callback_query(call.id, text="Showing more variants...")
        # Add your logic to display more variants or take appropriate action
    except Exception as e:
        print(f"Error in 'show_more' callback: {e}")
        bot.answer_callback_query(call.id, text="Something went wrong.")


# ...

# Use a single try-except block for multiple related operations
@bot.callback_query_handler(func=lambda c: c.data == 'click')
def click(call: types.CallbackQuery):
    try:
        print(call.message.chat.id)
    except Exception as e:
        print(f"Error in 'click' callback: {e}")
        bot.answer_callback_query(call.id, text="Something went wrong.")


# ...

# Use the 'format' method for better string formatting
@bot.callback_query_handler(func=lambda c: c.data == 'done_default')
def done_default(call: types.CallbackQuery):
    done = done_common(call)
    u_id, mv_name = done[0], done[1]
    try:
        send_msg(u_id.strip(),
                 f"The movie has been added to the database 😊\nYou can retry now\nTry saying `waste {mv_name.strip()}`",
                 parse_mode="Markdownv2")
        send_msg(1915029649, "Message sent successfully ")
    except Exception as e:
        print(f"Error in 'done_default' callback: {e}")
        send_msg(1915029649, "Something went wrong :(")


# ...

# Avoid using global variables; pass necessary data as function arguments
@bot.message_handler(regexp=r'\b[ a-zA-Z.]+\b')
def name(message):
    try:
        term = message.text
        u_id = message.from_user.id
        print(term)
        url = requests.get(f"https://doodapi.com/api/search/videos?key={DODAPI_KEY}&search_term={term}")
        data = url.text
        parse_json = json.loads(data)

        n = len(parse_json['result'])
        if n == 0:
            bot.reply_to(message, 'The movie is not in the database right now. It will be added to the database soon.')
            send_msg(message.chat.id, 'Please try again after some time. Wait for the next 15 minutes and try again.')
        else:
            try:
                if __name__ == "__main__":
                    with multiprocessing.Pool(processes=4) as pool:
                        # Use list comprehension for better readability
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
            except Exception as e:
                print(f"Error in 'name' message handler: {e}")
    except Exception as e:
        print(f"Error in 'name' message handler: {e}")
        bot.reply_to(message, 'Oops! Something went wrong.')


# ...

# Use a try-except block for better error handling
if __name__ == "__main__":
    try:
        bot.enable_save_next_step_handlers(delay=2)
        bot.infinity_polling()
    except Exception as e:
        print(f"Error in polling: {e}")
