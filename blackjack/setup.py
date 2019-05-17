import cx_Freeze
executables = [cx_Freeze.Executable("blackjack.py")]
cx_Freeze.setup(
    name= "Black Jack",
    options={"build_exe":{"packages":["pygame"],
                          "include_files":["images\\icon.png","images\\start_image.gif","images\\rules.png","images\\blackjack_dealer.png","images\\blackjack_user.png","images\\money.png","images\\wallpaper.jpg"]}},
    executables=executables
    )
