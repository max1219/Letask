# import asyncio
# import sys
# from time import perf_counter
#
#
# async def test() -> None:
#     # Тест для выявления того, имеет ли смысл хранить id в database/user_ids: set[int]
#     # Проверка наличия id в базе данных производится при получении каждого апдейта, так что проблема актуальна
#     # Хранение в ОЗУ usernames и связи между id и username счёл не столь важными: строка весит больше, а проверка
#     # наличия username в бд и получение id по username используются лишь в некоторых апдейтах
#     # Как результат, на 10000 записей и 20000 проверок вес в ОЗУ добавленного множества 524504 байта (менее 0.5 мб),
#     # время записи с множеством на 0.44 секунды больше 2%, время проверки меньше в 12000 раз
#
#     start_test = perf_counter()
#
#     for i in range(1, 20001, 2):
#         await database_with_set.add_user(i, str(i))
#
#     time_to_write = perf_counter() - start_test     # 22.407
#
#     for i in range(1, 20001):
#         await database_with_set.check_user_id_registered(i)
#
#     time_to_check = perf_counter() - start_test - time_to_write     # 0.003
#
#     print(f"Add 10000 records in database with set {time_to_write}, "
#           f"check 20000 records {time_to_check}, total {time_to_check + time_to_write}")
#
#     print("Size of user_ids - ", sys.getsizeof(database_with_set.user_ids))
#
#
#     start_test = perf_counter()
#
#     for i in range(1, 20001, 2):
#         await database_without_set.add_user(i, str(i))
#
#     time_to_write = perf_counter() - start_test     # 21.967
#
#     for i in range(1, 20001):
#         await database_without_set.check_user_id_registered(i)
#
#     time_to_check = perf_counter() - start_test - time_to_write     # 37.324
#
#     print(f"Add 10000 records in database without set {time_to_write}, "
#           f"check 20000 records {time_to_check}, total {time_to_check + time_to_write}")
#
#
# if __name__ == '__main__':
#     asyncio.run(test())
