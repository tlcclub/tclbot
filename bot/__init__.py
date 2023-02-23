import logging  
import json
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.keyboards.keyboards import  (
    BTN_PLACE_SELL,
    BTN_PALCE_BUY,
    BTN_DONE,
    SELL,
    BUY,
    HELP,
    DONE
)
from bot.messages.messages import Messages
import config

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

log = logger

bot = Bot(token=config.BOT_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    mtype = State()
    userid = State()
    title = State()
    description = State()
    photo = State()
    price = State()
    photo_counter = State()


msg = Messages()


@dp.message_handler(commands=['start', 'new'])
async def do_start(message: types.Message):
    await Form.mtype.set()
    await Form.userid.set()
    await message.answer(text=f'Этот бот поможет Вам правильно оформить объявление для Барахолки TLC',
                         reply_markup=HELP)


@dp.callback_query_handler(text='sell', state=Form)
async def do_callback_sell(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.update_data(mtype='sell', userid=callback_query.from_user.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=msg.sell(callback_query.from_user),
    )
    await Form.next()
    await bot.send_message(callback_query.from_user.id,
                           text="Введите название товара")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals=['cancel', 'отмена'], ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Создание объявлениея отменено!\nПриходите еще!',
                        reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.title)
async def do_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
        log.info(data)
    await Form.next()
    await message.reply("Введите описание")


@dp.message_handler(state=Form.description)
async def do_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        log.info(data)
    await Form.next()
    await message.reply("Введите картинки")


@dp.message_handler(content_types=[types.message.ContentType.PHOTO], state=Form)
async def do_photo(message: types.Message, state: FSMContext):
    log.info(f"DO_PHOTO {message}")
    await state.update_data(photo=[message.photo[-1]], photo_counter=1)
    await state.set_state('next_photo')
    await Form.next()
    await message.answer(text="C Фото всё?", reply_markup=DONE)

@dp.message_handler(state='next_photo', content_types=[types.message.ContentType.PHOTO])
async def next_photo_handler(message: types.Message, state:FSMContext):
    # we are here if the second and next messages are photos
    async with state.proxy() as data:
        data['photo_counter'] += 1
        photo_counter = data['photo_counter']
        data.get('photo').append(message.photo[-1])
        log.info(data)
    await state.set_state('next_photo')
    await Form.next()
    await message.answer(text="C Фото всё?", reply_markup=DONE)


@dp.callback_query_handler(text='done', state=Form)
async def do_callback_photo_done(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        log.info(f" QUERY PHOTO DONE {data}")
    await Form.next()
    await bot.send_message(callback_query.from_user.id,
                           text="осталось ввести ценник")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form)
async def do_price(message: types.Message, state: FSMContext):
    log.info("======")
    log.info(message)
    log.info("======")
    async with state.proxy() as data:

        data['price'] = message.text
        log.info(data)
        await types.ChatActions.upload_photo()

        markup = types.ReplyKeyboardRemove()
        caption = md.text(
            md.text(md.bold(f"{data.get('title')} - {data.get('price')}₱")),
            md.text(data.get('description')),
            md.text(message.from_user.username),
            sep="\n"
        ),
        media_group = types.MediaGroup()
        for p in data.get('photo'):
            await p.download()
            file = await bot.get_file(p.file_id)
            log.info(file)
            media_group.attach_photo(types.InputMediaPhoto(
                                     file.file_path,
                                     cation=caption,
                                     parse_mode=types.ParseMode.MARKDOWN
                ))


        # And send message
        await message.reply_media_group(media_group)
    await state.finish()

# @dp.callback_query_handler(text='buy')
# async def process_callback_wind(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(
#         callback_query.from_user.id,
#         text=msg.buy(callback_query.from_user),
#     )