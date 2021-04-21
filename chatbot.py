from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import configparser
import logging
import redis

global redis1


def main():
    # Load your token and create an Updater for your Bot

    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']),
                         port=(config['REDIS']['REDISPORT']))
    #用于链接Redis。

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(CommandHandler("BMI", BMI))
    dispatcher.add_handler(CommandHandler("RUN", RUN))
    dispatcher.add_handler(CommandHandler("FOOD", FOOD))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def hello_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('Hello,' + msg + "!")
    except (IndexError, ValueError):
        update.message.reply_text('No Hello')

def BMI(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        data = msg.split('+',1)

        d = []
        for i in data:
            d.append(float(i))

        height = d[0]
        weight = d[1]
        bmi = (weight)/(height*height)

        if bmi<18.5:
            str1 = "You are underweight！\nThe following are exercise recommendations for you: \n        Because the lean people have less muscle mass and fat, they can increase muscle mass through exercise and diet to achieve a normal BMI state. The lean people mainly take moderate-intensity strength training and cooperate with aerobic exercise once a week. \n        Strength training of large muscle groups in turn, but due to thinness and relatively few muscles, attention should be paid to the reasonable choice of equipment weight or direct self-weight training, such as training quadriceps, hamstrings, and biceps femoris. \n        You can choose self-weight Squats, lunges, and self-weight heel lifts; chest muscles and triceps can use push-ups at different angles, lighter barbell presses, etc.; back trapezius, deltoids, and latissimus dorsi can use pull-ups or Rowing and other actions."
        if bmi>=18.5 and bmi<24.9:
            str1 = "Your weight is normal！\nThe following are exercise recommendations for you: \n        The general population can do strength training three times a week and aerobic training twice a week. Strength training can use high-intensity multi-style anaerobic training. Strength training covers all muscle groups. It is reasonable to train different large muscle groups every day, such as training the buttocks on Monday. \n        For the legs, train the chest muscles and triceps on Wednesdays, train the back muscles and biceps on Fridays, and train the abdomen from Monday to Friday. Aerobic training is carried out on Tuesday and Thursday, and can be carried out by running, swimming, cycling, HIIT, etc. \n        On Saturdays, you can do some body sports, you can participate in some badminton, basketball and other sports, and rest on Sunday."
        if bmi>=24.9 and bmi<29.9:
            str1 = "You are overweight！\nThe following are exercise recommendations for you: \n        The goal of obese people is to lose fat, but due to their larger body weight, exercise has a greater impact on the joints. Aerobic training is the main method, and some low resistance training is also used. Aerobic training can be brisk walking, swimming, and riding. \n        The strength training is mainly based on the whole body large muscle group training, and each movement is 8-12 times. After losing some weight, add high-intensity intermittent exercises intermittently."
        if bmi>=29.9:
            str1 = "Your weight is obese！\nThe following are exercise recommendations for you: \n        Overweight people bear greater body strength. If you exercise vigorously, abdominal organs and lower limb joints may be severely compressed; \n        Therefore, generally overweight people are not recommended to use running skipping exercises that have a greater impact on the knee joints to reduce fat, follow a gradual approach In principle, it is recommended to use low-intensity, stretching and other static exercises in the early stage, such as brisk walking, yoga and aerobic exercises to make the body adapt; \n        Strength training adopts self-weight training, each movement 6 ~8 times, after a period of time, exercise intensity and time can be appropriately increased."

        redis1.incr(msg)
        update.message.reply_text('Your BMI value is : ' + str(bmi) + " !\n" + str1 )
    except (IndexError, ValueError):
        update.message.reply_text('Usage:/BMI height(m)+weight(kg) (Without The unit symbols)')


def RUN(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /RUN is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        data = msg.split("+", 2)

        d = []
        for i in data:
            d.append(float(i))

        time = d[0]
        distance = d[1]
        weight = d[2]

        speed = time / (distance / 400)
        k = 30 / speed

        heat = weight * k * (time / 60)

        icecream = heat/200

        redis1.incr(msg)
        update.message.reply_text('This run lasts for ' + str(time) + ' minutes and burns ' + str(heat) + ' kcal! \nEquivalent to ' + str(icecream) + ' ice cream!\nKeep up the good work!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /RUN <time(min)>+<distance(m)+<weight(kg)> (Without The unit symbols)')

def FOOD(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword

        if(msg == "Beef"):
            ka = 255
            str5 = "The content of sarcosine in beef is higher than that of any other food, which makes it particularly effective for building muscle and strengthening strength. In the first few seconds of training, sarcosine is the source of fuel for muscles. It can supplement adenosine triphosphate, so that the training can last longer.\n        Beef is low in fat, but rich in combined linoleic acid. These potential antioxidants can effectively combat tissue damage caused by weightlifting and other exercises. In addition, linoleic acid can also act as an antioxidant to maintain muscles."
        if(msg == "Chicken_Breast"):
            ka = 133
            str5 = "Chicken breast meat is high in protein. Whether it is for weight loss or fat loss or muscle gain, you need to consume a lot of protein, because protein is an important component of all cells and tissues of the human body. Among all parts of chicken, chicken breast has the most protein, and its content is comparable to beef. Fitness people eating chicken breast is not only easy to digest, but also relieve muscle loss.\n        Eat chicken breast to relieve fitness fatigue. The carnosine and methcarnosine substances contained in chicken breast can relieve muscle fatigue after fitness. After strenuous exercise, a large amount of lactic acid is generated in the muscles, which makes the muscles sore and very tired. The carnosine and methcarnosine substances in chicken breast can inhibit a certain amount of lactic acid and reduce human fatigue."
        if(msg == "Purple_Sweet_Potato"):
            ka = 82
            str5 = "Purple sweet potato can be antioxidant and anti-aging, because purple sweet potato contains a certain amount of anthocyanin, and anthocyanin has a good effect of scavenging free radicals, appropriate consumption of purple sweet potato to supplement anthocyanin has a good antioxidant, Anti-aging effect.\n        It can slow down the increase in blood sugar, because purple sweet potato itself contains relatively little sugar, and the dietary fiber in it can slow down the speed of sugar absorption. Appropriate eating of purple sweet potato has a good effect of stabilizing blood sugar."
        if(msg == "Milk"):
            ka = 54
            str5 = "Milk is rich in active calcium and is one of the best sources of calcium for humans. It is not only high in content, but the lactose in it can promote the absorption of calcium by the human intestinal wall, the absorption rate is as high as 98%, thereby regulating the metabolism of calcium in the body, maintaining the serum calcium concentration, and enhancing the calcification of bones. Good absorption is especially critical for calcium supplementation. Therefore, the statement that 'milk can replenish calcium' is scientifically justified."
        if(msg == "Lettuce"):
            ka = 16
            str5 = "Lettuce contains dietary fiber and vitamin C, which can eliminate excess fat. The lettuce has a high water content and is very nutritious. The most prominent feature is super low fat and low calories. If you want to lose weight, lettuce is your best Choice.\n        If you want to be healthy, you must ensure the acid-base balance in your body. Lettuce is an alkaline food, which can chemically react with acidic substances such as grains and meat to ensure an acid-base balance."
        redis1.incr(msg)
        update.message.reply_text('Each 100g of ' + msg + ' contains ' + str(ka) + ' kcal!\n        ' + str5)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /FOOD <food name>(Beef,Chicken breast,Purple Sweet Poteto,Milk,Lettuce)')

if __name__ == '__main__':
    main()