if __name__ == '__main__':
    try:
        from data.smile import Smile
        smile = Smile()
        smile.run()
    except:
        print('Sorry, something wrong.')
    import sys
    import pygame as pg
    from data.main import main
    main()
    pg.quit()
    sys.exit()

