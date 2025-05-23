from db_manager import init_db, insert_initial_data
from gui.main_window import run


def main():
    init_db()

    insert_initial_data()
    run()


if __name__ == '__main__':
    main()
