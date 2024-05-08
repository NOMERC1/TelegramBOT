from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()

class Register(StatesGroup):
    fio = State()
    distance = State()
    date = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! '
                         'Я твой личный ассистент для записи на увлекательные марафоны!🏃‍♂🏅\n\n',
                         reply_markup=kb.main)

@router.message(F.text == 'Регистрация')
async def registration(message: Message, state: FSMContext):
    await state.set_state(Register.fio)
    await message.answer('Добро пожаловать в раздел регистрации на марафон!🏃‍♂🏅\n'
                         'Для продолжения регистрации на марафон введите свои ФИО.')

@router.message(F.text == 'Контакты')
async def contact_info(message: Message):
    await message.answer('С удовольствием предоставим вам контактную информацию для связи с организаторами марафона.'
                         'Вы можете обратиться к нам по следующим контактным данным:'
                         '\n\nТелефон: +7 (951) 406-59-25☎\n'
                         'Email: p9ito40k@mail.ru📧'
                         '\n\nНе стесняйтесь обращаться к нам с вопросами, предложениями и отзывами.'
                         'Мы всегда готовы помочь вам!')

@router.message(F.text == 'Результаты марафонов')
async def marathon_results(message: Message):
    await message.answer('Представляем вам результаты предыдущих марафонов! Вот результаты соревнований:\n\n'
                         '🏅 Дистанция 5 км: 🏃‍♂\n'
                         '1. Иванова Ольга, время: 25:34\n'
                         '2. Петров Алексей, время: 27:15\n'
                         '3. Смирнова Ирина, время: 28:20\n\n'
                         '🏅Дистанция 10 км:🏃‍♂\n'
                         '1. Козлов Иван, время: 45:10\n'
                         '2. Сидорова Анна, время: 50:05\n'
                         '3. Михайлов Павел, время: 52:03\n\n'
                         'Благодарим всех за участие!'
                         'Ждем вас снова на следующих марафонах')

@router.message(F.text == 'Помощь')
async def participator(message: Message):
    await message.answer('Добро пожаловать в наш сервис поддержки!'
                         'Если у вас возникли вопросы или вам нужна помощь, мы готовы помочь вам. 🤝\n\n'
                         'Этот бот создан для обеспечения удобной регистрации на марафоны и '
                         'предоставления информации об организаторах и мероприятиях. 🏃‍♂🏅\n\n'
                         'Для регистрации на марафон вам необходимо нажать кнопку '
                         '"Я хочу зарегистрироваться на марафон".'
                         'Затем введите своё ФИО,'
                         'выберите километраж марафона и укажите дату проведения марафона. 📝👟🗓\n\n'
                         'Если вы хотите узнать о своих регистрациях, '
                         'нажмите кнопку "Мои регистрации" и укажите своё ФИО.'
                         'Вы получите информацию о марафонах на которые вы зарегистрированы.📋\n\n'
                         'Чтобы узнать больше о нас, нажмите кнопку "О нас".'
                         'А если вам нужны дополнительные сведения или у вас есть предложения, '
                         'нажмите кнопку "Контакты", чтобы связаться с нами. ✉📞')

@router.message(F.text == 'О нас')
async def participator(message: Message):
    await message.answer('Мы - команда организаторов марафонов,'
                         'которая с гордостью создает и проводит увлекательные соревнования '
                         'для всех любителей бега и здорового образа жизни.🏃‍♂🏅\n\n'
                         'Уже на протяжении многих лет мы успешно организуем марафоны,'
                         'принося радость и удовлетворение участникам со всех уголков.'
                         'Наши мероприятия пользуются большой популярностью, '
                         'и множество участников становились победителями, '
                         'получая заслуженные призы и награды. 🎉🏆\n\n'
                         'Если у вас возникли вопросы или вы хотите узнать больше о нас, '
                         'не стесняйтесь связаться с нами, нажав кнопку "Контакты". '
                         'Мы всегда рады общению и готовы помочь вам!💬')

@router.message(Register.fio)
async def register_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer('Выберите дистанцию марафона:', reply_markup=await kb.distances())

@router.callback_query(F.data.startswith('distance_'))
async def distance(callback: CallbackQuery, state: FSMContext):
    distance_text = callback.data.split('_')[1]
    await callback.answer('Вы выбрали дистанцию марафона')
    await state.update_data(distance=distance_text)
    await callback.message.answer('Выберите дату марафона:',
                                  reply_markup=await kb.dates(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('date_'))
async def date(callback: CallbackQuery, state: FSMContext):
    date_text = callback.data.split('_')[1]
    await callback.answer('Вы выбрали дату марафона')
    await state.update_data(date=date_text)
    data = await state.get_data()
    fio = data.get('fio')
    distance = data.get('distance')
    date = data.get('date')
    await rq.set_user(callback.from_user.id, fio, distance, date)
    await callback.message.answer('Поздравляем! '
                                  'Регистрация на марафон успешно завершена. '
                                  'Вы стали частью нашей увлекательной гонки на выносливость. '
                                  'Готовьтесь к захватывающему путешествию, исполненному вызовов и побед! '
                                  'Подготовьтесь к старту и будьте готовы выложиться по полной на трассе. '
                                  'Удачи! 🏃🏻‍♂🏃🏼‍♀🎽')